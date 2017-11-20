# -*- coding: utf-8 -*-
import logging
import traceback
import datetime
from zbase.base.dbpool import get_connection_exception
from posp_base.merchant import User
from posp_base.profile import Profile
from posp_base.channel import Channel

log = logging.getLogger()


def trans_datetime(date_value):
    func = 'trans_datetime'
    log.debug('func=%s|date_value=%s', func, date_value)
    date_str = datetime.datetime.strftime(date_value, '%Y-%m-%d %H:%M:%S')
    log.debug('func=%s|date_value=%s|date_str=%s', func, date_value, date_str)
    return date_str


def change_channel_state(channel_id, state):
    func = 'change_channel_state'
    log.debug('func=%s|channel_id=%s|state=%s', func, channel_id, state)
    channel = Channel(channel_id)
    ret = channel.switch_state(state)
    if ret == 1:
        return True
    return False


def get_channel(channel_id):
    func = 'get_channel_info'
    log.debug('func=%s|channel_id=%s', func, channel_id)
    channel = Channel(channel_id)
    channel.load()
    return channel.data


def get_channel_names():
    names = Channel.load_names()
    return names


def update_channel(channel_id, values):
    func = 'update_channel'
    log.debug('func=%s|channel_id=%s|values=%s', func, channel_id, values)

    channel = Channel(channel_id)
    ret = channel.update(values)
    if ret == 1:
        return True
    return False


def create_channel(values):
    func = 'create_channel'
    log.debug('func=%s|values=%s', func, values)
    ret = Channel.create(values)
    if ret == 1:
        return True
    return False


def get_merchant(merchant_id):
    func = 'get_merchant'
    log.debug('func=%s|merchant_id=%s', func, merchant_id)
    on = {'auth_user.id': 'profile.userid'}
    where = {'auth_user.id': merchant_id}
    keep_fields = [
        'auth_user.id', 'auth_user.mobile', 'auth_user.state', 'auth_user.email',
        'auth_user.is_active', 'profile.province', 'profile.city', 'profile.nickname',
        'profile.bankuser', 'profile.bankaccount',  'profile.bankname', 'profile.name',
        'profile.idnumber',
    ]
    with get_connection_exception('posp_core') as conn:
        ret = conn.select_join_one(table1='auth_user', table2='profile', fields=keep_fields, on=on, where=where)
        log.debug('func=%s|merchant_id=%s|ret=%s', func, merchant_id, ret)
        return ret


def update_merchant(merchant_id, values):
    func = 'update_merchant'
    log.debug('func=%s|merchant_id=%s|values=%s', func, merchant_id, values)

    now = datetime.datetime.now()
    user_values = {}
    profile_values = {}

    profile_values['name'] = values.pop('name')
    profile_values['nickname'] = values.pop('nickname')
    profile_values['idnumber'] = values.pop('idnumber')
    profile_values['province'] = values.pop('province')
    profile_values['city'] = values.pop('city')
    profile_values['bankname'] = values.pop('bankname')
    profile_values['bankuser'] = values.pop('bankuser')
    profile_values['bankaccount'] = values.pop('bankaccount')
    profile_values['last_modify'] = now.strftime('%Y-%m-%d')

    user_values['mobile'] = values.pop('mobile')
    user_values['email'] = values.pop('email')
    user_values['is_active'] = values.pop('is_active')
    user_values['state'] = values.pop('state')

    user = User(merchant_id)
    user.update(user_values)

    profile = Profile(merchant_id)
    profile.update(profile_values)


def build_user(values):
    func='build_user'
    log.debug('func=%s|input=%s', func, values)

    # 添加其它数据
    user = {}
    now = datetime.datetime.now()
    now_str = now.strftime('%Y-%m-%d %H:%M:%S')

    mobile = values.pop('mobile')
    user['email'] = values.pop('email')
    user['state'] = values.pop('state')
    user['is_active'] = values.pop('is_active')

    user['username'] = mobile
    user['mobile'] = mobile
    user['merchant_code'] = ''
    user['user_type'] = 0
    user['password'] = '123456'
    user['admin_password'] = ''
    user['is_staff'] = 0
    user['is_superuser'] = 0
    user['last_login'] = now_str
    user['date_joined'] = now_str

    log.debug('func=%s|output=%s', func, user)
    return user


def build_profile(values):
    # 添加其它数据
    func = 'build_profile'
    log.debug('func=%s|input=%s', func, values)
    now = datetime.datetime.now()

    profile = {}
    profile['nickname'] = values.pop('nickname')
    profile['name'] = values.pop('name')
    profile['idnumber'] = values.pop('idnumber')
    profile['province'] = values.pop('province')
    profile['city'] = values.pop('city')
    profile['bankname'] = values.pop('bankname')
    profile['bankuser'] = values.pop('bankuser')
    profile['bankaccount'] = values.pop('bankaccount')
    profile['user_state'] = values.get('state')
    profile['banktype'] = 0
    profile['allowarea'] = 0
    profile['groupid'] = 0
    profile['is_developer'] = 0
    profile['last_modify'] = now.strftime('%Y-%m-%d')
    profile['brchbank_code'] = '0'
    profile['is_salesman'] = 0
    profile['swiftCode'] = 0
    profile['licenseactive_date'] = '1970-01-01 00:00:00'
    profile['last_admin'] = 0

    log.debug('func=%s|output=%s', func, profile)
    return profile


def create_merchant(values):
    profile = build_profile(values)
    user = build_user(values)
    flag, userid = User.create(user, profile)
    return flag, userid


def find_user_by_mobile(mobile):
    user = User.load_user_by_mobile(mobile)
    if user.data:
        return True
    return False