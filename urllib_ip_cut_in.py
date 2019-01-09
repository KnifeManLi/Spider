# coding:utf-8

from urllib import request
from bs4 import  BeautifulSoup
import requests

# 测试 ip 是否可用的数
IP_test = 200

def ip_user():
    """伪装浏览器信息"""
    ip_dict = {}
    ip_dict['Request URL'] = 'https://www.kuaidaili.com/free/'
    ip_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 ' \
                            '(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    return ip_dict

def ip_response(url):
    """发起连接获取页面"""
    response = request.Request(url, headers=ip_user())
    obj = request.urlopen(response)
    return obj.read().decode('utf-8')

def path():
    """返回 ip 存放路径"""
    return r'C:\Users\Administrator\Desktop\ip\\'

def main_init():
    """获取 ip 端口,地址,存放本地"""
    baidu_url = 'https://www.baidu.com'
    n = 0
    j = 1
    for i in range(1,2650):
        url = 'https://www.kuaidaili.com/free/inha/' + str(i) + '/'
        html = ip_response(url)
        soup = BeautifulSoup(html, 'html.parser')
        for ip in soup.find_all('tr')[1:]:
            list_ip = ip.text.split('\n')[1:8]

            porxies = {list_ip[3].lower():list_ip[3].lower() + "://" + list_ip[0] + ':' + list_ip[1]}
            response = requests.get(baidu_url, porxies)
            # 测试 ip 是否可用
            if response.status_code == IP_test:
                with open(path() + '爬虫可用_ip_2_.txt', 'a') as fp:
                    fp.write(str(j) + ': ' + str(porxies) + list_ip[2] + '-' + list_ip[4] + '\n')

                    fp.write('*'*60+'\n')
                print(' ip 测试_ok 正在下载...')
            j += 1
        n = i
    print('可用 ip 地址总数为: ' + str(n))


if __name__ == "__main__":
    main_init()