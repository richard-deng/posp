# coding: utf-8
import logging

from runtime import g_rt
from config import cookie_conf
from config import ALLOW_LOGIN_MOBILE
from posp_base.merchant import User
from base_handler import BaseHandler
from posp_base.merchant import check_password
from posp_base.session import posp_set_cookie
from posp_base.session import posp_check_session
from posp_base.response import error, success, RESP_CODE
from posp_base.define import POSP_USER_STATE_OK
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
    def _post_handler(self):
        params = self.validator.data
        mobile = params['mobile']
        password = params["password"]
        if mobile not in ALLOW_LOGIN_MOBILE:
            log.info('mobile=%s forbidden', mobile)
            return error(RESP_CODE.USERFORBIDDEN)
        user = User.load_user_by_mobile(mobile)
        if user.data and user.userid:
            if user.data['state'] != POSP_USER_STATE_OK:
                log.info('userid=%s|state=%s|forbidden login', user.userid, user.data['state'])
                return error(RESP_CODE.USERSTATEERR)
            flag = check_password(password, user.data.get('password'))
            if not flag:
                return error(RESP_CODE.PWDERR)
            return success(data={'userid': user.userid})
        return error(RESP_CODE.DATAERR)


class LogoutHandler(BaseHandler):

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    def _get_handler(self):
        self.session.rm_session()
        self.resp.del_cookie('sessionid')
        return success(RESP_CODE.OK)
