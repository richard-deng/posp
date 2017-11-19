# coding: utf-8
from zbase.web import core
from zbase.web import template
from posp_base.session import posp_check_session_for_page
from config import cookie_conf
from runtime import g_rt

import logging

log = logging.getLogger()


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