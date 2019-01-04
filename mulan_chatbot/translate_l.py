# -*- coding:utf-8 -*-
 
import http.client
import hashlib
import urllib
import random
import json

appKey = '042cc7d45edceaf5'
secretKey = 'imMHPp1SiIibKFnFZUzMCZFYQ4Q3mchH'
 

def combine_url(q, fromLang, toLang):
    myurl = '/api'
    salt = random.randint(1, 65536)
    sign = appKey+q+str(salt)+secretKey
    m1 = hashlib.md5()
    m1.update(sign.encode("utf-8"))
    sign = m1.hexdigest()
    myurl = myurl+'?appKey='+appKey+'&q='+urllib.parse.quote(q)+'&from='+fromLang+'&to='+toLang+'&salt='+str(salt)+'&sign='+sign
    return myurl

def translate(q, key):
    if key == 'en':
        fromLang = 'EN'
        toLang = 'zh-CHS'
    if key == 'zh':
        fromLang = 'zh-CHS'
        toLang = 'EN'
    myurl = combine_url(q, fromLang, toLang)
    try:
        httpClient = http.client.HTTPConnection('openapi.youdao.com')
        httpClient.request('GET', myurl)
        response = httpClient.getresponse()
        result = response.read()
        result_json = json.loads(result.decode("utf-8"))
        return result_json["translation"][0]
    except Exception as e:
        print(e)
    finally:
        if httpClient:
            httpClient.close()

# translate("I am mulan", "en")
