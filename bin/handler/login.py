# coding: utf-8
import logging

from runtime import g_rt
from config import cookie_conf
from posp_base.merchant import User
from base_handler import BaseHandler
from posp_base.session import posp_set_cookie
from posp_base.response import error, success, RESP_CODE
from zbase.web.validator import (
    with_validator_self, Field, T_REG, T_INT, T_STR
)

log = logging.getLogger()


class LoginHandler(BaseHandler):

    _post_handler_fields = [
        Field('mobile', T_REG, False, match=r'^(1\d{10})$'),
        Field('password', T_STR, False),
    ]

    @posp_set_cookie(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _post_handler(self, *args):
        params = self.validator.data
        mobile = params['mobile']
        password = params["password"]
        user = User.load_user_by_mobile(mobile)
        if user.data and user.userid:
            return success(data={'userid': user.userid})
        return error(RESP_CODE.DATAERR)
