# coding: utf-8
import copy
import logging

import tools
from define import TOKEN_POSP_MIS
from zbase.base.dbpool import get_connection_exception
from zbase.web.validator import T_INT, T_STR

log = logging.getLogger()


class Terminal:

    TABLE = 'terminal'
    TABLE_ID = 'id'
    MUST_KEY = {
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
    OPTION_KEY = {
        'advice': T_STR,
        'group_id': T_INT,
        'qpos_pubkey': T_STR
    }
    DATETIME_KEY = {
        'produce_date': 'datetime',
        'deliver_date': 'datetime',
        'last_modify': 'datetime',
    }
    QUERY_KEY = {
        'terminalid': T_STR,
        'model': T_STR,
        'state': T_INT,
    }
    KEYS = MUST_KEY.keys() + OPTION_KEY.keys()

    def __init__(self, terminal_id):
        self.id = terminal_id
        self.data = {}
        self.keys = {}

    def load(self):
        where = {'id': self.id}
        keep_fields = copy.deepcopy(Terminal.KEYS)
        keep_fields.append(Terminal.TABLE_ID)
        with get_connection_exception(TOKEN_POSP_MIS) as conn:
            record = conn.select_one(table=Terminal.TABLE, fields=keep_fields, where=where)
            self.data = tools.trans_time(data=record, datetime_keys=Terminal.DATETIME_KEY)

    @classmethod
    def load_by_terminalid(cls, terminalid):
        where = {'terminalid': terminalid}
        with get_connection_exception(TOKEN_POSP_MIS) as conn:
            record = conn.select_one(table=cls.TABLE, fields='*', where=where)
            ret = tools.trans_time(data=record, datetime_keys=cls.DATETIME_KEY)
            cls.data = ret
            return cls

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
        need_query = cls.QUERY_KEY.keys()
        where = {}
        for k, v in kwargs.iteritems():
            if k in need_query and kwargs.get(k):
                where[k] = kwargs.get(k)
        other = kwargs.get('other', '')
        page = kwargs.get('page', 1)
        page_size = kwargs.get('maxnum', 10)
        log.debug('TERMINAL_KEY=%s', cls.KEYS)
        keep_fields = copy.deepcopy(cls.KEYS)
        keep_fields.append(cls.TABLE_ID)
        log.debug('keep_fields=%s', keep_fields)
        with get_connection_exception(TOKEN_POSP_MIS) as conn:
            sql = conn.select_sql(table=Terminal.TABLE, where=where, fields=keep_fields, other=other)
            pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
            pager.split()
            return pager.pagedata.data, pager.count


