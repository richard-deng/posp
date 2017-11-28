# coding: utf-8

import tools
import logging
import traceback

from runtime import g_rt
from config import cookie_conf
from base_handler import BaseHandler
from constant import INVALID_VALUE
from zbase.base.dbpool import with_database
from posp_base.response import error, success, RESP_CODE
from posp_base.session import posp_check_session
from zbase.web.validator import (
    with_validator_self, Field, T_REG, T_INT, T_STR
)

log = logging.getLogger()


class MerchantListHandler(BaseHandler):

    _get_handler_fields = [
        Field('page', T_INT, False),
        Field('maxnum', T_INT, False),
        Field('mobile', T_STR, True),
        Field('merchant_id', T_STR, True),
    ]

    @with_database('posp_core')
    def _query_handler(self, page, page_size, mobile=None, merchant_id=None):
        where = {}
        other = ''
        on = {'auth_user.id': 'profile.userid'}
        if mobile not in INVALID_VALUE:
            where['auth_user.mobile'] = mobile

        if merchant_id not in INVALID_VALUE:
            where['auth_user.id'] = merchant_id

        keep_fields = [
            'auth_user.id', 'auth_user.state', 'auth_user.mobile',
            'auth_user.date_joined','profile.nickname', 'profile.name',
            'profile.mcc', 'profile.groupid', 'profile.idnumber',
        ]
        sql = self.db.select_join_sql(
            table1='auth_user',
            table2='profile',
            on=on,
            fields=keep_fields,
            where=where,
            other=other,
        )
        pager = self.db.select_page(sql, pagecur=page, pagesize=page_size)
        pager.split()
        return pager.pagedata.data, pager.count

    def _translate(self, data):
        for item in data:
            if item.get('date_joined'):
                item['date_joined'] = tools.trans_datetime(item['date_joined'])
        return data

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _get_handler(self):
        data = {}
        params = self.validator.data
        curr_page = params.get('page')
        max_page_num = params.get('maxnum')
        mobile = params.get('mobile')
        merchant_id = params.get('merchant_id')
        info, num = self._query_handler(
            page=curr_page, page_size=max_page_num,
            mobile=mobile, merchant_id=merchant_id
        )
        if info:
            info = self._translate(info)
        data['info'] = info
        data['num'] = num
        return success(data=data)


class MerchantViewHandler(BaseHandler):

    _get_handler_fields = [
        Field('merchant_id', T_INT, False),
    ]

    _post_handler_fields = [
        Field('merchant_id', T_INT, False),
        Field('mobile', T_STR, False),
        Field('email', T_STR, True),
        # Field('is_active', T_INT, False),
        # Field('state', T_INT, False),

        Field('name', T_STR, False),
        # Field('nickname', T_STR, False),
        Field('idnumber', T_STR, True),
        Field('province', T_STR, True),
        Field('city', T_STR, True),
        Field('bankname', T_STR, True),
        Field('bankuser', T_STR, True),
        Field('bankaccount', T_STR, True),
    ]

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _get_handler(self):
        try:
            params = self.validator.data
            merchant_id = params.get('merchant_id')
            data = tools.get_merchant(merchant_id)
            return success(data=data)
        except Exception:
            log.warn(traceback.format_exc())
            return error(RESP_CODE.SERVERERR)

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _post_handler(self):
        try:
            params = self.validator.data
            merchant_id = params.pop('merchant_id')
            values = params
            tools.update_merchant(merchant_id, values)
            return success(data={})
        except Exception:
            log.warn(traceback.format_exc())
            return error(RESP_CODE.SERVERERR)


class MerchantCreateHandler(BaseHandler):

    _post_handler_fields = [
        Field('mobile', T_STR, False),
        Field('email', T_STR, True),
        Field('password', T_STR, False),
        # Field('state', T_INT, False),
        # Field('is_active', T_INT, False),


        Field('name', T_STR, False),
        # Field('nickname', T_STR, False),
        Field('idnumber', T_STR, True),
        Field('province', T_STR, True),
        Field('city', T_STR, True),
        Field('bankname', T_STR, True),
        Field('bankuser', T_STR, True),
        Field('bankaccount', T_STR, True),
    ]

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _post_handler(self):
        params = self.validator.data

        # 是否已经注册
        mobile = params.get('mobile')
        ret = tools.find_user_by_mobile(mobile)
        if ret:
            return error(RESP_CODE.DATAEXIST, resperr='手机号已存在')

        flag, userid = tools.create_merchant(params)
        if flag:
            return success(data={'userid': userid})

        return error(RESP_CODE.DATAERR)
