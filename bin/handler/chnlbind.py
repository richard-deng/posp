# coding: utf-8
import logging
import traceback

import tools
from runtime import g_rt
from config import cookie_conf
from base_handler import BaseHandler
from posp_base.response import error, success, RESP_CODE
from posp_base.session import posp_check_session
from posp_base.chnlbind import ChannelBind
from posp_base.merchant import User
from zbase.web.validator import (
    with_validator_self, Field, T_REG, T_INT, T_STR
)


log = logging.getLogger()


class ChannelBindListHandler(BaseHandler):

    _get_handler_fields = [
        Field('page', T_INT, False),
        Field('maxnum', T_INT, False),
    ]

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _get_handler(self):
        data = {}
        params = self.validator.data
        info, num = ChannelBind.page(**params)
        data['info'] = info
        data['num'] = num
        return success(data=data)


class ChannelBindViewHandler(BaseHandler):

    _get_handler_fields = [
        Field('channel_bind_id', T_INT, False)
    ]

    _post_handler_fields = [
        Field('channel_bind_id', T_INT, False),

        Field('priority', T_INT, False),
        Field('chnlid', T_INT, False),
        Field('mchntid', T_STR, False),
        Field('termid', T_STR, False),
        Field('mchntnm', T_STR, False),
        Field('mcc', T_STR, False),
        Field('tradetype', T_INT, False),
        Field('tag1', T_STR, False),
        Field('tag2', T_STR, False),
        Field('key1', T_STR, False),
        Field('key2', T_STR, False),
        Field('key3', T_STR, False),
        Field('available', T_INT, False),
    ]

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _get_handler(self):
        params = self.validator.data
        channel_bind_id = params.get('channel_bind_id')
        bind = ChannelBind(channel_bind_id)
        bind.load()
        data = bind.data
        return success(data=data)

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _post_handler(self):
        params = self.validator.data
        channel_bind_id = params.pop('channel_bind_id')
        values = tools.build_channel_bind_edit(params)
        bind = ChannelBind(channel_bind_id)
        ret = bind.update(values)
        if ret == 1:
            return success(data={})
        return error(RESP_CODE.DATAERR)


class ChannelBindCreateHandler(BaseHandler):

    _post_handler_fields = [
        Field('userid', T_INT, False),
        Field('priority', T_INT, False),
        Field('chnlid', T_INT, False),
        Field('mchntid', T_STR, False),
        Field('termid', T_STR, False),
        Field('mchntnm', T_STR, False),
        Field('mcc', T_STR, False),
        Field('tradetype', T_INT, False),
        Field('tag1', T_STR, False),
        Field('tag2', T_STR, False),
        Field('key1', T_STR, False),
        Field('key2', T_STR, False),
        Field('key3', T_STR, False),
        Field('available', T_INT, False),
    ]

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _post_handler(self):
        params = self.validator.data
        userid = params.get('userid')
        user = User(userid)
        user.load()
        if not user.data:
            log.info('ChannelBindCreateHandler|userid=%s|invalid', userid)
        values = tools.build_channel_bind_create(params)
        ret = ChannelBind.create(values)
        if ret == 1:
            return success(data={})
        return error(RESP_CODE.DATAERR)
