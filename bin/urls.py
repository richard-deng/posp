# coding: utf-8

from handler import (
    ping,
    page,
    login,
    channel,
    merchant,
)

urls = (
    # 接口
    ('^/ping$', ping.Ping),
    ('^/posp/v1/api/login$', login.LoginHandler),
    
    # 商户
    ('^/posp/v1/api/merchant/list$', merchant.MerchantListHandler),
    ('^/posp/v1/api/merchant/view$', merchant.MerchantViewHandler),
    ('^/posp/v1/api/merchant/create$', merchant.MerchantCreateHandler),

    # 通道
    ('^/posp/v1/api/channel/list$', channel.ChannelListHandler),
    ('^/posp/v1/api/channel/names$', channel.ChannelNameHandler),
    ('^/posp/v1/api/channel/state/change$', channel.ChannelSwitchHandler),
    ('^/posp/v1/api/channel/view$', channel.ChannelViewHandler),
    ('^/posp/v1/api/channel/create$', channel.ChannelCreateHandler),

    # 页面
    ('^/posp/v1/page/login.html$', page.Login),
    ('^/posp/v1/page/merchant.html', page.Merchant),
    ('^/posp/v1/page/channel.html', page.Channel),
)
