import sys
import argparse
from CVE_2020_1522 import CVE_2020_15227

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CVE-2020-15227 exploit tester by Filip Sedivy')
    parser.add_argument('url', metavar='url', nargs='+', help='Victim web URL formated as http|s://domain.com')

    sys.argv = parser.parse_args()

    url = sys.argv.url[0]

    cve = CVE_2020_15227()
    cve.run(url)
