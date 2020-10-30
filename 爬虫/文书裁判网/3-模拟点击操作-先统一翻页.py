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
time.sleep(10)

##定义获取具体内容的链接列表
##案例连接url
list_case_href=[]

current_page_url = driver.current_url

################不断翻页获取列表
page_now=1
while page_now<=600:
    print("页面:"+str(page_now))
    href_list=driver.find_elements_by_xpath("//a[@class='caseName'] ")  # 利用xpath查找元素进行输入文本

    loop_time=0
    while((len(href_list)==0)&(loop_time<=20)):
        print("waiting loading")
        href_list = driver.find_elements_by_xpath("//a[@class='caseName'] ")  # 利用xpath查找元素进行输入文本
        time.sleep(1)
        loop_time=loop_time+1

    for i in range(len(href_list)):
        print('page_now'+str(page_now)+'case:'+str(i))
        element=href_list[i]

        ##获取连接url
        element_href=element.get_attribute('href')

        ##url添加入list列表
        list_case_href.append(element_href)
        print('element_href:'+element_href)

    print('当前去重案例个数：'+str(len(list_case_href)))
    print('反转前：'+str(page_now))

    page_now=page_now+1
    str_xpath_next_page="//a[@value="+str(page_now)+"]"
    href_list_next_page = driver.find_elements_by_xpath(str_xpath_next_page)  # 利用xpath查找元素进行输入文本
    print('翻页元素个数:'+str(len(href_list_next_page)))
    if len(href_list_next_page)>0:
        element_nex_page=href_list_next_page[0]
        element_nex_page.click()
        time.sleep(10)
        print('翻转后:'+str(page_now))
    else:
        break


###获取单个案例相关数据
list_pdf_title=[]
list_pdf_innerText=[]
list_case_url=[]
num=0
for j in list_case_href:
    print('总计案例个数：'+str(len(list_case_href)))
    num=num+1
    print('当前案例：'+str(num))

    list_case_url.append(j)
    ##跳转至详情页面
    driver.get(j)
    time.sleep(4)

    ##获取详情页面的pdf标题
    div_pdf = driver.find_element_by_xpath("//div[@class='PDF_title']")
    div_pdf_name = div_pdf.get_attribute('innerText')
    print('获取pdf_name:' + str(div_pdf_name))

    ##标题添加至list
    list_pdf_title.append(div_pdf_name)

    ##获取pdf内容
    div_pdf_content = driver.find_element_by_xpath("//div[@class='PDF_box']")
    div_pdf_content_innerText = div_pdf_content.get_attribute('innerText')
    print('获取pdf_content' + str(div_pdf_content_innerText))

    ##添加内容至list
    list_pdf_innerText.append(div_pdf_content_innerText)


import pandas  as pd
df_total=pd.DataFrame([list_pdf_title,list_pdf_innerText,list_case_url]).T
df_total.columns=['list_pdf_title','list_pdf_innerText','list_case_url']
df_total.to_excel('C:/Users/EDZ/Desktop/df_total_case.xlsx')


##缺失数据补充
df_total_queshi=df_total[df_total.list_pdf_title=='']


list_case_href_1=list(df_total_queshi['list_case_url'])
###获取单个案例相关数据
list_pdf_title_1=[]
list_pdf_innerText_1=[]
list_case_url_1=[]
num=0
for j in list_case_href_1:
    print('总计案例个数：'+str(len(list_case_href_1)))
    num=num+1
    print('当前案例：'+str(num))

    list_case_url_1.append(j)
    ##跳转至详情页面
    driver.get(j)
    time.sleep(4)

    ##获取详情页面的pdf标题
    div_pdf = driver.find_element_by_xpath("//div[@class='PDF_title']")
    div_pdf_name = div_pdf.get_attribute('innerText')
    print('获取pdf_name:' + str(div_pdf_name))

    ##标题添加至list
    list_pdf_title_1.append(div_pdf_name)

    ##获取pdf内容
    div_pdf_content = driver.find_element_by_xpath("//div[@class='PDF_box']")
    div_pdf_content_innerText = div_pdf_content.get_attribute('innerText')
    print('获取pdf_content' + str(div_pdf_content_innerText))

    ##添加内容至list
    list_pdf_innerText_1.append(div_pdf_content_innerText)

