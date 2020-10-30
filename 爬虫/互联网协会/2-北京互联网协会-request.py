import requests
import pandas as pd
import time
import json

def  proxy_ip(df_ip_port):
    import time
    ip=list(df_ip_port['ip'])
    port=list(df_ip_port['port'])

    #随机选取ip,port
    import random
    index=random.sample(range(0,len(ip)),1)[0]

    ip_choose=str(ip[index])
    port_choose=str(port[index])

    # profile.set_preference('network.proxy.type', 1)
    # profile.set_preference('network.proxy.http', ip_choose)
    # profile.set_preference('network.proxy.http_port', port_choose)  # int
    # profile.set_preference("network.proxy.share_proxy_settings", True)
    #
    # profile.update_preferences()
    # time.sleep(1)
    # print('update ip:'+str(ip_choose))
    # print('update port:'+str(port_choose))
    # return None
    return ip_choose,port_choose

df_ip_port=pd.read_excel('爬虫/互联网协会/ip/df_ip_port.xlsx')

##爬取的网址
url = '''https://www.bjp2p.com.cn/malice/queryMaliceList'''

##初始ip
proxy={"http": "http://125.126.110.182:60004", "https": "https://125.126.110.182:60004"}

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.108 Safari/537',
    'Content-Type': 'application/json; charset=UTF-8',
    'Cookie': 'MicrosoftApplicationsTelemetryDeviceId=d6d978fd-7d4a-51bb-a56c-e9d01087265c; MicrosoftApplicationsTelemetryFirstLaunchTime=1514433998658; srcLang=-; smru_list=; sourceDia=en-US; destLang=zh-CHS; dmru_list=da%2Czh-CHS; destDia=zh-CN; mtstkn=EKimUInV29dbd91DCr7IzX80X6hVOI9Sk%252FHwx5ee4wudngq85T%252FMaSJeXCBtQJsJ; _EDGE_S=F=1&SID=2F7A08541C8762552CCA03321D306369; _EDGE_V=1; MUID=17658D2AD0B3658A0691864CD104645E; MUIDB=17658D2AD0B3658A0691864CD104645E; SRCHHPGUSR=WTS=63650030798; SRCHD=AF=NOFORM; SRCHUID=V=2&GUID=393B99CACB9E453BA91A92659B1DA288&dmnchg=1; SRCHUSR=DOB=20171228; _SS=SID=2F7A08541C8762552CCA03321D306369'
    }


param = {
    'name': '',
    'idcardno': '',
    'isLoss': '',
    'province':'',
    'hasCollection': '',
    'page': '2',
    'num': '20'
}

resp = requests.post(url, data=param, headers=headers,proxies=proxy,timeout=10)

resp_dic = json.loads(resp.text).get('maliceList')

# 解析
page_num = 1
page_num_list = []
beginOverdueTime_list = []
chuxian_list = []
chuxiandesc_list = []
falvwenshuhao_list = []
hasCollection_list = []
hasCollectionDesc_list = []
id_list = []
idcardno_list = []
isLoss_list = []
name_list = []
overdue_list = []
phoneNo_list = []
platFormName_list = []
totalLoanAmount_list = []
zhuti_list = []
zhutidesc_list = []

resp_list_dic = json.loads(resp.text).get('maliceList')
tmp = 0

df_total = pd.DataFrame()
flag = True
while(page_num <= 10):
    time.sleep(5)
    param = {
        'name': '',
        'idcardno': '',
        'isLoss': '',
        'hasCollection': '',
        'page': str(page_num),
        'num': '20'
    }

    try:
        resp = requests.post(url, data=param, headers=headers,proxies=proxy,timeout=10)
    except Exception:
        ip,port=proxy_ip(df_ip_port)
        proxy = {"http": "http://"+str(ip)+":"+str(port), "https":"http://"+str(ip)+":"+str(port)}
        resp = requests.post(url, data=param, headers=headers, proxies=proxy, timeout=10)

    resp_dic = json.loads(resp.text).get('maliceList')

    for i in resp_list_dic:
        print('page_num:' + str(page_num) + ' name：' + i['name'] + ' ' + str(tmp))
        page_num_list.append(page_num)
        beginOverdueTime_list.append(i['beginOverdueTime'])
        chuxian_list.append(i['chuxian'])
        chuxiandesc_list.append(i['chuxiandesc'])
        falvwenshuhao_list.append(i['falvwenshuhao'])
        hasCollection_list.append(i['hasCollection'])
        hasCollectionDesc_list.append(i['hasCollectionDesc'])
        id_list.append(i['id'])
        idcardno_list.append(i['idcardno'])
        isLoss_list.append(i['isLoss'])
        name_list.append(i['name'])
        overdue_list.append(i['overdue'])
        phoneNo_list.append(i['phoneNo'])
        platFormName_list.append(i['platFormName'])
        totalLoanAmount_list.append(i['totalLoanAmount'])
        zhuti_list.append(i['zhuti'])
        zhutidesc_list.append(i['zhutidesc'])
        tmp = tmp + 1

        df_temp = pd.DataFrame([page_num_list, beginOverdueTime_list, chuxian_list, chuxiandesc_list, falvwenshuhao_list, hasCollection_list, hasCollectionDesc_list, id_list, idcardno_list, isLoss_list, name_list, overdue_list, phoneNo_list, platFormName_list, totalLoanAmount_list, zhuti_list, zhutidesc_list]).T
        df_temp.columns = ['page_num_list', 'beginOverdueTime', 'chuxian', 'chuxiandesc', 'falvwenshuhao', 'hasCollection', 'hasCollectionDesc', 'id', 'idcardno', 'isLoss', 'name', 'overdue', 'phoneNo', 'platFormName', 'totalLoanAmount', 'zhuti', 'zhutidesc']

    df_total = pd.concat([df_total, df_temp])
    if tmp%10==0:
        df_total.to_excel('爬虫/互联网协会/data/'+'df_total_'+str(tmp).xlsx)

df_total.to_excel('爬虫/互联网协会/data/'+'df_total_final'.xlsx)