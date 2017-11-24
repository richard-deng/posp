# coding: utf-8
import logging
import datetime
from zbase.base.dbpool import get_connection_exception

log = logging.getLogger()


class CardBin:

    TABLE = 'cardbin'
    CARDBIN_MUST_KEY = [
        'bankname', 'bankid', 'cardcd', 'cardlen',
        'cardbin', 'cardname', 'cardtp', 'cardorg'
    ]
    CARDBIN_OPTION_KEY = ['`foreign`']
    CARDBIN_DATETIME_KEY = []
    CARDBIN_KEY = CARDBIN_MUST_KEY + CARDBIN_OPTION_KEY


    def __init__(self, id):
        self.id = id
        self.data = {}
        self.keys = CardBin.CARDBIN_KEY

    def load(self):
        where = {'id': self.id}
        with get_connection_exception('posp_core') as conn:
            record = conn.select_one(table=CardBin.TABLE, fields=self.keys, where=where)
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
        keep_fields = cls.CARDBIN_KEY + ['id']
        with get_connection_exception('posp_core') as conn:
            sql = conn.select_sql(table=CardBin.TABLE, where=where, fields=keep_fields, other=other)
            pager = conn.select_page(sql, pagecur=page, pagesize=page_size)
            pager.split()
            return pager.pagedata.data, pager.count