df_total_1=pd.DataFrame([list_pdf_title_1,list_pdf_innerText_1,list_case_url_1]).T
df_total_1.columns=['list_pdf_title','list_pdf_innerText','list_case_url']
df_total_not_null=df_total[df_total.list_pdf_title!='']

df_total_together=pd.concat([df_total_not_null,df_total_1])
#df_total_together.to_excel('C:/Users/EDZ/Desktop/df_total_together.xlsx')


###有效信息提取 姓名出生日期，地址等的解析
def explain_basic(str_innertext):
    def  explain_1(str_innertext):
        list_1=str(str_innertext).split('被执行人')
        if len(list_1)>1:
            result=str(list_1[1]).split('。')[0]
            if  ('女' in result) or ('男' in result):
                result = result.replace('：', '')
                return  result
            else:
                return None
        else:
            return None


    def explain_2(str_innertext):
        list_1=str(str_innertext).split('被告')
        if len(list_1)>1:
            result=str(list_1[1]).split('。')[0]
            if  ('女' in result) or ('男' in result):
                result=result.replace('：','')
                return  result
            else:
                return None
        else:
            return None
    result=explain_1(str_innertext)
    result_1=explain_2(str_innertext)
    if result is None:
        return result_1
    else:
        return result

df_total_together['基本信息']=df_total_together['list_pdf_innerText'].apply(lambda x:explain_basic(x))



###有效信息提取 姓名出生日期，地址等的解析
def explain_immei(str_innertext):
    def  explain_1(str_innertext):
        list_1=str(str_innertext).split('IMEI号')
        if len(list_1)>1:
            result=str(list_1[1]).split('的')[0]
            return  result
        else:
            return None


    def explain_2(str_innertext):
        list_1=str(str_innertext).split('IMEI号')
        if len(list_1)>1:
            result=str(list_1[1]).split('）')[0]

            return  result
        else:
            return None

    result=explain_1(str_innertext)
    result_1=explain_2(str_innertext)

    if result_1 is not None:
        result_1=result_1.split('，')[0]
        result_1=result_1.replace('为','')
        result_1=result_1.replace(')','')
        result_1=result_1.replace('）','')
    if result is not None:
        result=result.split('，')[0]
        result=result.replace('为','')
        result=result.replace(')','')
        result=result.replace('）','')
    if result is None:
        return result_1
    else:
        return result

df_total_together['imei']=df_total_together['list_pdf_innerText'].apply(lambda x:explain_immei(x))


##发布日期
def explain_faburiqi(str_inner_text):
    result = str_inner_text.split('浏览')
    if len(result) > 1:
        result = result[0]
        if result is not None:
            result = result.split('：')[1]

    else:
        result = None
    # result=result.split('浏览')[1]
    # if result is not None:
    #     result=result.split('法院')[0]+'法院'
    #     result=result.split(' ')[1]
    #     result=result.replace(' ','')

    if result is not None:
        return result
    else:
        return None


df_total_together['发布日期'] = df_total_together['list_pdf_innerText'].apply(lambda x: explain_faburiqi(x))


##法院
def explain_fayuan(str_inner_text):
    result=str_inner_text.split('民 事 判 决 书')[0]
    result=result.split('浏览')[1]
    if result is not None:
        result=result.split('法院')[0]+'法院'
        result=result.split(' ')[1]
        result=result.replace(' ','')

    if result is not None:
        return result
    else:
        return None
df_total_together['法院']=df_total_together['list_pdf_innerText'].apply(lambda x:explain_fayuan(x))


##立案时间
def explain_lian_time(str_inner_text):
    result=str_inner_text.split('本院于')
    if len(result)>1:
        result=result[1]
        result=result.split('日立案')[0]+'日'
        result = result.split('日')[0] + '日'
    else:
        result=None
    # result=result.split('浏览')[1]
    # if result is not None:
    #     result=result.split('法院')[0]+'法院'
    #     result=result.split(' ')[1]
    #     result=result.replace(' ','')

    if result is not None:
        return result
    else:
        return None
