# coding: utf-8
import logging

import tools
from runtime import g_rt
from config import cookie_conf
from base_handler import BaseHandler
from posp_base.response import error, success, RESP_CODE
from posp_base.session import posp_check_session
from posp_base.termbind import TermBind
from posp_base.merchant import User
from posp_base.terminal import Terminal
from posp_base.tools import trans_time
from zbase.web.validator import (
    with_validator_self, Field, T_REG, T_INT, T_STR
)

log = logging.getLogger()


class TermBindListHandler(BaseHandler):

    _get_handler_fields = [
        Field('page', T_INT, False),
        Field('maxnum', T_INT, False),
        Field('userid', T_STR, True),
        Field('terminalid', T_STR, True),
    ]

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _get_handler(self):
        data = {}
        params = self.validator.data
        info, num = TermBind.page(**params)
        data['num'] = num
        data['info'] = [trans_time(item, TermBind.DATETIME_KEY) for item in info]
        return success(data=data)


class TermBindViewHandler(BaseHandler):

    _get_handler_fields = [
        Field('termbind_id', T_INT, False)
    ]

    _post_handler_fields = [
        Field('termbind_id', T_INT, False),

        Field('userid', T_INT, False),
        Field('terminalid', T_STR, False),
        Field('pinkey1', T_STR, True),
        Field('pinkey2', T_STR, True),
        Field('mackey', T_STR, True),
        Field('state', T_INT, True),
        Field('qpos_pubkey', T_STR, True),
        Field('tmk', T_STR, True),
    ]

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _get_handler(self):
        params = self.validator.data
        termbind_id = params.get('termbind_id')
        termbind = TermBind(termbind_id)
        termbind.load()
        return success(data=termbind.data)

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _post_handler(self):
        params = self.validator.data
        termbind_id = params.pop('termbind_id')
        termbind = TermBind(termbind_id)
        values = tools.build_termbind_edit(params)
        termbind.update(values)
        return success(data={})


class TermBindCreateHandler(BaseHandler):

    _post_handler_fields = [
        Field('userid', T_INT, False),
        Field('terminalid', T_STR, False),
        Field('pinkey1', T_STR, True),
        Field('pinkey2', T_STR, True),
        Field('mackey', T_STR, True),
        Field('qpos_pubkey', T_STR, True),
        Field('tmk', T_STR, True),
        # Field('active_date', T_STR, True),
    ]

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _post_handler(self):
        params = self.validator.data

        # 判断userid
        userid = params.get('userid')
        user = User(userid)
        user.load()
        if not user.data:
            log.info('userid=%s|invalid', userid)
            return error(RESP_CODE.DATAERR)

        # 判断terminalid
        terminalid = params.get('terminalid')
        terminal = Terminal.load_by_terminalid(terminalid)
        if not terminal.data:
            log.info('terminalid=%s|invalid', terminalid)
            return error(RESP_CODE.DATAERR)

        values = tools.build_termbind_create(params)
        ret = TermBind.create(values)
        if ret == 1:
            return success(data={})
        return error(RESP_CODE.DATAERR)
