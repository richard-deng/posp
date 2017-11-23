# coding: utf-8

from handler import (
    ping,
    page,
    login,
    channel,
    cardbin,
    merchant,
    chnlbind,
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

    # 商户通道绑定
    ('^/posp/v1/api/channel/bind/list$', chnlbind.ChannelBindListHandler),
    ('^/posp/v1/api/channel/bind/view$', chnlbind.ChannelBindViewHandler),
    ('^/posp/v1/api/channel/bind/create$', chnlbind.ChannelBindCreateHandler),
    ('^/posp/v1/api/channel/bind/switch$', chnlbind.ChannelBindSwitchHandler),

    # 卡表
    ('^/posp/v1/api/card/list$', cardbin.CardBinListHandler),
    ('^/posp/v1/api/card/view$', cardbin.CardBinViewHandler),
    ('^/posp/v1/api/card/create$', cardbin.CardBinCreateHandler),

    # 页面
    ('^/$', page.Root),
    ('^/posp/v1/page/login.html$', page.Login),
    ('^/posp/v1/page/merchant.html', page.Merchant),
    ('^/posp/v1/page/channel.html', page.Channel),
    ('^/posp/v1/page/channel/bind.html', page.ChannelBind),
    ('^/posp/v1/page/cardbin.html', page.CardBin),

)
