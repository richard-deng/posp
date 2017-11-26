# coding: utf-8
import logging
import traceback
import datetime

import tools
from define import TOKEN_POSP_TRADE
from zbase.base.dbpool import get_connection_exception
from zbase.web.validator import T_INT, T_STR
from define import DATETIMEException

log = logging.getLogger()




class TradeList:

    QUERY_KEY = {
        'userid': T_INT,
        'chnlid': T_INT,
        'syssn': T_STR,
        'busicd': T_STR,
        'terminalid': T_STR,
        'cardcd': T_STR,
        'retcd': T_STR,
        'sysdtm': T_STR,
        'servername': T_STR
    }

    DATETIME_KEY = {
        'sysdtm': 'datetime'
    }

    def __init__(self, syssn):
        self.syssn = syssn
        self.data = {}

    def load(self):
        table_name = 'record_' + self.syssn[:6]
        where = {'syssn': self.syssn}
        with get_connection_exception(TOKEN_POSP_TRADE) as conn:
            record = conn.select_one(table=table_name, fields='*', where=where)
            self.data = tools.trans_time(record, TradeList.DATETIME_KEY)

    @classmethod
    def _query(cls, table_list, where, other):
        result = []
        with get_connection_exception(TOKEN_POSP_TRADE) as conn:
            for table_name in table_list:
                try:
                    ret = conn.select(table=table_name, fields='*', where=where, other=other)
                    result.extend(ret)
                except Exception as e:
                    if len(e.args) > 0 and e[0] in (1146, ):
                        log.warn('cannot find table=%s', table_name)
                        continue
                    else:
                        raise e
        return result

    @classmethod
    def _gen_tables(cls, start_time, end_time):
        if all((start_time, end_time)):
            try:
                start_time = datetime.datetime.strptime(start_time, '%Y-%m-%d %H:%M:%S')
                end_time = datetime.datetime.strptime(end_time, '%Y-%m-%d %H:%M:%S')
            except Exception:
                log.warn(traceback.format_exc())
                raise DATETIMEException
            table_list = tools.gen_trade_table_list(start_time, end_time)
            return table_list
        else:
            now = datetime.datetime.now()
            table = 'record_' + now.strftime('%Y%m')
            return [table]

    @classmethod
    def _count(cls, total_len, pagesize):
        a = divmod(total_len, pagesize)
        if a[1] > 0:
            page_count = a[0] + 1
        else:
            page_count = a[0]
        return page_count

    @classmethod
    def _gen_ret_range(cls, page, maxnum):
        start = maxnum * page - maxnum
        end = start + maxnum
        return start, end

    @classmethod
    def _query_one_table(cls, table, where, other, page, page_size):
        with get_connection_exception(TOKEN_POSP_TRADE) as conn:
            sql = conn.select_sql(table=table, where=where, fields='*', other=other)
            pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
            pager.split()
            return pager.pagedata.data, pager.count

    @classmethod
    def page(cls, **kwargs):
        need_query = cls.QUERY_KEY.keys()
        where = {}
        for k, v in kwargs.iteritems():
            if k in need_query and kwargs.get(k):
                where[k] = kwargs.get(k)
        other = kwargs.get('other', '')
        page = kwargs.get('page', 1)
        page_size = kwargs.get('maxnum', 10)
        cls.QUERY_KEY.keys().append('id')
        keep_fields = cls.QUERY_KEY.keys()
        keep_fields.append(('id'))
        log.debug('keep_fields=%s', keep_fields)
        table = 'record_201709'
        with get_connection_exception(TOKEN_POSP_TRADE) as conn:
            sql = conn.select_sql(table=table, where=where, fields=keep_fields, other=other)
            pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
            pager.split()
            return pager.pagedata.data, pager.count

    @classmethod
    def page_more(cls, **kwargs):
        need_query = cls.QUERY_KEY.keys()
        where = {}
        for k, v in kwargs.iteritems():
            if k in need_query and kwargs.get(k):
                where[k] = kwargs.get(k)
        other = kwargs.get('other', '')
        page = kwargs.get('page', 1)
        page_size = kwargs.get('maxnum', 10)
        start_time = kwargs.get('start_time')
        end_time = kwargs.get('end_time')
        table_list = cls._gen_tables(start_time, end_time)
        if len(table_list) == 1:
            records, num = cls._query_one_table(table_list[0], where, other, page, page_size)
            info = [tools.trans_time(item, TradeList.DATETIME_KEY) for item in records]
            return info, num
        else:
            records = cls._query(table_list=table_list, where=where, other=other)
            num = len(records)
            info = [tools.trans_time(item, TradeList.DATETIME_KEY) for item in records]


