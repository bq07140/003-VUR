import requests

url = 'http://ingress-sit.ma/vwasp-sit-vur-service-dbr/DPL/v1/activeUser?'

# vinList=1&vinList=2
vin_li = ['HVWTDMER6PA000450', 'LAVTDMERZAA000050']
vin_str = ['vinList='+str(i) for i in vin_li]
vin_str_join = "&".join(vin_str)

url += vin_str_join
print(url)

headers = {
    'Host': 'ingress-sit.ma',
    'X-Signature': 'gy4qLmKEJ4rNXHzIjdXFHIp8si7sdv7myQ1MvPNul+c=',
    'X-Client-Id': 'vwa-vur-sit',
    'X-Nonce': '1690786405965',
    'X-Date': 'Mon, 31 Jul 2023 06:53:25 GMT',
    'X-Method': 'GET'
}

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print("请求成功:")
    print(response.text)
else:
    print("请求失败:", response.status_code)
