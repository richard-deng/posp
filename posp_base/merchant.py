#coding: utf-8

import random
import string
import hashlib
import base64
import logging
import traceback

from profile import Profile
from zbase.base.dbpool import get_connection_exception

log = logging.getLogger()


def gen_passwd(password):
    pre = ''
    data_str = string.lowercase + string.digits
    data_list = list(data_str)
    len = 5
    for i in range(0, len):
        pre += random.choice(data_list)

    deal_passwd=hashlib.sha1(pre+password).hexdigest()
    finish_passwd='sha1$'+pre+'$'+deal_passwd
    return finish_passwd


def gen_old_password(origin_password):
    password_plus = '360'+origin_password+'Huyan'
    client_password = base64.b64encode(hashlib.sha512(password_plus).digest())
    enc_password = hashlib.sha512(client_password).hexdigest()
    return enc_password


def constant_time_compare(val1, val2):
    if len(val1) != len(val2):
        return False
    result = 0
    for x, y in zip(val1, val2):
        result |= ord(x) ^ ord(y)
    return result == 0


def get_hexdigest(algorithm, salt, raw_password):
    if algorithm == 'crypt':
        try:
            import crypt
        except ImportError:
            raise ValueError('"crypt" password algorithm not supported in this environment')
        return crypt.crypt(raw_password, salt)

    if algorithm == 'md5':
        return hashlib.md5(salt + raw_password).hexdigest()
    elif algorithm == 'sha1':
        return hashlib.sha1(salt + raw_password).hexdigest()
    raise ValueError("Got unknown password algorithm type in password.")


def check_password(raw_password, enc_password):
    algo, salt, hsh = enc_password.split('$')
    return constant_time_compare(hsh, get_hexdigest(algo, salt, raw_password))


def check_old_password(raw_password, enc_password):
    hsh = hashlib.sha512(raw_password).hexdigest()
    log.debug('verify pass has=%s, enc=%s', hsh, enc_password)
    return constant_time_compare(hsh, enc_password)


class User:

    TABLE = 'auth_user'
    USER_MUST_KEY = [
        'id', 'username', 'mobile', 'merchant_code', 'user_type',
        'state', 'email', 'password', 'admin_password', 'is_staff',
        'is_active', 'is_superuser', 'last_login', 'date_joined',
    ]
    USER_OPTION_KEY = ['user_level']
    USER_DATETIME_KEY = {'last_login': 'datetime', 'date_joined': 'datetime'}
    USER_KEY = list(set(USER_MUST_KEY + USER_OPTION_KEY + USER_DATETIME_KEY.keys()))


    def __init__(self, userid):
        self.userid = userid
        self.data = {}
        self.login = False
        self.keys = User.USER_KEY

    @classmethod
    def load_user_by_mobile(cls, mobile):
        where = {'mobile': mobile}
        keep_fields = cls.USER_KEY
        with get_connection_exception('posp_core') as conn:
            record = conn.select_one(table=User.TABLE, fields=keep_fields, where=where)
            log.debug('func=load_user_by_mobile|mobile=%s|record=%s', mobile, record)
            cls.data = record
            cls.userid = record.get('id') if record else None
            return cls

    def load(self):
        where = {'id': self.userid}
        keep_fields = self.keys
        with get_connection_exception('posp_core') as conn:
            record = conn.select_one(table=User.TABLE, fields=keep_fields, where=where)
            self.data = self.trans_time(record)

    def trans_time(self, data):

        if not data:
            return {}

        for key, data_type in User.USER_DATETIME_KEY.iteritems():
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
        where = {'id': self.userid}
        log.debug('func=%s|merchant_id=%s|values=%s', func, self.userid, values)
        with get_connection_exception('posp_core') as conn:
            ret = conn.update(table=User.TABLE, values=values, where=where)
            log.debug('func=%s|merchant_id=%s|values=%s|ret=%s', func, self, values, ret)
            return ret

    @classmethod
    def create(cls, user, profile):
        with get_connection_exception('posp_core') as conn:
            try:
                conn.start()
                conn.insert(table=User.TABLE, values=user)
                userid = conn.last_insert_id()
                profile['userid'] = userid
                conn.insert(table=Profile.TABLE, values=profile)
                conn.commit()
                return True, userid
            except Exception:
                log.warn(traceback.format_exc())
                conn.rollback()
                return False, None


    def _check_permission(self, user_type):
        pass

    def check_user_login(self, mobile, password):
        pass