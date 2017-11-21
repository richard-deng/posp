# coding: utf-8
import logging
import traceback

import tools
from runtime import g_rt
from config import cookie_conf
from base_handler import BaseHandler
from posp_base.response import error, success, RESP_CODE
from posp_base.session import posp_check_session
from posp_base.cardbin import CardBin
from zbase.web.validator import (
    with_validator_self, Field, T_REG, T_INT, T_STR
)


log = logging.getLogger()


class CardBinListHandler(BaseHandler):

    _get_handler_fields = [
        Field('page', T_INT, False),
        Field('maxnum', T_INT, False),
        Field('bankname', T_STR, True),
        Field('bankid', T_STR, True),
        Field('cardbin', T_STR, True),
        Field('cardname', T_STR, True),
    ]

    def _query_handler(self, params):
        info, num = CardBin.page(**params)
        return info, num

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _get_handler(self):
        data = {}
        params = self.validator.data
        info, num = self._query_handler(params)
        data['info'] = info
        data['num'] = num
        return success(data=data)


class CardBinViewHandler(BaseHandler):

    _get_handler_fields = [
        Field('card_bin_id', T_INT, False),
    ]

    _post_handler_fields = [
        Field('card_bin_id', T_INT, False),
        Field('bankname', T_STR, False),
        Field('bankid', T_STR, False),
        Field('cardlen', T_INT, False),
        Field('cardbin', T_STR, False),
        Field('cardname', T_STR, False),
        Field('cardtp', T_INT, False),
        Field('foreign', T_INT, False),
    ]

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _get_handler(self):
        params = self.validator.data
        card_bin_id = params.get('card_bin_id')
        card = CardBin(card_bin_id)
        card.load()
        data = card.data
        return success(data=data)

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _post_handler(self):
        params = self.validator.data
        card_bind_id = params.get('card_bin_id')
        values = tools.build_card_bin(params)
        card = CardBin(card_bind_id)
        ret = card.update(values)
        return success(data={})



