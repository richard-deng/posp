# coding: utf-8
import logging

import tools
from define import TOKEN_POSP_MIS
from zbase.base.dbpool import get_connection_exception
from zbase.web.validator import T_INT, T_STR

log = logging.getLogger()


class Terminal:

    TABLE = 'terminal'
    TABLE_ID = 'id'
    TERMINAL_MUST_KEY = {
        'userid': T_INT,
        'terminalid': T_STR,
        'psamid': T_STR,
        'producer': T_STR,
        'model': T_STR,
        'produce_date': T_STR,
        'deliver_date': T_STR,
        'tck': T_STR,
        'used': T_INT,
        'state': T_INT,
        'last_modify': T_STR,
        'last_admin': T_INT,
    }
    TERMINAL_OPTION_KEY = {
        'advice': T_STR,
        'group_id': T_INT,
        'qpos_pubkey': T_STR
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
        with get_connection_exception(TOKEN_POSP_MIS) as conn:
            sql = conn.select_sql(table=Terminal.TABLE, where=where, fields=keep_fields, other=other)
            pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
            pager.split()
            return pager.pagedata.data, pager.count


