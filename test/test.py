# -*- coding: utf-8 -*-
import json
import hashlib
import unittest
from zbase.base import logger
from zbase.base.http_client import RequestsClient
from zbase.server.client import HttpClient

log = logger.install('stdout')


class TestPospInstrument(unittest.TestCase):
    def setUp(self):
        self.url = ''
        self.send = {'se_userid': 88769}
        self.host = '127.0.0.1'
        self.port = 8084
        self.timeout = 2000
        self.server = [{'addr': (self.host, self.port), 'timeout': self.timeout}, ]
        self.client = HttpClient(self.server, client_class=RequestsClient)
        self.headers = {'sessionid': 'ea74f0cb-8f38-4325-88bf-1669314285be'}
        self.cookie = self.headers

    @unittest.skip("skipping")
    def test_login(self):
        password = '123456'
        md5_password = hashlib.md5(password).hexdigest()
        self.url = '/posp/v1/api/login'
        self.send = {
            "mobile": "13802438716",
            "password": md5_password
        }
        ret = self.client.post(self.url, self.send)
        log.info(ret)
        print '--headers--'
        print self.client.client.headers
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_logout(self):
        self.url = '/posp/v1/api/logout'
        ret = self.client.get(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_merchant_list(self):
        self.url = '/posp/v1/api/merchant/list'
        self.send.update({
            'page': 1,
            'maxnum': 10
        })
        ret = self.client.get(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_merchant_view(self):
        self.url = '/posp/v1/api/merchant/view'
        self.send.update({
            'merchant_id': 10000
        })
        ret = self.client.get(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_merchant_create(self):
        self.url = '/posp/v1/api/merchant/create'
        self.send.update({
            'mobile': '13802438725',
            'name': '测试8725',
            'email': '13802438725@qq.com',
        })
        ret = self.client.post(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_channel_list(self):
        self.url = '/posp/v1/api/channel/list'
        self.send.update({
            'page': 1,
            'maxnum': 10
        })
        ret = self.client.get(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_channel_view(self):
        self.url = '/posp/v1/api/channel/view'
        self.send.update({
            'channel_id': 1
        })
        ret = self.client.get(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_channel_names(self):
        self.url = '/posp/v1/api/channel/names'
        ret = self.client.get(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_channel_switch_state(self):
        self.url = '/posp/v1/api/channel/state/change'
        self.send.update({
            'channel_id': 1,
            'state': 0
        })
        ret = self.client.post(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_channel_create(self):
        self.url = '/posp/v1/api/channel/create'
        self.send.update({
            'name': '测试通道20171201'
        })
        ret = self.client.post(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_card_bin_list(self):
        self.url = '/posp/v1/api/card/list'
        self.query = {
            'page': 2,
            'maxnum': 10,
            'bankname': '邮储银行',
        }
        self.send.update(self.query)
        ret = self.client.get(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_get_card_bin(self):
        self.url = '/posp/v1/api/card/view'
        self.query = {
            'card_bin_id': 7384
        }
        self.send.update(self.query)
        ret = self.client.get(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_edit_card_bin(self):
        self.url = '/posp/v1/api/card/view'
        self.send.update({
            'card_bin_id': 7384,
            'bankname': '测试',
            'bankid': '111111',
            'cardlen': 12,
            'cardbin': '123456',
            'cardname': '测试卡',
            'cardtp': 1,
            'foreign': 0,
        })
        ret = self.client.post(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_create_card_bin(self):
        self.url = '/posp/v1/api/card/create'
        self.send.update({
            'bankname': '测试2',
            'bankid': '222222',
            'cardlen': 12,
            'cardbin': '222222',
            'cardname': '测试卡2',
            'cardtp': 1,
            'foreign': 0,
        })
        ret = self.client.post(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_channel_bind_list(self):
        self.url = '/posp/v1/api/channel/bind/list'
        self.send.update({
            'page': 1,
            'maxnum': 5,
        })
        ret = self.client.get(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_get_channel_bind(self):
        self.url = '/posp/v1/api/channel/bind/view'
        self.send.update({
            'channel_bind_id': 1
        })
        ret = self.client.get(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_edit_channel_bind(self):
        self.url = '/posp/v1/api/channel/bind/view'
        self.send.update({
            'channel_bind_id': 465772,
            'priority': 1,
            'chnlid': 1,
            'mchntid': '222222',
            'mchntnm': '测试商户名称',
            'termid': '1001',
            'mcc': '测试MCC',
            'tradetype': 1,
            'tag1': 'tag1_test',
            'tag2': 'tag2_test',
            'key1': 'key1_test',
            'key2': 'key2_test',
            'key3': 'key3_test',
            'available': 1,
        })
        ret = self.client.post(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_create_channel_bind(self):
        self.url = '/posp/v1/api/channel/bind/create'
        self.send.update({
            'userid': 287548,
            'priority': 1,
            'chnlid': 1,
            'mchntid': '11111',
            'mchntnm': '测试商户名称',
            'termid': '1001',
            'mcc': '测试MCC',
            'tradetype': 1,
            'tag1': 'tag1_test',
            'tag2': 'tag2_test',
            'key1': 'key1_test',
            'key2': 'key2_test',
            'key3': 'key3_test',
            'available': 1,
        })
        ret = self.client.post(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_switch_channel_bind_available(self):
        self.url = '/posp/v1/api/channel/bind/switch'
        self.send.update({
            'channel_bind_id': 1,
            'available': 1,
        })
        ret = self.client.post(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_terminal_list(self):
        self.url = '/posp/v1/api/terminal/list'
        self.send.update({
            'page': 1,
            'maxnum': 10
        })
        ret = self.client.get(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_terminal_view(self):
        self.url = '/posp/v1/api/terminal/view'
        self.send.update({
            'terminal_table_id': 27000
        })
        ret = self.client.get(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_terminal_create(self):
        self.url = '/posp/v1/api/terminal/create'
        self.send.update({
            'terminalid': '201712011531'
        })
        ret = self.client.post(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_terminal_bind_list(self):
        self.url = '/posp/v1/api/terminal/bind/list'
        self.send.update({
            'page': 1,
            'maxnum': 10
        })
        ret = self.client.get(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_terminal_bind_view(self):
        self.url = '/posp/v1/api/terminal/bind/view'
        self.send.update({
            'termbind_id': 767
        })
        ret = self.client.get(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_terminal_bind_create(self):
        self.url = '/posp/v1/api/terminal/bind/create'
        self.send.update({
            'userid': 10000,
            'terminalid': '201712011531'
        })
        ret = self.client.post(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_trade_list(self):
        self.url = '/posp/v1/api/trade/list'
        self.send.update({
            'page': 1,
            'maxnum': 10,
            'start_time': '2017-09-01 00:00:00',
            'end_time': '2017-09-30 23:59:59'
        })
        ret = self.client.get(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')

    @unittest.skip("skipping")
    def test_trade_view(self):
        self.url = '/posp/v1/api/trade/view'
        self.send.update({
            'syssn': '20170925586205'
        })
        ret = self.client.get(self.url, self.send, cookies=self.cookie)
        log.info(ret)
        respcd = json.loads(ret).get('respcd')
        self.assertEqual(respcd, '0000')


suite = unittest.TestLoader().loadTestsFromTestCase(TestPospInstrument)
unittest.TextTestRunner(verbosity=2).run(suite)
