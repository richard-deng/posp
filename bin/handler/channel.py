# coding: utf-8
import logging
import traceback

import tools
from runtime import g_rt
from config import cookie_conf
from base_handler import BaseHandler
from zbase.base.dbpool import with_database
from posp_base.response import error, success, RESP_CODE
from posp_base.session import posp_check_session
from zbase.web.validator import (
    with_validator_self, Field, T_REG, T_INT, T_STR
)


log = logging.getLogger()


class ChannelListHandler(BaseHandler):

    _get_handler_fields = [
        Field('page', T_INT, False),
        Field('maxnum', T_INT, False),
        Field('name', T_STR, True),
    ]

    @with_database('posp_core')
    def _query_handler(self, page, page_size, name=''):
        where = {}
        other = ''
        if name not in ('', None):
            where['name'] = name

        keep_fields = [
            'id', 'name', 'zmk', 'zpk', 'mcc', 'chcd', 'inscd', 'code', 'regioncd',
            'mchntid', 'mchntnm', 'terminalid', 'mode', 'parent', 'route', 'available',
            'tdkey', 'mackey',
        ]
        sql = self.db.select_sql(table='channel', where=where, fields=keep_fields, other=other)
        pager = self.db.select_page(sql, pagecur=page, pagesize=page_size)
        pager.split()
        return pager.pagedata.data, pager.count

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _get_handler(self):
        data = {}
        params = self.validator.data
        name = params.get('name', '')
        curr_page = params.get('page')
        max_page_num = params.get('maxnum')
        info, num = self._query_handler(page=curr_page, page_size=max_page_num, name=name)
        data['info'] = info
        data['num'] = num
        return success(data=data)


class ChannelNameHandler(BaseHandler):

    def _query_handler(self):
        ret = tools.get_channel_names()
        return ret

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _get_handler(self):
        data = self._query_handler()
        return success(data=data)


class ChannelSwitchHandler(BaseHandler):

    _post_handler_fields = [
        Field('channel_id', T_INT, False),
        Field('state', T_INT, False),
    ]

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _post_handler(self):
        try:
            params = self.validator.data
            flag = tools.change_channel_state(params['channel_id'], params['state'])
            if flag:
                return success(data={})
            else:
                return error(RESP_CODE.DATAERR)
        except Exception as e:
            log.warn(traceback.format_exc())
            return error(RESP_CODE.SERVERERR)


class ChannelViewHandler(BaseHandler):

    _get_handler_fields = [
        Field('channel_id', T_INT, False),
    ]

    _post_handler_fields = [
        Field('channel_id', T_INT, False),
        Field('name', T_STR, False),
        Field('zmk', T_STR, False),
        Field('zpk', T_STR, False),
        # Field('mcc', T_STR, False),
        Field('chcd', T_STR, False),
        Field('inscd', T_STR, False),
        Field('code', T_STR, False),
        Field('mchntid', T_STR, False),
        Field('mchntnm', T_STR, False),
        # Field('terminalid', T_STR, False),
        # Field('mode', T_STR, False),
        # Field('parent', T_STR, False),
        Field('route', T_STR, False),
        Field('available', T_STR, False),
        Field('tdkey', T_STR, False),
        Field('mackey', T_STR, False),
    ]

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _get_handler(self):
        try:
            params = self.validator.data
            data = tools.get_channel(channel_id=params['channel_id'])
            return success(data=data)
        except Exception:
            log.warn(traceback.format_exc())
            return error(RESP_CODE.SERVERERR)

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _post_handler(self):
        try:
            params = self.validator.data
            channel_id = params.pop('channel_id')
            values = params
            flag = tools.update_channel(channel_id=channel_id, values=values)
            if flag:
                return success(data={})
            return error(RESP_CODE.DATAERR)
        except Exception:
            log.warn(traceback.format_exc())
            return error(RESP_CODE.SERVERERR)


class ChannelCreateHandler(BaseHandler):

    _post_handler_fields = [
        Field('name', T_STR, False),
        Field('zmk', T_STR, False),
        Field('zpk', T_STR, False),
        # Field('mcc', T_STR, False),
        Field('chcd', T_STR, False),
        Field('inscd', T_STR, False),
        Field('code', T_STR, False),
        Field('mchntid', T_STR, False),
        Field('mchntnm', T_STR, False),
        #Field('terminalid', T_STR, False),
        #Field('mode', T_STR, False),
        #Field('parent', T_STR, False),
        Field('route', T_STR, False),
        Field('available', T_STR, False),
        Field('tdkey', T_STR, False),
        Field('mackey', T_STR, False),
    ]

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _post_handler(self):
        try:
            params = self.validator.data
            values = params
            flag = tools.create_channel(values=values)
            if flag:
                return success(data={})
            return error(RESP_CODE.DATAERR)
        except Exception:
            log.warn(traceback.format_exc())
            return error(RESP_CODE.SERVERERR)