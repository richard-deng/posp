# coding: utf-8
import logging
import datetime

from runtime import g_rt
from config import cookie_conf
from base_handler import BaseHandler
from posp_base.response import error, success, RESP_CODE
from posp_base.session import posp_check_session
from posp_base.trade import TradeList
from posp_base.tools import trans_time
from zbase.web.validator import (
    with_validator_self, Field, T_REG, T_INT, T_STR
)


log = logging.getLogger()


class TradeListHandler(BaseHandler):

    _get_handler_fields = [
        Field('page', T_INT, False),
        Field('maxnum', T_INT, False),
        Field('syssn', T_STR, True),
        Field('userid', T_INT, True),
        Field('start_time', T_STR, True),
        Field('end_time', T_STR, True),
    ]

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _get_handler(self):
        data = {}
        params = self.validator.data
        syssn = params.get('syssn')
        start_time = params.get('start_time')
        end_time = params.get('end_time')

        if syssn:
            flag, info, num = TradeList.page_syssn(syssn)

        elif start_time and end_time:
            table_arr = TradeList._gen_tables(start_time, end_time)
            table_arr = TradeList._gen_valid_tables(table_arr)
            if len(table_arr) > 1:
                flag, info, num = TradeList.page_more(**params)
            else:
                flag, info, num = TradeList.page(table=table_arr[0], **params)
        else:
            # 默认当月
            now = datetime.datetime.now()
            table = 'record_' + now.strftime('%Y%m')
            flag, info, num = TradeList.page(table=table, **params)

        if not flag:
            return error(RESP_CODE.DATAERR)
        data['num'] = num
        data['info'] = [trans_time(item, TradeList.DATETIME_KEY) for item in info]
        return success(data=data)


class TradeListViewHandler(BaseHandler):

    _get_handler_fields = [
        Field('syssn', T_STR, False)
    ]

    @posp_check_session(g_rt.redis_pool, cookie_conf)
    @with_validator_self
    def _get_handler(self):
        params = self.validator.data
        syssn = params.get('syssn')
        trade = TradeList(syssn)
        trade.load()
        return success(data=trade.data)
