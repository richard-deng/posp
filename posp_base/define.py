# coding:utf-8

class DATETIMEException(Exception):
    pass

POSP_OP_OK = 0
POSP_OP_ERR = -1


#用户状态
# 1 未知, 2 绑定, 3 激活, 4 消费, 5 沉默, 6 黑名单, 7 封禁, 8 注销, 9 关闭
# 未知
POSP_USER_STATE_UNKNOWN = 1
# 绑定
POSP_USER_STATE_BIND = 2
# 激活
POSP_USER_STATE_OK = 3
# 消费
POSP_USER_STATE_CONSUME = 4
# 沉默
POSP_USER_STATE_SILENCE = 5
# 黑名单
POSP_USER_STATE_BLACKLIST = 6
# 封禁
POSP_USER_STATE_FORBIDDEN = 7
# 注销
POSP_USER_STATE_CANCEL = 8
# 关闭
POSP_USER_STATE_CLOSE = 9

POSP_USER_STATE_MAP = {
    POSP_USER_STATE_UNKNOWN: '未知',
    POSP_USER_STATE_BIND: '绑定',
    POSP_USER_STATE_OK: '激活',
    POSP_USER_STATE_CONSUME: '消费',
    POSP_USER_STATE_SILENCE: '沉默',
    POSP_USER_STATE_BLACKLIST: '黑名单',
    POSP_USER_STATE_FORBIDDEN: '封禁',
    POSP_USER_STATE_CANCEL: '注销',
    POSP_USER_STATE_CLOSE: '关闭',
}

# DB TOKEN
TOKEN_POSP_CORE = 'posp_core'
TOKEN_POSP_MIS = 'posp_mis'
TOKEN_POSP_TRADE = 'posp_trade'

# 终端激活
TERMINAL_ACTIVATE = 0
TERMINAL_UN_ACTIVATE = 1

# 终端绑定
TERMINAL_BIND = 0
TERMINAL_UN_BIND = 1

# 通道可用
CHANNEL_AVAILABLE = 1
CHANNEL_UN_AVAILABLE = 0

#银行卡类型
BANK_CARD_MAP = {
    '00': '未识别卡',
    '01': '借记卡',
    '02': '信用卡(贷记卡)',
    '03': '准贷记卡',
    '04': '储值卡'
}

