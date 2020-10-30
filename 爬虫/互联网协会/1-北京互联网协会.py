from selenium import webdriver
import time
import re
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium import webdriver


# 如果firefox没有安装在默认位置，就要手动指定位置
location = 'D:/Program Files/Mozilla Firefox/firefox.exe'

#读入代理 df_ip_port
import pandas  as  pd
df_ip_port=pd.read_excel('爬虫/互联网协会/ip/df_ip_port.xlsx')

profile = webdriver.FirefoxProfile()
profile.set_preference('network.proxy.type', 1)
profile.set_preference('network.proxy.http', '119.142.197.77：4216')
profile.set_preference('network.proxy.http_port', 4216) # int
profile.set_preference("network.proxy.share_proxy_settings", True)

profile.update_preferences()

driver = webdriver.Firefox(firefox_profile=profile,firefox_binary=location)
#driver.get('http://httpbin.org/ip')


# 请求页面
driver.get("https://www.bjp2p.com.cn/malice/details")

str_table='''//table[@class='s-main-l-table']'''
locator = (By.XPATH, str_table)
box = WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located(locator))

# 手动登陆
time.sleep(5)

# 页面列表
page_list = []

# table 详情
# 序号
number_list = []
# 姓名
name_list = []
# 身份证号
idcard_list = []
# 手机号码
phone_list = []
# 区域
city_list = []
# 案件身份
money_list = []
# 法院名称
overdue_money_list = []

# 逾期开始时间
overdue_start_time_list = []

# 是否失联
is_shilian_list = []

# 催收情况
collection_list = []

# source
source_list = []


# 初始页面
is_final = False
tmp_page = 1
# source
label = '北京互联网金融协会'

while ((not is_final)):
    # 获取table内容
    table = driver.find_element_by_xpath("//table[@class='s-main-l-table']")

    table_rows = table.find_elements_by_tag_name('tr')
    print(str(tmp_page)+':解析table内容')
    for tr in range(1, len(table_rows)):

        number_list.append(table_rows[tr].find_elements_by_tag_name('td')[0].text)
        name_list.append(table_rows[tr].find_elements_by_tag_name('td')[1].text)
        idcard_list.append(table_rows[tr].find_elements_by_tag_name('td')[2].text)
        phone_list.append(table_rows[tr].find_elements_by_tag_name('td')[3].text)
        city_list.append(table_rows[tr].find_elements_by_tag_name('td')[4].text)
        money_list.append(table_rows[tr].find_elements_by_tag_name('td')[5].text)
        overdue_money_list.append(table_rows[tr].find_elements_by_tag_name('td')[6].text)
        overdue_start_time_list.append(table_rows[tr].find_elements_by_tag_name('td')[7].text)
        is_shilian_list.append(table_rows[tr].find_elements_by_tag_name('td')[8].text)
        collection_list.append(table_rows[tr].find_elements_by_tag_name('td')[9].text)
        page_list.append(tmp_page)
        source_list.append(label)

    tmp_page = tmp_page + 1

    str_fanye = "//li[@id='li_%d']" % tmp_page

    # 翻页,异常时任务到底
    try:
        if ((tmp_page>1) & (tmp_page%10==1)):
            str_fanye_next = "//li[@class='next']"
            driver.find_element_by_xpath(str_fanye_next).click()  # 利用xpath查找元素进行输入文本
            locator = (By.XPATH, str_fanye)
            box = WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located(locator))

        # 等待页面加载
        locator = (By.XPATH,str_fanye)
        box = WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located(locator))
        time.sleep(5)

        driver.find_element_by_xpath(str_fanye).click()  # 利用xpath查找元素进行输入文本
        time.sleep(5)
        firefox_update_ip(df_ip_port, profile)
    except Exception:
        is_final = True
        # 最终保存
        df_tmp = pd.DataFrame([number_list, name_list, idcard_list, phone_list, city_list, money_list, overdue_money_list,
                               overdue_start_time_list, is_shilian_list, collection_list, page_list, source_list]).T
        df_tmp.columns = ['number_list', 'name_list', 'idcard_list', 'phone_list', 'city_list', 'money_list',
                          'overdue_money_list', 'overdue_start_time_list', 'is_shilian_list', 'collection_list',
                          'page_list', 'source_list']
        print('save data:' + str(tmp_page))
        df_tmp.to_excel('D:/xianghuanji/code_total/爬虫/互联网协会/data/' + str(tmp_page) + '_' + label + '_final.xlsx', encoding='utf-8', index=False)
    # 每隔50页保存一次
    if tmp_page % 5 == 0:
        import pandas as pd
        df_tmp = pd.DataFrame([number_list, name_list, idcard_list, phone_list, city_list, money_list, overdue_money_list, overdue_start_time_list, is_shilian_list, collection_list, page_list, source_list]).T
        df_tmp.columns = ['number_list', 'name_list', 'idcard_list', 'phone_list', 'city_list', 'money_list', 'overdue_money_list', 'overdue_start_time_list', 'is_shilian_list', 'collection_list', 'page_list', 'source_list']
        print('save data:' + str(tmp_page))
        df_tmp.to_excel('D:/xianghuanji/code_total/爬虫/互联网协会/data/' +  str(tmp_page) + '_' + label + '.xlsx', encoding='utf-8', index=False)


