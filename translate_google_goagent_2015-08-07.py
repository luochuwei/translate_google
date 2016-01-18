#-*- coding:utf-8 -*-
############################################
#
#    Author: Chuwei Luo
#    Email: luochuwei@gmail.com
#    Date: 07/08/2015
#    Usage: google translate with goagent proxy
#
############################################

import cPickle
import re
import urllib,urllib2

#-*- coding: utf-8 -*-

import re
import urllib,urllib2
import random

def translate(sentence):
    user_agents = ['Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20130406 Firefox/23.0','Mozilla/5.0 (Windows NT 6.1; WOW64; rv:18.0) Gecko/20100101 Firefox/18.0', 'Mozilla/5.0 (Windows; U; Windows NT 6.1; en-US) AppleWebKit/533 (KHTML, like Gecko) Element Browser 5.0', 'Mozilla/5.0 (compatible; MSIE 10.0; Windows NT 6.1; WOW64; Trident/6.0)', 'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36', 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/28.0.1468.0 Safari/537.36', 'Mozilla/5.0 (compatible; MSIE 9.0; Windows NT 6.0; Trident/5.0; TheWorld)','Mozilla/5.0 (Windows NT 5.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36 SE 2.X MetaSr 1.0']
    
    index = random.randint(0, 8)
    index2 = random.randint(0,1)
    # print user_agents[index]
    values = {'h1':'zh-CN', 'ie':'UTF-8', 'text':sentence, 'langpair':"'en'|'zh-CN'"}
    # url=['http://translate.gfsstp.com','http://translate.google.cn/','http://translate.google.com/']
    url=['http://translate.google.cn/','http://translate.google.com/']
    # url2 = 'http://translate.google.cn/'
    # url3 = 'http://translate.google.com/'
    data = urllib.urlencode(values)
    
    try:
        req = urllib2.Request(url[index2],data)
        user_agent = user_agents[index]
        # browser='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
        req.add_header('User-Agent', user_agent)
        response = urllib2.urlopen(req, timeout=10)
    except Exception, e1:
        try:
            req = urllib2.Request(url[1-index2],data)
            user_agent = user_agents[index]
            # browser='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
            req.add_header('User-Agent', user_agent)
            response = urllib2.urlopen(req, timeout=10)
            # print 'Google'
        except Exception, e2:
            """
            goagent代理
            """
            # proxy = urllib2.ProxyHandler({"http":"http://127.0.0.1:8087","https":"https://127.0.0.1:8087"})
            # opener = urllib2.build_opener(proxy)
            # urllib2.install_opener(opener)
            # req = urllib2.Request(url[2],data)
            # user_agent = user_agents[index]
            # # browser='Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/31.0.1650.63 Safari/537.36'
            # req.add_header('User-Agent', user_agent)
            # response = urllib2.urlopen(req, timeout=20)
        
    

    html = response.read()
    response.close()
    p=re.compile(r"(?<=TRANSLATED_TEXT=).*?;")
    m=p.search(html)
    
    chineseText=m.group(0).strip(';')
    return chineseText



if __name__ == '__main__':
    ftext = open(r'text_unlabeled.review')
    ftext_translate = open(r'text_unlabeled_translate.txt', 'w')
    ftext_error = open(r't_error_of_books.txt', 'w')


    n = 0

    for textid,textline in enumerate(ftext):
        try:
            wt = translate(textline)
            ftext_translate.write(wt)
            ftext_translate.write('\n')
        except Exception, e3:
            print e3
            print textid
            #在出错的一行写EEEEEEE...作为记号
            ftext_translate.write('EEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')
            ftext_translate.write('\n')
            ftext_error.write(str(textid))
            ftext_error.write('\n')

    ftext.flush()
    ftext.close()
    ftext_translate.flush()
    ftext_translate.close()
    ftext_error.flush()
    ftext_error.close()
