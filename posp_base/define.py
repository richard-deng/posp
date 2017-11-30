# coding:utf-8

class DATETIMEException(Exception):
    pass

POSP_OP_OK = 0
POSP_OP_ERR = -1


#用户状态
# 2 通过审核，未设备激活
POSP_USER_STATE_VERIFIED = 2
# 3 已设备激活，未业务激活
POSP_USER_STATE_ACTIVE = 3
# 4 已业务激活，正常
POSP_USER_STATE_OK = 4

POSP_USER_STATE_MAP = {
    POSP_USER_STATE_VERIFIED: '设备未激活',
    POSP_USER_STATE_ACTIVE: '设备已激活，未激活业务',
    POSP_USER_STATE_OK: '业务已激活'
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

# 银行卡类型
BANK_CARD_MAP = {
    '00': '未识别卡',
    '01': '借记卡',
    '02': '信用卡(贷记卡)',
    '03': '准贷记卡',
    '04': '储值卡'
}

FOREIGN_MAP = {
    '0': '国内',
    '1': '国外',
}
