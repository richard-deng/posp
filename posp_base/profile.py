# coding: utf-8
import logging

from zbase.base.dbpool import get_connection_exception

log = logging.getLogger()

class Profile:

    TABLE = 'profile'
    PROFILE_MUST_KEY = [
        'user_state', 'banktype', 'allowarea', 'groupid', 'is_developer',
        'last_admin', 'brchbank_code', 'is_salesman', 'swiftCode',
        'last_modify', 'licenseactive_date',
    ]
    PROFILE_OPTION_KEY = [
        'nickname', 'name', 'idnumber', 'province', 'city', 'bankname',
        'bankuser', 'bankaccount', 'mobile', 'email',
    ]
    PROFILE_DATETIME_KEY = {'last_modify': 'date', 'licenseactive_date': 'date'}
    PROFILE_KEY = list(set(PROFILE_MUST_KEY + PROFILE_OPTION_KEY + PROFILE_DATETIME_KEY.keys()))

    def __init__(self, userid):
        self.userid = userid
        self.data = {}
        self.keys = Profile.PROFILE_KEY
        self.load()

    def load(self):
        keep_fields = self.keys
        where = {'userid': self.userid}
        with get_connection_exception('posp_core') as conn:
            record = conn.select_one(table=Profile.TABLE, fields=keep_fields, where=where)
            self.data = self.trans_time(record)

    def trans_time(self, data):

        if not data:
            return {}

        for key, data_type in Profile.PROFILE_DATETIME_KEY.iteritems():
            if data.get(key):
                if data_type in ('time', 'date'):
                    data[key] = str(data[key])
                elif data_type == 'datetime':
                    data[key] = data.get(key).strftime('%Y-%m-%d %H:%M:%S')
                else:
                    pass
        return data

    def update(self, values):
        func = 'update'
        where = {'userid': self.userid}
        log.debug('func=%s|userid=%s|values=%s', func, self.userid, values)
        with get_connection_exception('posp_core') as conn:
            ret = conn.update(table=Profile.TABLE, values=values, where=where)
            log.debug('func=%s|userid=%s|values=%s|ret=%s', func, self.userid, values, ret)
            return ret