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
        self.headers = {'sessionid': '61ab563b-efd3-425c-ba2f-338a4042f604'}
        self.cookie = self.headers

    @unittest.skip("skipping")
    def test_login(self):
        self.url = '/posp/v1/api/login'
        self.send = {
            "mobile": "13802438716",
            "password": '123456'
        }
        ret = self.client.post(self.url, self.send)
        log.info(ret)
        print '--headers--'
        print self.client.client.headers
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

    #@unittest.skip("skipping")
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


suite = unittest.TestLoader().loadTestsFromTestCase(TestPospInstrument)
unittest.TextTestRunner(verbosity=2).run(suite)