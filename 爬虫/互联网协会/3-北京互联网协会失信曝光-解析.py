import pandas as pd
import numpy as  np

df_1088=pd.read_excel('爬虫/互联网协会/data/1088_9北京互联网金融协会-全国老赖_final---1.xlsx')
df_1080=pd.read_excel('爬虫/互联网协会/data/1080_北京互联网金融协会-全国老赖.xlsx')

df_total=pd.concat([df_1080,df_1088])


df_total['失信被执行人']=df_total.content_list.apply(lambda x:x.split('身份证号')[0])
df_total['失信被执行人']=df_total['失信被执行人'].apply(lambda x:x.replace('失信被执行人','').replace('\n',''))
df_total['失信被执行人']=df_total['失信被执行人'].apply(lambda x:x.replace('：',''))

##截取身份证
import re
df_total['身份证号']=df_total['content_list'].apply(lambda x:re.findall(r"身份证号：(.+?)\n住址",x))
df_total['身份证号']=df_total['身份证号'].apply(lambda x:str(x).replace('[',''))
df_total['身份证号']=df_total['身份证号'].apply(lambda x:str(x).replace(']',''))
df_total['身份证号']=df_total['身份证号'].apply(lambda x:str(x).replace('\'',''))


##住址
df_total['住址']=df_total['content_list'].apply(lambda x:re.findall(r"住址：(.+?)\n执行法院",x))
df_total['住址']=df_total['住址'].apply(lambda x:str(x).replace('[',''))
df_total['住址']=df_total['住址'].apply(lambda x:str(x).replace(']',''))
df_total['住址']=df_total['住址'].apply(lambda x:str(x).replace('住',''))
df_total['住址']=df_total['住址'].apply(lambda x:str(x).replace(' ',''))
df_total['住址']=df_total['住址'].apply(lambda x:str(x).replace('。',''))
df_total['住址']=df_total['住址'].apply(lambda x:str(x).replace('\'',''))

##执行法院
df_total['执行法院']=df_total['content_list'].apply(lambda x:re.findall(r"执行法院(.+?)法院\n",x))
df_total['执行法院']=df_total['执行法院'].apply(lambda x:str(x).replace('[',''))
df_total['执行法院']=df_total['执行法院'].apply(lambda x:str(x).replace(']',''))
df_total['执行法院']=df_total['执行法院'].apply(lambda x:str(x).replace('：',''))
df_total['执行法院']=df_total['执行法院'].apply(lambda x:str(x)+'法院')
df_total['执行法院']=df_total['执行法院'].apply(lambda x:str(x).replace('\'',''))


df_total_1=df_total.drop_duplicates()
df_total_1['flag']='中国信息协会法律分会调解中心'
df_total_1['url']='http://jr.yzx360.com/list'
df_total_1=df_total_1[['page_list',  '失信被执行人', '身份证号', '住址', '执行法院', 'flag',
       'url','content_list']]

##保存数据
df_total_1.to_excel('中国信息协会法律分会调解中心_爬取数据.xlsx',index=False,encoding='utf-8')