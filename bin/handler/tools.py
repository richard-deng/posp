# -*- coding: utf-8 -*-
import logging
import traceback
import datetime
from constant import INVALID_VALUE
from config import REGISTER_STATE
from config import DEFAULT_ACTIVE
from zbase.base.dbpool import get_connection_exception
from zbase.web.validator import T_INT, T_STR
from posp_base.merchant import User
from posp_base.profile import Profile
from posp_base.channel import Channel
from posp_base.cardbin import CardBin
from posp_base.chnlbind import ChannelBind
from posp_base.terminal import Terminal
from posp_base.termbind import TermBind
from posp_base.merchant import gen_passwd

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
    channel_values = {}

    for key in Channel.KEYS:
        value = values.get(key)
        if value in INVALID_VALUE:
            log.debug('ignore invalid key=%s|value=%s', key, value)
        else:
            channel_values[key] = value

    channel = Channel(channel_id)
    ret = channel.update(channel_values)
    if ret == 1:
        return True
    return False


def create_channel(values):
    func = 'create_channel'
    log.debug('func=%s|values=%s', func, values)
    channel_values = {}
    for key in Channel.KEYS:
        value = values.get(key)
        if value not in INVALID_VALUE:
            channel_values[key] = value
        else:
            log.debug('ignore key=%s|value=%s', key, value)
    ret = Channel.create(channel_values)
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

    user_value = {}
    profile_value = {}

    for key, value in values.iteritems():
        if value not in INVALID_VALUE:
            if key in User.KEYS:
                user_value[key] = value
            if key in Profile.KEYS:
                profile_value[key] = value
        else:
            log.debug('ingore key=%s', key)

    user = User(merchant_id)
    user.update(user_value)

    profile = Profile(merchant_id)
    profile.update(profile_value)


def build_user(values):
    func='build_user'
    log.debug('func=%s|input=%s', func, values)
    user = {}
    now = datetime.datetime.now()

    for key in User.KEYS:
        value = values.get(key)
        if key in User.MUST_KEY.keys():
            if value not in INVALID_VALUE:
                user[key] = value
            else:
                if User.MUST_KEY.get(key) == T_INT:
                    user[key] = 0
                else:
                    user[key] = ''

        if key in User.OPTION_KEY.keys():
            if value not in INVALID_VALUE:
                user[key] = value

        for key in User.DATETIME_KEY.keys():
            if User.DATETIME_KEY.get(key) == 'date':
                user[key] = now.strftime('%Y-%m-%d')
            if User.DATETIME_KEY.get(key) == 'datetime':
                user[key] = now.strftime('%Y-%m-%d %H:%M:%S')

    user['state'] = REGISTER_STATE
    user['is_active'] = DEFAULT_ACTIVE
    user['password'] = gen_passwd(values.get('mobile')[-6:])

    log.debug('func=%s|output=%s', func, user)
    return user


def build_profile(values):
    # 添加其它数据
    func = 'build_profile'
    log.debug('func=%s|input=%s', func, values)

    profile = {}
    now = datetime.datetime.now()

    for key in Profile.KEYS:
        value = values.get(key)
        if key in Profile.MUST_KEY.keys():
            if value not in INVALID_VALUE:
                profile[key] = value
            else:
                if Profile.MUST_KEY.get(key) == T_INT:
                    profile[key] = 0
                else:
                    profile[key] = ''

        if key in Profile.OPTION_KEY.keys():
            if value not in INVALID_VALUE:
                profile[key] = value

        for key in Profile.DATETIME_KEY.keys():
            if Profile.DATETIME_KEY.get(key) == 'date':
                profile[key] = now.strftime('%Y-%m-%d')
            if Profile.DATETIME_KEY.get(key) == 'datetime':
                profile[key] = now.strftime('%Y-%m-%d %H:%M:%S')

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


def build_card_bin(params):
    data = {}
    for key in CardBin.CARDBIN_MUST_KEY:
        data[key] = params.get(key, '')

    for key in CardBin.CARDBIN_OPTION_KEY:
        if key == '`foreign`':
            data[key] = params.get('foreign')
        else:
            data[key] = params.get(key, '')
    return data