df_total_together['立案时间']=df_total_together['list_pdf_innerText'].apply(lambda x:explain_lian_time(x))


##手机租金
def explain_zujin(str_inner_text):
    result=str_inner_text.split('租金')
    if len(result)>1:
        result=result[1]
        if result is not None:
            result=result.split('；')[0]
            result = result.split(')')[0]+')'
            result = result.split('(')[0]
            result = result.split('（')[0]
            result = result.split('，')[0]
            result=result.split('及')[0]
            result=result.replace('为每月','')
            result=result.replace(')','')
            result = result.replace('按月支付。合同签订后', '')
    else:
        result=None
    # result=result.split('浏览')[1]
    # if result is not None:
    #     result=result.split('法院')[0]+'法院'
    #     result=result.split(' ')[1]
    #     result=result.replace(' ','')

    if result is not None:
        return result
    else:
        return None
#df_total_together['租金']=df_total_together['list_pdf_innerText'].apply(lambda x:explain_zujin(x))

##租赁服务服务协议前订日期
##手机租金
def explain_fuwuqianding_date(str_inner_text):
    result=str_inner_text.split('签订')
    if len(result)>1:
        result=result[0]
        result=result[len(result)-100:len(result)-1]
        result = result[len(result) - 25:len(result) - 1]
        result=result.split('。')
        if len(result)>1:
            result=result[1]
            result=result.split('，')
            if len(result)>0:
                result=result[0].replace('当日原被告双','')
                result=str(result)
                result=result.replace('原告（甲方）与被告','')
                result=result.replace('苹果手机一部，原告经审核同意出租，当日原、被告双','')
                result=result.replace('，原告(甲方)与被告（乙','')
                if '2' not in result:
                    return None
                return  result
    else:
        result=None
    # result=result.split('浏览')[1]
    # if result is not None:
    #     result=result.split('法院')[0]+'法院'
    #     result=result.split(' ')[1]
    #     result=result.replace(' ','')

    if result is not None:
        return result
    else:
        return None

def explain_zlfwxyqdrqi(str_1):
    str_1=str(str_1).replace('原告(甲方)与被告（乙','')
    str_1=str_1.replace("['下：\n",'')
    str_1=str_1.replace("，']",'')
    str_1=str_1.replace("['苹果手机一部，原告经审核同意出租，当日原、被告双']",'')
    str_1=str_1.replace("['实体门店经营手机相关业务，原被告于2017年9月']",'')
    str_1=str_1.replace("['月之前都准时还款，后即使出现逾期，其又再次和这些']",'')
    str_1=str_1.replace("['下：\n",'')
    str_1=str_1.replace("['：\n",'')
    str_1=str_1.replace("，原告（甲方）与被告（乙']",'')
    str_1=str_1.replace("['下：",'')
    str_1=str_1.replace("['：",'')
    str_1=str_1.replace("['其系诸暨伟鹏汽车销售有限公司原法定代表人，孔某1']",'')
    str_1=str_1.replace("n",'')
    str_1=str_1.replace("\\",'')
    str_1=str_1.replace("Noe",'')

    return str_1

df_total_together['租赁服务服务协议签订日期']=df_total_together['list_pdf_innerText'].apply(lambda x:explain_fuwuqianding_date(x))
df_total_together['租赁服务服务协议签订日期']=df_total_together['租赁服务服务协议签订日期'].apply(lambda x:explain_zlfwxyqdrqi(x))

##申请的sku
def explain_sku(str_inner_text):
    result=str_inner_text.split('申请租赁')
    if len(result)>1:
        result=result[1]
        result=result.split('，')[0]
        return  result
    else:
        result=None
    # result=result.split('浏览')[1]
    # if result is not None:
    #     result=result.split('法院')[0]+'法院'
    #     result=result.split(' ')[1]
    #     result=result.replace(' ','')

    if result is not None:
        return result
    else:
        return None

df_total_together['sku']=df_total_together['list_pdf_innerText'].apply(lambda x:explain_sku(x))


