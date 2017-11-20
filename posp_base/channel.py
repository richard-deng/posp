# coding: utf-8
import logging
import datetime
from zbase.base.dbpool import get_connection_exception

log = logging.getLogger()


class Channel:

    TABLE = 'channel'
    CHANNEL_MUST_KEY = ['name', 'parent', 'available']
    CHANNEL_OPTION_KEY = [
        'zmk', 'zpk', 'mcc', 'chcd', 'inscd', 'code',
        'regioncd', 'mchntid', 'mchntnm', 'terminalid',
        'mode', 'cuttime', 'upkeytime', 'route', 'tdkey',
        'mackey', 'batch_num',
    ]
    CHANNEL_DATETIME_KEY = {'cuttime': 'time', 'upkeytime': 'datetime'}
    CHANNEL_KEY = list(set(CHANNEL_MUST_KEY + CHANNEL_OPTION_KEY + CHANNEL_DATETIME_KEY.keys()))

    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.data = {}

    def load(self):
        where = {'id': self.channel_id}
        keep_fields = Channel.CHANNEL_KEY
        with get_connection_exception('posp_core') as conn:
            record = conn.select_one(table=Channel.TABLE, fields=keep_fields, where=where)
            self.data = self.trans_time(record)

    def trans_time(self, data):

        if not data:
            return {}

        for key, data_type in Channel.CHANNEL_DATETIME_KEY.iteritems():
            if data.get(key):
                if data_type in ('time', 'date'):
                    data[key] = str(data[key])
                elif data_type == 'datetime':
                    data[key] = data.get(key).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    pass
        return data

    def update(self, values):
        now = datetime.datetime.now()
        values['upkeytime'] = now.strftime('%Y-%m-%d %H:%M:%S')
        where = {'id': self.channel_id}
        with get_connection_exception('posp_core') as conn:
            ret = conn.update(table=Channel.TABLE, values=values, where=where)
            return ret

    def switch_state(self, state):
        with get_connection_exception('posp_core') as conn:
            values = {
                'available': state
            }
            where = {'id': self.channel_id}
            ret = conn.update(table=Channel.TABLE, values=values, where=where)
            return ret

    @classmethod
    def create(cls, values):
        with get_connection_exception('posp_core') as conn:
            ret = conn.insert(table=Channel.TABLE, values=values)
            return ret

    @classmethod
    def load_names(cls):
        with get_connection_exception('posp_core') as conn:
            ret = conn.select(table=Channel.TABLE, fields='name')
            return ret