# coding:utf-8

from urllib import request
from bs4 import BeautifulSoup
import re
import os

# 定义一个全局列表存放糗事百科的用户名
list_name = []

def qiushi_user():
    """添加浏览器信息"""
    qiushi_agent = {}
    qiushi_agent['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 ' \
                                 '(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    qiushi_agent['Request'] = 'https://www.qiushibaike.com/hot/'
    return qiushi_agent

def main_init():
    """获取主页面的 url, 用户名及用户头像"""
    for index in range(1,14):
        url = 'https://www.qiushibaike.com/hot/page/' + str(index) + '/'
        html = response_link(url)
        if html is not None:
            soup = BeautifulSoup(html, 'html.parser')
            # 获取用户头像及用户名
            for link in soup.find_all(rel='nofollow'):
                new_link = link.get('href')
                if new_link is not None:
                    if new_link.startswith('/'):
                        data_user = re.search(r'/users/.*$', new_link)
                        if data_user is not None:
                            new_url = ''.join(['https://www.qiushibaike.com', data_user.group()])
                            url_link(new_url)

            print('用户名及头像下载完毕...')
            print()
            print()
            # 获取糗事百科用户名发送的内容
            for blank in soup.find_all(class_="contentHerf"):
                target = blank.get('href')
                if target is not None:
                    if target.startswith('/'):
                        data_article = re.search(r'/article/.*$', target)
                        if data_article is not None:
                            article_url = ''.join(['https://www.qiushibaike.com', data_article.group()])
                            content(article_url)
                            print('------------------')
                            print('糗事百科内容下载完毕')
                            print('------------------')

def content(url):
    """获取糗事百科内容将其存储"""
    html = response_link(url)
    if html is not None:
        soup = BeautifulSoup(html, 'html.parser')
        data = soup.find(class_='content')

        for lt in list_name:
            with open(path() + lt + '\\' + lt + '_的段子' + '.txt', 'a') as fp:
                try:
                    result = data.get_text()
                    fp.write(str(result))
                except:
                    pass
            print('糗事百科内容下载中。。。')


def response_link(url):
    """发送链接获取页面"""
    try:
        obj = request.Request(url, headers=qiushi_user())
        resp = request.urlopen(obj)
        return resp.read()
    except:
        return None

def url_link(url):
    """获取糗事百科头像和用户名"""
    html = response_link(url)
    soup = BeautifulSoup(html, 'html.parser')
    img = soup.find('img')
    # 获取图片地址
    url_img = img.get('src')
    new_image = ''.join(['https:', url_img])
    image = response_link(new_image)
    # 获取用户名
    user_name = img.get('alt')
    # 创建文件夹
    is_making = create(user_name)
    # 存储图片和糗事百科信息
    if is_making is None:
        with open(path() + user_name + '\\' + user_name + '.jpg', 'wb') as fp:
            list_name.append(user_name)
            fp.write(image)

        for info in soup.find_all(class_='user-statis user-block'):
            with open(path() + '\\' + user_name + '\\' + user_name + '糗事百科信息' + '.txt', 'a') as FP:
                FP.write(str(info.get_text()))
    else:
        with open(path() + 'Error_user.txt', 'a') as p:
            p.write(':---> ' + user_name + '\n')


    print('糗事百科用户名及头像下载中...')

def create(folder):
    """以糗事百科用户名创建文件夹名字"""
    if not os.path.isdir(path()+folder):
            try:
                os.mkdir(path()+folder)
            except:
                # 用户名建立不了文件夹,直接跳过
                return True

def path():
    """返回存放的目录"""
    return r'C:\Users\Administrator\Desktop\糗事百科故事\\'



if __name__ == '__main__':
    main_init()