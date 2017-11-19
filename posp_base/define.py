# coding:utf-8

POSP_OP_OK = 0
POSP_OP_ERR = -1


#用户状态
#正常
POSP_USER_STATE_OK = 3
#封禁
POSP_USER_STATE_FORBIDDEN = 4
#注销
POSP_USER_STATE_CANCEL = 5
POSP_USER_STATE_MAP = {
    POSP_USER_STATE_OK: '正常',
    POSP_USER_STATE_FORBIDDEN: '封禁',
    POSP_USER_STATE_CANCEL: '注销'
}