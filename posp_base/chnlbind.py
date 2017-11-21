# coding: utf-8
# coding: utf-8
import logging
import datetime
from zbase.base.dbpool import get_connection_exception

log = logging.getLogger()


class ChannelBind:

    TABLE = 'chnlbind'
    CHNLBIND_MUST_KEY = [
        'userid', 'tradetype', 'chnlid', 'priority',
        'change', 'bigmchnt', 'available',
    ]
    CHNLBIND_OPTION_KEY = [
        'mchntid', 'termid', 'mchntnm', 'mcc', 'key1',
        'key2', 'key3', 'chnlfee', 'qffee', 'admin',
        'last_admin', 'create_time', 'update_time',
        'tag1', 'tag2', 'memo',
    ]
    CHNLBIND_DATETIME_KEY = {
        'create_time': 'datetime',
        'update_time': 'datetime',
    }
    CHNLBIND_KEY = CHNLBIND_MUST_KEY + CHNLBIND_OPTION_KEY

    def __init__(self, chnlbind_id):
        self.id = chnlbind_id
        self.data = {}
        self.keys = ChannelBind.CHNLBIND_KEY

    def load(self):
        where = {'id': self.id}
        with get_connection_exception('posp_core') as conn:
            record = conn.select_one(table=ChannelBind.TABLE, fields=self.keys, where=where)
            self.data = self.trans_time(record)

    def trans_time(self, data):

        if not data:
            return {}

        for key, data_type in ChannelBind.CHNLBIND_DATETIME_KEY.iteritems():
            if data.get(key):
                if data_type in ('time', 'date'):
                    data[key] = str(data[key])
                elif data_type == 'datetime':
                    data[key] = data.get(key).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    pass
        return data


    def update(self, values):
        where = {'id': self.id}
        with get_connection_exception('posp_core') as conn:
            ret = conn.update(table=ChannelBind.TABLE, values=values, where=where)
            return ret

    @classmethod
    def create(cls, values):
        with get_connection_exception('posp_core') as conn:
            ret = conn.insert(table=ChannelBind.TABLE, values=values)
            return ret