# -*- coding: utf-8 -*-
"""
Created on Wed Jul  1 14:29:21 2020

@author: EDZ
"""
import requests
import pandas as pd
import time
import json


##获得代理ip
def get_proxy_ip_online():
    url = 'http://http.tiqu.alicdns.com/getip3?num=1&type=1&pro=&city=0&yys=0&port=1&time=1&ts=0&ys=0&cs=0&lb=1&sb=0&pb=4&mr=1&regions=&gm=4'
    request_data = requests.get(url, timeout=3)
    port_ip = request_data.text
    port_ip = port_ip.replace('\r', '')
    port_ip = port_ip.replace('\n', '')
    print('port_ip' + str(port_ip))
    proxy = {"http": "http://" + port_ip, "https": "https://" + port_ip}
    return proxy


##爬取的网址
url = '''https://www.bjp2p.com.cn/malice/queryMaliceList'''

##初始ip 代理
proxy = get_proxy_ip_online()

payloadHeader = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.106 Safari/537.36"
}

param = {
    'name': '',
    'idcardno': '',
    'isLoss': '',
    'province': '',
    'hasCollection': '',
    'page': '1',
    'num': '20'
}

s = requests.Session()

s.get('https://www.bjp2p.com.cn/index', headers=payloadHeader)
s.get('https://www.bjp2p.com.cn/malice/maliceList', headers=payloadHeader)

resp = s.post(url, data=param, timeout=3, verify=False, proxies=proxy).text
resp_dic = json.loads(resp).get('maliceList')

# 解析
page_num = 1
df_total = pd.DataFrame()


def get_content(page_num, proxy, df_total):
    #flag = True
    import random
    try:

        while (page_num <= 3000):
            time.sleep(random.randrange(5, 20, 1))
            param = {
                'name': '',
                'idcardno': '',
                'isLoss': '',
                'province': '',
                'hasCollection': '',
                'page': str(page_num),
                'num': '20'
            }

            page_num_list = []
            beginOverdueTime_list = []
            hasCollection_list = []
            hasCollectionDesc_list = []
            id_list = []
            idcardno_list = []
            isLoss_list = []
            name_list = []
            overdue_list = []
            phoneNo_list = []
            platFormName_list = []
            province_list = []
            totalLoanAmount_list = []

            try:
                resp_0 = s.post(url, data=param, timeout=3, verify=False, proxies=proxy)
                resp = resp_0.text
                time.sleep(10)

                # 切换ip个数
                num = 0
                while (('过于频繁' in resp_0.text) & (num <= 10)):
                    time.sleep(20)

                    # 切换ip
                    proxy = get_proxy_ip_online()

                    print('切换ip 0：' + str(proxy['http']))
                    resp_0 = s.post(url, data=param, timeout=3, verify=False, proxies=proxy)
                    resp = resp_0.text
                    num = num + 1

            except Exception:

                proxy = get_proxy_ip_online()

                print('切换ip 1：' + str(proxy['http']))

                time.sleep(random.randrange(50, 60, 1))

                get_content(page_num, proxy, df_total)

            resp_dic = json.loads(resp).get('maliceList')

            for i in resp_dic:
                print('page_num:' + str(page_num) + ' name：' + i['name'] + ' ' + str(page_num))
                page_num_list.append(page_num)
                beginOverdueTime_list.append(i['beginOverdueTime'])

                hasCollection_list.append(i['hasCollection'])
                hasCollectionDesc_list.append(i['hasCollectionDesc'])
                id_list.append(i['id'])
                idcardno_list.append(i['idcardno'])
                isLoss_list.append(i['isLoss'])
                name_list.append(i['name'])
                overdue_list.append(i['overdue'])
                phoneNo_list.append(i['phoneNo'])
                platFormName_list.append(i['platFormName'])
                province_list.append(i['province'])
                totalLoanAmount_list.append(i['totalLoanAmount'])

            df_temp = pd.DataFrame(
                [page_num_list, beginOverdueTime_list, hasCollection_list, hasCollectionDesc_list, id_list,
                 idcardno_list, isLoss_list, name_list, overdue_list, phoneNo_list, platFormName_list, province_list,
                 totalLoanAmount_list]).T
            df_temp.columns = ['page_num_list', 'beginOverdueTime', 'hasCollection', 'hasCollectionDesc', 'id',
                               'idcardno', 'isLoss', 'name', 'overdue', 'phoneNo', 'platFormName', 'province_list',
                               'totalLoanAmount']

            page_num = page_num + 1
            df_total = pd.concat([df_total, df_temp])
            if page_num % 10 == 0:
                print('save data:' + str(page_num))
                df_total.to_excel('D:/xianghuanji/互联网协会/data/' + 'df_total_' + str(page_num) + '.xlsx')

    except Exception:

        df_total.to_excel('D:/xianghuanji/互联网协会/data/' + 'df_total_' + str(page_num) + '_final' + '.xlsx')

    return None


get_content(page_num, proxy, df_total)

##添加ip 白名单
# response = requests.get('curl web.http.cnapi.cc/index/index/save_white?neek=6ppkey=fae10aa1d846f09a2ea&white='+ip)




