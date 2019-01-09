# coding:utf-8

from urllib import request
from bs4 import  BeautifulSoup
import requests

# 浏览器返回状态码
ip_ok = 200


def ip_user():
    """添加浏览器信息"""
    ip_dict = {}
    ip_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                            'Chrome/69.0.3497.100 Safari/537.36'
    ip_dict['Request URL'] = 'https://www.xicidaili.com/'
    return ip_dict

def ip_response(url):
    """发起 http 链接获取页面信息"""
    response = request.Request(url, headers=ip_user())
    obj = request.urlopen(response)
    return obj.read().decode('utf-8')

def path():
    """ip 地址存放路径"""
    return r'C:\Users\Administrator\Desktop\ip\\'

def main_init():
    """查找 ip 获取 ip 测试 ip 将其存放本地"""
    N = 1
    url = 'https://www.xicidaili.com/'
    html = ip_response(url)
    soup = BeautifulSoup(html, 'html.parser')
    for ip in soup.find_all(class_='odd'):
        # 将列表里面的换行符删除
        data_ip = ip.get_text().split('\n')[2:7]
        porxie = {data_ip[-1].lower():data_ip[-1].lower()+'://'+data_ip[0]+':'+data_ip[1]}
        response = requests.get('http://www.baidu.com', porxie)
        # 测试 ip 是否可用
        if response.status_code == ip_ok:
            with open(path() + '爬虫可用代理_ip_.txt', 'a') as fp:
                fp.write(str(N) + ': ' + str(porxie) + ' ' + data_ip[2] + ' ' + data_ip[3] + '\n')
                fp.write('*'*50)
                fp.write('\n')
            print('ip 可以使用 ' + str(N) + ' 个,正在下载...')
        N += 1

    print('测试代理 ip 完成,可用: ' + str(N) + ' 个')

if __name__ == '__main__':
    main_init()