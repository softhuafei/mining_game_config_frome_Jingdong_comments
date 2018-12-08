
# coding: utf-8

# In[ ]:


import re
import requests
import json
import csv
import pandas as pd
from fake_useragent import UserAgent
import time
from tqdm import tqdm


# In[ ]:


# -*- coding: utf-8 -*-
"""
Created on Tue Nov 27 15:12:41 2018

@author: lenovo
"""
import re
import requests
import json
import csv
import pandas as pd
from fake_useragent import UserAgent
import time
from tqdm import tqdm
def getPageComments(url,param):           #获得一页的评论
    try:
        ua = UserAgent()
        headers_ = {'User-Agent': ua.random}
        r=requests.get(url,params=param,timeout=30, headers=headers_)
        print(r.url)
        r.raise_for_status()
        r.encoding=r.apparent_encoding
        return r.text
    except:
        print('爬取失败'+url)
        return ''
        
def getContent(data):                     #对一页的评论进行分析
    commentList=[]
    try:                     
        data_convert = re.findall(r'{"productAttr":.*}',data)  #使用正则表达式对string内容进行匹配，返回的是list
#        print(type(data_convert))
#        print(len(data_convert))
        data_convert = data_convert[0]    #取出list的元素，元素为string
#        print(type(data_convert))
        data_convert = json.loads(data_convert)    #将string转为dict
#        print(type(data_convert))
        comments = data_convert['comments']      #取出dict中的comments,comments为key,其value为list，list的元素为dict,一个dict就是一条评论
#        print(type(comments))
#        print(len(comments))
        #print(comments)
        for element in comments:   #取出list中的元素dict
            score_comment=[element['score'],element['content'].replace('\n',''), element['productColor'], element['productSize'],element['productSales'],element['referenceName']]    #取出dict中key为'score','content'对应的value，以list存储
            commentList.append(score_comment)
        return commentList
    except:
        return None
        print('解析失败')

def getComments(url,page_num,productId):
    comments = []
    param={                                                #url中的参数
#            'callback': 'fetchJSON_comment98vv28909',
            'productId': 7512626,
            'score': 0,
            'sortType': 5,
            'page': 0,
            'pageSize': 10,
            'isShadowSku': 0,
            'fold': 1
            }
    param['productId'] = productId 
    for i in range(page_num):
        param['page'] = i
        data_text = getPageComments(url,param)
        if(data_text!=''):
            commentsList = getContent(data_text)
            if(commentsList!=None):
#                print(commentsList)
                comments.extend(commentsList)
    return comments

def wirteToCsv(file_name, url,comments, write_type):                #写入csv
    with open(file_name, 'a',newline='',encoding='UTF-8') as csvFile:
        csv_writer = csv.writer(csvFile)
#        csv_writer.writerow(['url','评论'])
        if(write_type == 1):
            data = [url]
            csv_writer.writerow(data)
        if(write_type == 2):
            for element in comments:                   #comments的每个元素作为一行写入
                element.insert(0,'')
                csv_writer.writerow(element)  
        csvFile.close() 
        
def fetchProductId(url):
#https://item.jd.com/7512626.html
    productId = re.findall('\\d+',url)
    return productId
    
def readUrl(file_path):
    d = pd.read_csv(file_path)
    url_list = d['url'].values.tolist()
    return url_list

def process(url_file_path, result_file_path):
    url_base="https://sclub.jd.com/comment/productPageComments.action?"
    urls = readUrl(url_file_path)
    for url in tqdm(urls):
        productId = fetchProductId(url)
        time.sleep(0.2)
#        print('productId')
#        print(productId)
        wirteToCsv(result_file_path, url, '',1)
        comments = getComments(url_base,100,productId[0])
        wirteToCsv(result_file_path,'', comments,2)


# In[ ]:


# 注意，写入的文件是append模型的，初始化的时候保证是个空文件
process('yitiji.csv','./yitiji-result.csv')

