# coding: utf-8
import logging
import datetime

import tools
from define import TOKEN_POSP_MIS
from zbase.base.dbpool import get_connection_exception

log = logging.getLogger()


class Terminal:

    TABLE = 'terminal'
    TABLE_ID = 'id'
    TERMINAL_MUST_KEY = {
        'userid': 'int',
        'terminalid': 'str',
        'psamid': 'str',
        'producer': 'str',
        'model': 'str',
        'produce_date': 'datetime',
        'deliver_date': 'datetime',
        'tck': 'str',
        'used': 'int',
        'state': 'int',
        'last_modify': 'datetime',
        'last_admin': 'int',
    }
    TERMINAL_OPTION_KEY = {
        'advice': 'str',
        'group_id': 'int',
        'qpos_pubkey': 'str'
    }
    TERMINAL_DATETIME_KEY = {
        'produce_date': 'datetime',
        'deliver_date': 'datetime',
        'last_modify': 'datetime',
    }
    TERMINAL_KEY = TERMINAL_MUST_KEY.keys() + TERMINAL_OPTION_KEY.keys()

    def __init__(self, terminal_id):
        self.id = terminal_id
        self.data = {}
        self.keys = Terminal.TERMINAL_KEY + Terminal.TABLE_ID

    def load(self):
        where = {'id': self.id}
        with get_connection_exception(TOKEN_POSP_MIS) as conn:
            record = conn.select_one(table=Terminal.TABLE, fields=self.keys, where=where)
            ret = tools.trans_time(data=record, datetime_keys=Terminal.TERMINAL_DATETIME_KEY)
            return ret

    def update(self, values):
        where = {'id': self.id}
        with get_connection_exception(TOKEN_POSP_MIS) as conn:
            ret = conn.update(table=Terminal.TABLE, values=values, where=where)
            return ret

    @classmethod
    def create(cls, values):
        with get_connection_exception(TOKEN_POSP_MIS) as conn:
            ret = conn.insert(table=Terminal.TABLE, values=values)
            return ret

    @classmethod
    def page(cls, **kwargs):
        need_query = ['terminalid', 'model', 'state']
        where = {}
        for k, v in kwargs.iteritems():
            if k in need_query and kwargs.get(k):
                where[k] = kwargs.get(k)
        other = kwargs.get('other', '')
        page = kwargs.get('page', 1)
        page_size = kwargs.get('maxnum', 10)
        keep_fields = cls.TERMINAL_KEY + cls.TABLE_ID
        with get_connection_exception('posp_core') as conn:
            sql = conn.select_sql(table=Terminal.TABLE, where=where, fields=keep_fields, other=other)
            pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
            pager.split()
            return pager.pagedata.data, pager.count


