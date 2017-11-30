# coding: utf-8
import copy
import logging
import datetime
from zbase.web.validator import T_INT, T_STR
from zbase.base.dbpool import get_connection_exception

log = logging.getLogger()


class CardBin:

    TABLE = 'cardbin'
    TABLE_ID = 'id'
    MUST_KEY = {
        'bankname': T_STR,
        'bankid': T_STR,
        'cardcd': T_STR,
        'cardlen': T_INT,
        'cardbin': T_STR,
        'cardname': T_STR,
        'cardtp': T_STR,
        'cardorg': T_STR,
    }

    OPTION_KEY = {
        '`foreign`': T_INT
    }
    DATETIME_KEY = []
    KEYS = MUST_KEY.keys() + OPTION_KEY.keys()


    def __init__(self, id):
        self.id = id
        self.data = {}
        self.keys = CardBin.KEYS

    def load(self):
        where = {'id': self.id}
        keep_fields = copy.deepcopy(CardBin.KEYS)
        keep_fields.append(CardBin.TABLE_ID)
        with get_connection_exception('posp_core') as conn:
            record = conn.select_one(table=CardBin.TABLE, fields=keep_fields, where=where)
            self.data = record

    def update(self, valeus):
        where = {'id': self.id}
        with get_connection_exception('posp_core') as conn:
            ret = conn.update(table=CardBin.TABLE, values=valeus, where=where)
            return ret

    @classmethod
    def create(cls, values):
        with get_connection_exception('posp_core') as conn:
            ret = conn.insert(table=CardBin.TABLE, values=values)
            return ret

    @classmethod
    def page(cls, **kwargs):
        need_query = ['bankname', 'bankid', 'cardname', 'cardbin']
        where = {}
        for k, v in kwargs.iteritems():
            if k in need_query and kwargs.get(k):
                where[k] = kwargs.get(k)
        other = kwargs.get('other', '')
        page = kwargs.get('page', 1)
        page_size = kwargs.get('maxnum', 10)
        keep_fields = copy.deepcopy(cls.KEYS)
        keep_fields.append(cls.TABLE_ID)
        with get_connection_exception('posp_core') as conn:
            sql = conn.select_sql(table=CardBin.TABLE, where=where, fields=keep_fields, other=other)
            pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
            pager.split()
            return pager.pagedata.data, pager.count