from selenium import webdriver
import time
import re
# opt = webdriver.ChromeOptions()  # 创建浏览器
# opt.add_experimental_option('useAutomationExtension', False)
# opt.add_experimental_option('excludeSwitches', ['enable-automation'])
#
# driver = webdriver.Chrome(options=opt)  # 创建浏览器对象
# driver.get('https://wenshu.court.gov.cn')  # 打开网页
# driver.maximize_window()                      #最大化窗口
# time.sleep(2)  # 加载等待
#
# driver.find_element_by_xpath("//input[@class='searchKey search-inp']").send_keys("早稻科技")  # 利用xpath查找元素进行输入文本
# a=driver.find_element_by_xpath("//div[@class='search-rightBtn search-click']") # 点击按钮
# a.click()
# print(a)

from selenium import webdriver
# 如果firefox没有安装在默认位置，就要手动指定位置
location = 'D:/Program Files/Mozilla Firefox/firefox.exe'
driver = webdriver.Firefox(firefox_binary=location)

# 请求页面
driver.get("https://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=922c7c42c93d1384ebed74df916fb170&s21=%E6%97%A9%E7%A8%BB%E7%A7%91%E6%8A%80")
import time
time.sleep(5)

##定义获取具体内容的链接列表
list_pdf_href=[]
list_pdf_title=[]
list_pdf_innerText=[]
list_list_page_url=[]

##获取下一页的href
#element_next_page_href=driver.find_elements_by_xpath()
current_page_url = driver.current_url

# 获取详情页
page_now=1
while page_now<=10:
    print("页面:"+str(page_now))
    href_list=driver.find_elements_by_xpath("//a[@class='caseName'] ")  # 利用xpath查找元素进行输入文本
    list_tmp = []
    for i in range(len(href_list)):
        print(i)
        list_list_page_url.append(current_page_url)

        element=href_list[i]

        ##获取连接url
        element_href=element.get_attribute('href')
        print(element_href)
        ##url添加入list列表
        list_tmp.append(element_href)

    for j in list_tmp:
        print(j)
        list_pdf_href.append(j)
        ##跳转至详情页面
        driver.get(j)
        time.sleep(3)

        ##获取详情页面的pdf标题
        div_pdf=driver.find_element_by_xpath("//div[@class='PDF_title']")
        div_pdf_name=div_pdf.get_attribute('innerText')
        print('获取pdf_name:'+str(div_pdf_name))

        ##标题添加至list
        list_pdf_title.append(div_pdf_name)

        ##获取pdf内容
        div_pdf_content=driver.find_element_by_xpath("//div[@class='PDF_box']")
        div_pdf_content_innerText=div_pdf_content.get_attribute('innerText')
        print('获取pdf_content'+str(div_pdf_content_innerText))

        ##添加内容至list
        list_pdf_innerText.append(div_pdf_content_innerText)


    ##选择点击下一页按钮
    ##返回最近列表页面
    driver.get(current_page_url)
    print('反转前：'+str(page_now)+' url:'+current_page_url)

    page_now=page_now+1

    str_xpath_next_page="//a[@value="+str(page_now)+"]"
    href_list_next_page = driver.find_elements_by_xpath(str_xpath_next_page)  # 利用xpath查找元素进行输入文本
    print('翻页元素个数:'+str(len(href_list_next_page)))
    if len(href_list_next_page)>0:
        element_nex_page=href_list_next_page[0]
        element_nex_page.click()
        time.sleep(5)
        current_page_url=driver.current_url
        print('翻转后:'+str(page_now)+' url:'+current_page_url)

# https://wenshu.court.gov.cn/website/wenshu/181217BMTKHNT2W0/index.html?pageId=922c7c42c93d1384ebed74df916fb170&s21=%E6%97%A9%E7%A8%BB%E7%A7%91%E6%8A%80


import pandas  as pd
df_total=pd.DataFrame([list_pdf_title,list_pdf_innerText,list_pdf_href]).T
df_total.columns=['list_pdf_title','list_pdf_innerText','list_pdf_href']
df_total.to_excel('C:/Users/EDZ/Desktop/df_total.xlsx')
