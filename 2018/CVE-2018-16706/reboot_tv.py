import requests

r = requests.get('http://192.168.1.55:9080/qsr_server/device/reboot')

print("Status Code:", r.status_code)

#r = requests.post('http://192.168.1.55:9080/qsr_server/device/reboot')
#print("Status Code:", r.status_code)

