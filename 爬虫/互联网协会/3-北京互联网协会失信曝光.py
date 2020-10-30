import time
import random

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from selenium import webdriver
opt = webdriver.ChromeOptions()  # 创建浏览器
PROXY = "119.142.197.77：4216"

opt.add_argument('--proxy-server={0}'.format(PROXY))

driver = webdriver.Chrome(options=opt)  # 创建浏览器对象

# 请求页面
driver.get("http://jr.yzx360.com/list")


#抓取
str_table='''//li[@class='clearfix']'''
locator = (By.XPATH, str_table)
box = WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located(locator))

# 手动登陆
time.sleep(5)

# 页面列表
page_list = []

# 返回内容
content_list=[]

# 初始页面
is_final = False
tmp_page = 4659
# source
label = '北京互联网金融协会-全国老赖'

while ((not is_final)&(tmp_page<=4659)):
    # 获取table内容
    table = driver.find_elements_by_xpath("//li[@class='clearfix']")
    print('-' * 100)
    print('page:' + str(tmp_page))

    for i in range(len(table)):
        print('number:' + str(i))
        content_list.append(table[i].text)
        page_list.append(tmp_page)
        print(table[i].text)


    tmp_page = tmp_page - 1

    str_fanye = "//button[@class='btn-prev']"

    # 翻页,异常时任务到底
    try:
        #str_fanye_next = "//li[@class='next']"
        driver.find_element_by_xpath(str_fanye).click()  # 利用xpath查找元素进行输入文本

        #获取active页面页码
        str_active='''//li[@class='number active']'''
        locator = (By.XPATH, str_active)
        box = WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located(locator))
        active_page = driver.find_element_by_xpath(str_active)
        print('active page:'+active_page.text)


        time.sleep(random.sample(range(3,6), 1)[0])

    except Exception:
        is_final = True
        # 最终保存
        df_tmp = pd.DataFrame([page_list, content_list]).T
        df_tmp.columns = ['page_list', 'content_list']
        print('save data:' + str(tmp_page))
        df_tmp.to_excel('D:/xianghuanji/code_total/爬虫/互联网协会/data/' + str(tmp_page) + '_'+str(i) + label + '_final.xlsx', encoding='utf-8', index=False)

    #每隔50页保存一次
    if tmp_page % 30 == 0:
        import pandas as pd
        df_tmp = pd.DataFrame([page_list, content_list]).T
        df_tmp.columns = ['page_list', 'content_list']
        print('save data:' + str(tmp_page))
        df_tmp.to_excel('D:/xianghuanji/code_total/爬虫/互联网协会/data/' +  str(tmp_page) + '_' + label + '.xlsx', encoding='utf-8', index=False)



# str_fanye = "//button[@class='btn-next']"
# flag_1=True
# while (flag_1):
#     str_active = '''//li[@class='number active']'''
#     active_page = driver.find_element_by_xpath(str_active)
#     int_active_page=int(active_page.text)
#     driver.find_element_by_xpath(str_fanye).click()
#     time.sleep(1)
#     print(str(int_active_page))
#     if int_active_page>=1000:
#         flag_1=False









