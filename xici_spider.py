import random
from urllib import request
import chardet
from bs4 import  BeautifulSoup
import os
import logging

def gen_spider_data(proxy_ips, user_agents, referer, host, url, request_type):
    proxy_ips   = proxy_ips             #代理ip
    user_agents = user_agents           #浏览器客户端
    referer     = referer               #来源网址
    host        = host                  #服务器地址
    url         = url                   #访问地址
    request_type= request_type          #请求类型
    spider_data = {
        'proxy_ip'      : random.choice(proxy_ips),
        'user_agent'    : random.choice(user_agents),
        'referer'       : referer,
        'host'          : host,
        'url'           : url,
        'request_type'  : request_type
    }
    return spider_data

def get_content(spider_data):
    if spider_data['proxy_ip'] != '0.0.0.0':
        proxy_handler = request.ProxyHandler({'http':spider_data['proxy_ip']})
        proxy_auth_handler = request.ProxyBasicAuthHandler()
        opener = request.build_opener(proxy_handler, proxy_auth_handler)
        request.install_opener(opener)
    forged_header = {
        'User-Agent': spider_data['user_agent'],
        'Referer'   : spider_data['referer'],
        'Host'      : spider_data['host'],
        spider_data['request_type'] : spider_data['url']
    }
    req = request.Request(spider_data['url'], headers=forged_header)
    html = request.urlopen(req, timeout=8)
    content = html.read()
    encoding = chardet.detect(content)['encoding']
    #html = request.urlopen(req, timeout=8)
    return  content.decode(encoding)

def getip_from_xici():
    proxy_ips   = ['0.0.0.0']         #不设置代理
    user_agents = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0',
                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.13705.206 Safari/537.36',
                  'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36']
    referer     = 'http://www.xicidaili.com/nn/'
    host        = 'www.xicidaili.com'
    url         = 'http://www.xicidaili.com/nn/'
    request_type= 'GET'
    try:
        spider_data = gen_spider_data(proxy_ips, user_agents, referer, host, url, request_type)
        html_content= get_content(spider_data)
        return html_content
    except Exception as e:
        print(e)

def testip_from_content(html_content):
    soup    = BeautifulSoup(html_content, 'lxml')
    ips     = soup.find_all('tr')
    save_ip = ''
    for ind, ip in enumerate(ips):
        if ind == 0:
            continue
        tds = ip.find_all('td')
        proxy = 'http://%s:%s' %(tds[1].contents[0], tds[2].contents[0])
        print('total:%s index:%d ip:%s' %(len(ips), ind, proxy))
        try:
            # 代理ip
            proxy_ips = [proxy]
            # 浏览器客户端
            user_agents = ['Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:48.0) Gecko/20100101 Firefox/48.0',
                          'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 UBrowser/5.6.13705.206 Safari/537.36',
                          'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Ubuntu Chromium/51.0.2704.79 Chrome/51.0.2704.79 Safari/537.36',
                          'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36']
            # 来源网址
            referer = 'http://ip.chinaz.com/getip.aspx'
            # 服务器
            host = 'ip.chinaz.com'
            # 要访问的url
            url = 'http://ip.chinaz.com/getip.aspx'
            # 请求类型
            request_type    = 'GET'
            spider_data     = gen_spider_data(proxy_ips, user_agents, referer, host, url, request_type)
            html_content    = get_content(spider_data)
            #print(html_content)
        except Exception as e:
            logging.warning(e.__str__())
            continue
        else:
            save_ip = save_ip + proxy + os.linesep

    with open('ips.txt', 'w') as ip_file:
        ip_file.write(save_ip)

testip_from_content(getip_from_xici())