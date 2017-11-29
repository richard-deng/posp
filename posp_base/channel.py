# coding: utf-8
import copy
import logging
import datetime

import tools
from define import TOKEN_POSP_CORE
from zbase.web.validator import T_INT, T_STR
from zbase.base.dbpool import get_connection_exception

log = logging.getLogger()


class Channel:

    TABLE = 'channel'
    TABLE_ID = 'id'
    MUST_KEY = {
        'name': T_STR,
    }
    OPTION_KEY = {
        'zmk': T_STR,
        'zpk': T_STR,
        'mcc': T_STR,
        'chcd': T_STR,
        'inscd': T_STR,
        'code': T_STR,
        'regioncd': T_STR,
        'mchntid': T_STR,
        'mchntnm': T_STR,
        'terminalid': T_STR,
        'mode': T_INT,
        'route': T_STR,
        'tdkey': T_STR,
        'mackey': T_STR,
        'batch_num': T_STR,
    }
    DATETIME_KEY = {'cuttime': 'time', 'upkeytime': 'datetime'}
    KEYS = list(set(MUST_KEY.keys() + OPTION_KEY.keys() + DATETIME_KEY.keys()))

    def __init__(self, channel_id):
        self.channel_id = channel_id
        self.data = {}

    def load(self):
        where = {'id': self.channel_id}
        keep_fields = copy.deepcopy(Channel.KEYS)
        keep_fields.append(Channel.TABLE_ID)
        with get_connection_exception(TOKEN_POSP_CORE) as conn:
            record = conn.select_one(table=Channel.TABLE, fields=keep_fields, where=where)
            self.data = tools.trans_time(record, Channel.DATETIME_KEY)

    def update(self, values):
        now = datetime.datetime.now()
        values['upkeytime'] = now.strftime('%Y-%m-%d %H:%M:%S')
        where = {'id': self.channel_id}
        with get_connection_exception(TOKEN_POSP_CORE) as conn:
            ret = conn.update(table=Channel.TABLE, values=values, where=where)
            return ret

    def switch_state(self, state):
        with get_connection_exception(TOKEN_POSP_CORE) as conn:
            values = {
                'available': state
            }
            where = {'id': self.channel_id}
            ret = conn.update(table=Channel.TABLE, values=values, where=where)
            return ret

    @classmethod
    def create(cls, values):
        with get_connection_exception(TOKEN_POSP_CORE) as conn:
            ret = conn.insert(table=Channel.TABLE, values=values)
            return ret

    @classmethod
    def load_names(cls):
        with get_connection_exception(TOKEN_POSP_CORE) as conn:
            ret = conn.select(table=Channel.TABLE, fields='name')
            return ret