def build_channel_bind_edit(params):
    values = {}
    for key in ChannelBind.KEYS:
        value = params.get(key)
        if value not in INVALID_VALUE:
            values[key] = value
        else:
            if key in ChannelBind.MUST_KEY:
                if ChannelBind.MUST_KEY.get(key) == T_INT:
                    values[key] = 0
                if ChannelBind.MUST_KEY.get(key) == T_STR:
                    values[key] = ''
            else:
                log.debug('ignore key=%s|value=%s', key, value)
    now = datetime.datetime.now()
    values['update_time'] = now.strftime('%Y-%m-%d %H:%M:%S')
    return values


def build_channel_bind_create(params):
    data = {}
    now = datetime.datetime.now()

    for key in ChannelBind.KEYS:
        value = params.get(key)
        if value not in INVALID_VALUE:
            data[key] = value
        else:
            if key in ChannelBind.MUST_KEY:
                if ChannelBind.MUST_KEY.get(key) == T_INT:
                    data[key] = 0
                if ChannelBind.MUST_KEY.get(key) == T_STR:
                    data[key] = ''
            else:
                log.debug('ignore key=%s|value=%s', key, value)

    data['create_time'] = now.strftime('%Y-%m-%d %H:%M:%S')
    return data


def build_terminal_edit(params):
    data = {}
    for key in params.keys():
        if key in Terminal.TERMINAL_MUST_KEY.keys():
            if params.get(key):
                data[key] = params.get(key)
            else:
                if Terminal.TERMINAL_MUST_KEY.get(key) == T_INT:
                    data[key] = 0
                elif Terminal.TERMINAL_MUST_KEY.get(key) == T_STR:
                    data[key] = ''
                else:
                    log.info('build_terminal_edit key=%s|cannot find type', key)

        if key in Terminal.TERMINAL_OPTION_KEY.keys() and params.get(key):
            data[key] = params.get(key)

        if key == 'last_modify':
            now = datetime.datetime.now()
            data[key] = now.strftime('%Y-%m-%d %H:%M:%S')

    return data


def build_terminal_create(params):
    data = {}
    for key in Terminal.TERMINAL_KEY:
        if key in Terminal.TERMINAL_MUST_KEY.keys():
            if params.get(key):
                data[key] = params.get(key)
            else:
                if Terminal.TERMINAL_MUST_KEY.get(key) == T_INT:
                    data[key] = 0
                elif Terminal.TERMINAL_MUST_KEY.get(key) == T_STR:
                    data[key] = ''
                else:
                    log.info('build_terminal_create key=%s|cannot find type', key)

        if key in Terminal.TERMINAL_OPTION_KEY.keys() and params.get(key):
            data[key] = params.get(key)

        if key == 'last_modify':
            now = datetime.datetime.now()
            data[key] = now.strftime('%Y-%m-%d %H:%M:%S')

    return data

def build_termbind_edit(params):
    data = {}
    for key in params.keys():
        if key in TermBind.TERMBIND_MUST_KEY.keys():
            if params.get(key) not in INVALID_VALUE:
                data[key] = params.get(key)
            else:
                if TermBind.TERMBIND_MUST_KEY.get(key) == T_INT:
                    data[key] = 0
                elif TermBind.TERMBIND_MUST_KEY.get(key) == T_STR:
                    data[key] = ''
                else:
                    log.info('build_termbind_edit key=%s|cannot find default value', key)

        if key in TermBind.TERMBIND_OPTION_KEY.keys():
            if params.get(key):
                data[key] = params.get(key)

    return data


def build_termbind_create(params):
    data = {}
    for key in TermBind.TERMBIND_KEY:
        if key in TermBind.TERMBIND_MUST_KEY.keys():
            if params.get(key) not in INVALID_VALUE:
                data[key] = params.get(key)
            else:
                if TermBind.TERMBIND_MUST_KEY.get(key) == T_INT:
                    data[key] = 0
                elif TermBind.TERMBIND_MUST_KEY.get(key) == T_STR:
                    data[key] = ''
                else:
                    log.info('build_termbind_create key=%s|cannot find default value', key)

        if key in TermBind.TERMBIND_OPTION_KEY.keys():
            if params.get(key):
                data[key] = params.get(key)

    return data
