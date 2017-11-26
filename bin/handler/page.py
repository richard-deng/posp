# coding: utf-8
from zbase.web import core
from zbase.web import template
from posp_base.session import posp_check_session_for_page
from config import cookie_conf
from runtime import g_rt

import logging

log = logging.getLogger()


class Root(core.Handler):
    def GET(self):
        self.redirect('/posp/v1/page/login.html')


class Login(core.Handler):
    def GET(self):
        self.write(template.render('login.html'))


class Merchant(core.Handler):
    @posp_check_session_for_page(g_rt.redis_pool, cookie_conf)
    def GET(self):
        self.write(template.render('merchant.html'))


class Channel(core.Handler):
    @posp_check_session_for_page(g_rt.redis_pool, cookie_conf)
    def GET(self):
        self.write(template.render('channel.html'))


class ChannelBind(core.Handler):
    @posp_check_session_for_page(g_rt.redis_pool, cookie_conf)
    def GET(self):
        self.write(template.render('chnlbind.html'))


class CardBin(core.Handler):
    @posp_check_session_for_page(g_rt.redis_pool, cookie_conf)
    def GET(self):
        self.write(template.render('cardbin.html'))


class Terminal(core.Handler):
    @posp_check_session_for_page(g_rt.redis_pool, cookie_conf)
    def GET(self):
        self.write(template.render('terminal.html'))


class TerminalBind(core.Handler):
    @posp_check_session_for_page(g_rt.redis_pool, cookie_conf)
    def GET(self):
        self.write(template.render('termbind.html'))

class TradeList(core.Handler):
    @posp_check_session_for_page(g_rt.redis_pool, cookie_conf)
    def GET(self):
        self.write(template.render('trade.html'))