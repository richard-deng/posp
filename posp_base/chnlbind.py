# coding: utf-8
import copy
import logging
import datetime

import tools
from channel import Channel
from define import TOKEN_POSP_CORE
from zbase.web.validator import T_INT, T_STR
from zbase.base.dbpool import get_connection_exception

log = logging.getLogger()


class ChannelBind:

    TABLE = 'chnlbind'
    TABLE_ID = 'id'
    MUST_KEY = {
        'userid': T_INT,
        'tradetype': T_INT,
        'chnlid': T_INT,
        'priority': T_INT,
        '`change`': T_INT,
        'bigmchnt': T_INT,
        'available': T_INT,
    }
    OPTION_KEY = {
        'mchntid': T_STR,
        'termid': T_STR,
        'mchntnm': T_STR,
    }
    DATETIME_KEY = {
        'create_time': 'datetime',
        'update_time': 'datetime',
    }
    KEYS = list(set(MUST_KEY.keys() + OPTION_KEY.keys() + DATETIME_KEY.keys()))

    def __init__(self, chnlbind_id):
        self.id = chnlbind_id
        self.data = {}
        self.keys = ChannelBind.KEYS

    def load(self):
        where = {'id': self.id}
        keep_fields = copy.deepcopy(ChannelBind.KEYS)
        log.debug('keep_fields=%s', keep_fields)
        keep_fields.append(ChannelBind.TABLE_ID)
        with get_connection_exception(TOKEN_POSP_CORE) as conn:
            record = conn.select_one(table=ChannelBind.TABLE, fields=keep_fields, where=where)
            self.data = tools.trans_time(record, ChannelBind.DATETIME_KEY)

    def update(self, values):
        where = {'id': self.id}
        with get_connection_exception(TOKEN_POSP_CORE) as conn:
            ret = conn.update(table=ChannelBind.TABLE, values=values, where=where)
            return ret

    @classmethod
    def create(cls, values):
        with get_connection_exception(TOKEN_POSP_CORE) as conn:
            ret = conn.insert(table=ChannelBind.TABLE, values=values)
            return ret

    @classmethod
    def page(cls, **kwargs):
        need_query = ['userid', 'mchntid', 'termid']
        where = {}
        for k, v in kwargs.iteritems():
            if k in need_query and kwargs.get(k):
                where[cls.TABLE + '.' + k] = kwargs.get(k)
        other = kwargs.get('other', '')
        page = kwargs.get('page', 1)
        page_size = kwargs.get('maxnum', 10)
        on = {'chnlbind.chnlid': 'channel.id'}
        keep_fields = [cls.TABLE + '.' + key for key in cls.KEYS]
        keep_fields.append(Channel.TABLE+'.'+'name')
        keep_fields.append(ChannelBind.TABLE+'.'+'id')
        with get_connection_exception(TOKEN_POSP_CORE) as conn:
            sql = conn.select_join_sql(
                table1=cls.TABLE,
                table2=Channel.TABLE,
                on=on,
                fields=keep_fields,
                where=where,
            )

            pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
            pager.split()
            if pager.count > 0:
                for data in pager.pagedata.data:
                    tools.trans_time(data, ChannelBind.DATETIME_KEY)
            return pager.pagedata.data, pager.count

    def switch_available(self, available):
        now = datetime.datetime.now()
        now_str = now.strftime('%Y-%m-%d %H:%M:%S')
        where = {'id': self.id}
        values = {'available': available, 'update_time': now_str}
        with get_connection_exception(TOKEN_POSP_CORE) as conn:
            ret = conn.update(table=ChannelBind.TABLE, values=values, where=where)
            return ret
