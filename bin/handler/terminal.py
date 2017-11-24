# coding: utf-8
import logging

import tools
from runtime import g_rt
from config import cookie_conf
from base_handler import BaseHandler
from posp_base.response import error, success, RESP_CODE
from posp_base.session import posp_check_session
from posp_base.terminal import Terminal
from posp_base.tools import trans_time
from zbase.web.validator import (
    with_validator_self, Field, T_REG, T_INT, T_STR
)


log = logging.getLogger()


class TerminalListHandler(BaseHandler):

    _get_handler_fields = [
        Field(key, tp, True) for key, tp in Terminal.QUERY_KEY
    ].append([
        Field('page', T_INT, False),
        Field('maxnum', T_INT, False)
    ])

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _get_handler(self):
        data = {}
        params = self.validator.data
        info, num = Terminal.page(**params)
        data['num'] = num
        data['info'] = [trans_time(item, Terminal.TERMINAL_DATETIME_KEY) for item in info]
        return success(data=data)


class TerminalViewHandler(BaseHandler):

    _get_handler_fields = [
        Field('terminal_id', T_INT, False)
    ]

    _post_handler_fields = [
        Field('terminal_id', T_INT, False),

        Field('terminalid', T_STR, False),
        Field('psamid', T_STR, False),
        Field('producer', T_STR, False),
        Field('model', T_STR, False),
        Field('product_date', T_STR, False),
        Field('deliver_date', T_STR, True),
        Field('tck', T_STR, False),
        Field('used', T_INT, False),
        Field('state', T_INT, False),
        Field('qpos_pubkey', T_STR, False),
    ]

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _get_handler(self):
        params = self.validator.data
        terminal_id = params.get('terminal_id')
        terminal = Terminal(terminal_id)
        terminal.load()
        return success(data=terminal.data)

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _post_handler(self):
        params = self.validator.data
        terminal_id = params.pop('terminal_id')
        terminal = Terminal(terminal_id)
        values = tools.build_terminal_edit(params)
        ret = terminal.update(values)
        if ret == 1:
            return success(data={})
        return error(RESP_CODE.DATAERR)


class TerminalCreateHandle(BaseHandler):

    _post_handler_fields = [
        Field('terminalid', T_STR, False),
        Field('psamid', T_STR, False),
        Field('producer', T_STR, False),
        Field('model', T_STR, False),
        Field('product_date', T_STR, False),
        Field('deliver_date', T_STR, True),
        Field('tck', T_STR, False),
        Field('used', T_INT, False),
        Field('state', T_INT, False),
        Field('qpos_pubkey', T_STR, False),
        Field('advice', T_STR, True),
    ]

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _post_handler(self):
        params = self.validator.data

        terminal_id = params.get('terminal_id')
        terminal = Terminal(terminal_id)
        terminal.load()
        if terminal.data:
            return error(RESP_CODE.DATAEXIST)

        values = tools.build_terminal_create(params)
        ret = Terminal.create(values)
        if ret == 1:
            return success(data={})
        return error(RESP_CODE.DATAERR)
