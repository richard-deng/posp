# coding: utf-8
import copy
import logging
import traceback
import datetime

import tools
import page_tool
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
        'servername': T_STR,
        'cancel': T_INT,
        'txamt': T_INT,
        'origssn': T_STR,
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
    def _table_exists(cls, table):
        with get_connection_exception(TOKEN_POSP_TRADE) as conn:
            try:
                ret = conn.select_one(table=table, fields='*')
                if ret:
                    return True
                return False
            except Exception as e:
                if len(e.args) > 0 and e[0] in (1146, ):
                    log.warn('cannot find table=%s', table)
                else:
                    raise e
        return False

    @classmethod
    def _gen_valid_tables(cls, table_arr):
        valid_arr = []
        for table in table_arr:
            flag = cls._table_exists(table)
            if flag:
                valid_arr.append(table)

        return valid_arr

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
    def _gen_table_map(cls, table_list, where={}, other=''):
        ret = {}
        ret2 = []
        with get_connection_exception(TOKEN_POSP_TRADE) as conn:
            for table in table_list:
                record = conn.select_one(table=table, fields='count(*) as count', where=where, other=other)
                if record.get('count') > 0:
                    ret[table] = record.get('count', 0)
                    ret2.append((table, record.get('count', 0)))

            return ret, ret2

    @classmethod
    def _query(cls, table, fields, where, other=''):
        with get_connection_exception(TOKEN_POSP_TRADE) as conn:
            ret = conn.select(table=table, fields=fields, where=where, other=other)
            if ret:
                return ret
            else:
                return []

    @classmethod
    def _query_one_table(cls, table, fields, where, limit, offset):
        with get_connection_exception(TOKEN_POSP_TRADE) as conn:
            other = 'limit %d offset %d' % (limit, offset)
            ret = conn.select(table=table, fields='*', where=where, other=other)
            if ret:
                return ret
            else:
                return []

    @classmethod
    def page_syssn(cls, syssn):
        table_name = 'record_' + syssn[:6]
        flag = cls._table_exists(table_name)
        if not flag:
            return False, [], 0
        with get_connection_exception(TOKEN_POSP_TRADE) as conn:
            info = conn.select_one(table=table_name, fields='*', where={'syssn': syssn})
            if info:
                return True, [info], 1
            else:
                return True, [], 0

    @classmethod
    def page(cls, table, **kwargs):
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
        if start_time and end_time:
            where.update({'sysdtm': ('between', (str(start_time), str(end_time)))})
        keep_fields = cls.QUERY_KEY.keys()
        keep_fields.append(('id'))
        log.debug('keep_fields=%s', keep_fields)
        with get_connection_exception(TOKEN_POSP_TRADE) as conn:
            sql = conn.select_sql(table=table, where=where, fields=keep_fields, other=other)
            pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
            pager.split()
            return True, pager.pagedata.data, pager.count

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
        keep_fields = cls.QUERY_KEY.keys()
        keep_fields.append(('id'))
        start_time = kwargs.get('start_time')
        end_time = kwargs.get('end_time')
        if start_time and end_time:
            where.update({'sysdtm': ('between', (str(start_time), str(end_time)))})
        table_arr = cls._gen_tables(start_time, end_time)
        table_arr = cls._gen_valid_tables(table_arr)
        log.debug('table_arr=%s', table_arr)

        table_map, table_list = cls._gen_table_map(table_list=table_arr, where=where)
        total, origin, judge, judge_map = page_tool.gen_from_table(table_list, page, page_size)
        if total <= page_size:
            info = []
            for table in table_list:
                ret = cls._query(table=table[0], fields=keep_fields, where=where)
                info.extend(ret)
            return True, info, total

        range_map = page_tool.table_range_map(table_list)
        pages = page_tool.gen_total_pages(total, page_size)
        page_range = page_tool.gen_page_range(pages, page_size)
        start, end = page_range.get(page)
        start_table, end_table = page_tool.query_from(range_map, page, page_range)
        if start_table == end_table:
            count, offset = page_tool.gen_one_limit_offset(range_map, start_table, start, end)
            info = cls._query_one_table(table=start_table, fields=keep_fields, where=where, limit=count, offset=offset)
        else:
            if start_table and end_table:
                ret = page_tool.gen_two_limit_offset(range_map, start_table, end_table, start, end)
                info1 = cls._query_one_table(table=start_table, fields=keep_fields, where=where, limit=ret[0][start_table][0], offset=ret[0][start_table][1])
                info2 = cls._query_one_table(table=end_table, fields=keep_fields, where=where, limit=ret[1][end_table][0], offset=ret[1][end_table][1])
                info1.extend(info2)
                info = info1
            else:
                count, offset = page_tool.gen_one_limit_offset(range_map, start_table, start, end)
                info = cls._query_one_table(table=start_table, fields=keep_fields, where=where, limit=count, offset=offset)
        return True, info, total