##申请签约价
def explain_sku_price(str_inner_text):
    result=str_inner_text.split('签约价')
    if len(result)>1:
        result=result[1]
        result=result.split('，')[0]
        if len(result)>70:
            return None
        result=result.replace('为基数','')
        result=result.replace('元','')
        result=result.split('按')[0]
        return  result
    else:
        result=None
    # result=result.split('浏览')[1]
    # if result is not None:
    #     result=result.split('法院')[0]+'法院'
    #     result=result.split(' ')[1]
    #     result=result.replace(' ','')

    if result is not None:
        return result
    else:
        return None

df_total_together['sku_price']=df_total_together['list_pdf_innerText'].apply(lambda x:explain_sku_price(x))


##申请律师费
def explain_lushi_price(str_inner_text):
    result=str_inner_text.split('杭州早稻科技有限公司律师费')
    if len(result)>1:
        result=result[1]
        result=result.split(';')[0]
        result=result.split('。')[0]
        result=result.split('、')[0]
        result=result.split('；')[0]

        return  result
    else:
        result=None
    # result=result.split('浏览')[1]
    # if result is not None:
    #     result=result.split('法院')[0]+'法院'
    #     result=result.split(' ')[1]
    #     result=result.replace(' ','')

    if result is not None:
        return result
    else:
        return None

df_total_together['律师费']=df_total_together['list_pdf_innerText'].apply(lambda x:explain_lushi_price(x))


##已支付月数
def explain_month_payed(str_inner_text):
    result=str_inner_text.split('支付了')
    if len(result)>1:
        result=result[1]

        result=result.split('，')[0]
        result=result.replace('另查明','')

        return  result
    else:
        result=None
    # result=result.split('浏览')[1]
    # if result is not None:
    #     result=result.split('法院')[0]+'法院'
    #     result=result.split(' ')[1]
    #     result=result.replace(' ','')

    if result is not None:
        return result
    else:
        return None

df_total_together['已支付']=df_total_together['list_pdf_innerText'].apply(lambda x:explain_month_payed(x))

##租用日期
##已支付月数
def explain_rent_date(str_inner_text):
    result=str_inner_text.split('租用日期为')
    if len(result)>1:
        result=result[1]

        result=result.split('，')[0]
        #result=result.replace('另查明','')

        return  result
    else:
        result=None
    # result=result.split('浏览')[1]
    # if result is not None:
    #     result=result.split('法院')[0]+'法院'
    #     result=result.split(' ')[1]
    #     result=result.replace(' ','')

    if result is not None:
        return result
    else:
        return None

df_total_together['租用日期']=df_total_together['list_pdf_innerText'].apply(lambda x:explain_rent_date(x))


def explain_rent_date_start(str_inner_text):
    str_inner_text=str(str_inner_text)
    result=str_inner_text.split('至')
    if len(result)>1:
        result=result[0]
        #result=result.split('，')[0]
        result=result.replace('起','')

        return  result
    else:
        result=None
    # result=result.split('浏览')[1]
    # if result is not None:
    #     result=result.split('法院')[0]+'法院'
    #     result=result.split(' ')[1]
    #     result=result.replace(' ','')

    if result is not None:
        return result
    else:
        return None
df_total_together['租用日期开始时间']=df_total_together['租用日期'].apply(lambda x:explain_rent_date_start(x))


##租用日期结束时间

def explain_rent_date_end(str_inner_text):
    str_inner_text=str(str_inner_text)
    result=str_inner_text.split('至')
    if len(result)>1:
        result=result[1]
        #result=result.split('，')[0]
        result=result.replace('止','')

        return  result
    else:
        result=None
    # result=result.split('浏览')[1]
    # if result is not None:
    #     result=result.split('法院')[0]+'法院'
    #     result=result.split(' ')[1]
    #     result=result.replace(' ','')

    if result is not None:
        return result
    else:
        return None
df_total_together['租用日期到期时间']=df_total_together['租用日期'].apply(lambda x:explain_rent_date_end(x))


df_total_together.to_excel('C:/Users/EDZ/Desktop/df_total_together_2.xlsx')
