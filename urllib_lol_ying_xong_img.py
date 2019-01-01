# coding:utf-8

from urllib import request
from bs4 import BeautifulSoup
import os

def main_init():
    """获取主页面 url 提取相关的信息,英雄 url, 名字, 属性等信息"""
    lol_dict = {}
    lol_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                             'Chrome/69.0.3497.100 Safari/537.36'
    lol_dict['Request URL'] = 'http://lol.duowan.com/hero/'
    url = 'http://lol.duowan.com/hero/'
    obj = request.Request(url, headers=lol_dict)
    response = request.urlopen(obj)
    html = response.read()

    soup = BeautifulSoup(html, 'html.parser')
    # for link in soup.find_all(id="data-aside"):
        # 用 find_all 查找是返回的 bs4 对象, 再用 select 选择器查找, 也是返回的 bs4 对象, 必须迭代才能使用 get 方法来查找
        # href_list = link.select('a, href')[1:]
        # for http in href_list:
        #     print(http.get('href'))
        #     # print(http.text)
        #     address = http.get('href')
        #     text = http.text
        #     # print(type(text))
        #        # response_img(text, address)

    # 获取英雄 url 链接
    ying_xong_list = []
    for ying_xong in soup.find_all(class_='lol_champion'):
        ying_xong_list.append(ying_xong.get('href'))
    # 获取英雄名字
    name_list = []
    for name in soup.find_all(class_='champion_name'):
        name_list.append(name.text)
    # 获取英雄属性
    instructions_list = []
    for inst in soup.find_all(class_='tooltip champion_tooltip'):
        instructions_list.append(inst.text)

    # 将英雄名字去重
    new_name_list = []
    for ch in name_list:
        if ch.replace(' ','') not in  new_name_list:
            new_name_list.append(ch)

    ying_xong_url_name(new_name_list, instructions_list ,ying_xong_list)

def ying_xong_url_name(new_name_list, instructions_list, ying_xong_list):
    """获取英雄图片地址,和 名字,属性"""
    for url in  ying_xong_list:
        obj = request.urlopen(url)
        html = obj.read()
        soup = BeautifulSoup(html, 'html.parser')

        name = new_name_list.pop(0)
        name = name.replace(' ','')
        inst = instructions_list.pop(0)

        n = 1
        # 获取英雄图片链接地址
        for img in soup.find_all(alt="$title"):
            image = img.get('src')
            wrire_ying_xong( inst, image,  name, n)
            n += 1

def wrire_ying_xong( inst, img_url,  name, n):
    # 每个英雄建立自己的文件夹
    if not os.path.isdir(path(name)):
        os.mkdir(path(name))

    img_obj = request.urlopen(img_url)
    data = img_obj.read()
    print('正在下载:' +  name + ' 的图片:-->' + img_url)

    new_name = '\\'.join([path(name), name])
    # 英雄图片
    with open(new_name + str(n) + '.jpg', 'wb') as fp:
        fp.write(data)

    # 英雄的属性说明
    try:
        if not os.path.exists(new_name  + '.txt'):
            with open(new_name +  '.txt', 'w') as Fp:
                Fp.write(str(inst))
    except Exception as text:
        print('没有存入的文档有:-->', text)

def path(name):
    """返回一个文件路径"""
    return ''.join([r'C:\Users\Administrator\Desktop\LOL\%s' %name])

if __name__ == '__main__':
    main_init()