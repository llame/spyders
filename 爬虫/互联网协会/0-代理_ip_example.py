import requests
import pandas as pd
import time
import json


##获得代理ip
def get_proxy_ip_online():
    url = 'http://http.tiqu.alicdns.com/getip3?num=1&type=1&pro=0&city=0&yys=0&port=1&pack=106632&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=110000,130000&gm=4'
    request_data = requests.get(url, data=json.dumps(param), timeout=3)
    port_ip = request_data.text
    port_ip = port_ip.replace('\r', '')
    port_ip = port_ip.replace('\n', '')
    return port_ip


port_ip = get_proxy_ip_online()

##爬取的网址
## 查看是post的 form形式，还是payload模式

url = '''http://www.hzifia.com/api/debt/paginate'''

##初始ip
proxy = {"http": 'http://' + port_ip, "https": 'https//' + port_ip}

payloadHeader = {
    'Host': 'www.hzifia.com',
    'Content-Type': 'application/json;charset=UTF-8'
}

param = {
    'city': '',
    'idcard': '',
    'ismissing': '',
    'name': '',
    'page': 3,
    'pagesieze': '20',
    'state': ''
}

try:
    resp = requests.get(url, data=json.dumps(param), timeout=3, headers=payloadHeader, proxies=proxy, verify=False)
except Exception:
    while (True):
        port_ip = get_proxy_ip_online()
        proxy = {"http": 'http://' + port_ip, "https": 'https//' + port_ip}
        print('proxy:' + "http://" + str(port_ip))
        resp = requests.get(url, data=json.dumps(param), timeout=3, headers=payloadHeader, proxies=proxy, verify=False)
        if resp.status_code == 200:
            break

resp_dic = json.loads(resp.text).get('page')
