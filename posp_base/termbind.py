# coding: utf-8
import copy
import logging

import tools
from define import TOKEN_POSP_CORE
from zbase.base.dbpool import get_connection_exception
from zbase.web.validator import T_INT, T_STR

log = logging.getLogger()


class TermBind:

    TABLE = 'termbind'
    TABLE_ID = 'id'
    MUST_KEY = {
        'userid': T_INT,
        'udid': T_STR,
        'terminalid': T_STR,
        'psamid': T_STR,
        'psamtp': T_STR,
        'pinkey1': T_STR,
        'pinkey2': T_STR,
        'mackey': T_STR,
        'os': T_INT,
        'active_date': T_STR,
        'state': T_INT,
    }
    OPTION_KEY = {
        'tckkey': T_STR,
        'diskey': T_STR,
        'os_ver': T_STR,
        'fackey': T_STR,
        'key_version': T_INT,
        'dig_env': T_STR,
        'enc_pin_key': T_STR,
        'tmk': T_STR,
        'qpos_pubkey': T_STR,
    }
    DATETIME_KEY = {
        'active_date': 'datetime',
    }

    QUERY_KEY = {
        'userid': T_INT,
        'terminalid': T_STR,
        'psamid': T_STR,
    }

    KEYS = MUST_KEY.keys() + OPTION_KEY.keys()


    def __init__(self, tb_id):
        self.id = tb_id
        self.data = {}

    def load(self):
        where = {'id': self.id}
        keep_fields = copy.deepcopy(TermBind.KEYS)
        keep_fields.append(TermBind.TABLE_ID)
        with get_connection_exception(TOKEN_POSP_CORE) as conn:
            record = conn.select_one(table=TermBind.TABLE, fields=keep_fields, where=where)
            self.data = tools.trans_time(record, TermBind.DATETIME_KEY)

    def update(self, values):
        where = {'id': self.id}
        with get_connection_exception(TOKEN_POSP_CORE) as conn:
            ret = conn.update(table=TermBind.TABLE, values=values, where=where)
            return ret

    @classmethod
    def create(cls, values):
        with get_connection_exception(TOKEN_POSP_CORE) as conn:
            ret = conn.insert(table=TermBind.TABLE, values=values)
            return ret

    @classmethod
    def page(cls, **kwargs):
        need_query = cls.QUERY_KEY
        where = {}
        for k, v in kwargs.iteritems():
            if k in need_query and kwargs.get(k):
                where[k] = kwargs.get(k)
        other = kwargs.get('other', '')
        page = kwargs.get('page', 1)
        page_size = kwargs.get('maxnum', 10)
        keep_fields = copy.deepcopy(cls.KEYS)
        keep_fields.append(cls.TABLE_ID)
        with get_connection_exception(TOKEN_POSP_CORE) as conn:
            sql = conn.select_sql(table=TermBind.TABLE, where=where, fields=keep_fields, other=other)
            pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
            pager.split()
            return pager.pagedata.data, pager.count
