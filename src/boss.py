from http.cookies import SimpleCookie
from bs4 import BeautifulSoup
import requests
from time import sleep

def cookiesToDict (cookiesStr):
    cookie = SimpleCookie()
    cookie.load(cookiesStr)

    # Even though SimpleCookie is dictionary-like, it internally uses a Morsel object
    # which is incompatible with requests. Manually construct a dictionary instead.
    cookies = {}
    for key, morsel in cookie.items():
        cookies[key] = morsel.value
    return cookies
cookies = cookiesToDict('_uab_collina=154986259832814671100894; t=ZGi0Tg9fQhcHzTyh; wt=ZGi0Tg9fQhcHzTyh; JSESSIONID=""; __c=1550412575; __g=-; __l=l=%2Fwww.zhipin.com%2Fjob_detail%2F%3Fka%3Dheader-job&r=; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1549862598,1550311378,1550311379,1550412575; lastCity=100010000; __a=68311430.1549457543.1549862598.1550412575.195.3.74.76; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1550458820')

# 全国 薪酬15k-20k
def makeJobListUrl (pageNumber): 
    return 'https://www.zhipin.com/c100010000/y_5/?query=前端&page=%s&ka=page-%s' % (pageNumber, pageNumber)

def makeHiUrl (jid, lid):
    return 'https://www.zhipin.com/gchat/addRelation.json?jobId=%s&lid=%s' % (jid, lid)

def sayHi (response):
    jobs = BeautifulSoup(response.content, 'html.parser').select('.info-primary > h3 > a')
    print(len(jobs))
    for job in jobs:
        url = makeHiUrl(job['data-jid'], job['data-lid'])
        response = requests.post(url=url, cookies=cookies, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'})
        print(response.text)
        sleep(1)

pageNumber = 1
response = 0
while True:
    url = makeJobListUrl(pageNumber)
    response = requests.get(url=url, cookies=cookies, headers={'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.109 Safari/537.36'})
    sayHi(response)
    break
