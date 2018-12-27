# coding:utf-8

# 导入 urllib 包下的 request 模块
from urllib import request
import re


def main_init():
    """发起主页面链接,获取图片 url 地址"""
    # 存放浏览器验证信息的身份
    tieba_dict = {}
    # 存放图片的列表
    url_list = []
    url = 'https://tieba.baidu.com/p/3823765471'
    tieba_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                               'Chrome/69.0.3497.100 Safari/537.36'
    tieba_dict['Request'] = 'https://tieba.baidu.com/p/3823765471'

    obj = request.Request(url, headers=tieba_dict)
    response = request.urlopen(obj)
    # 返回 btype 类型数据, 将其转换成 utf-8 的格式, 之后将其里面的字符串进行分割
    data = response.read().decode('utf-8').split()

    for string in data:
        result = re.search(r'(https:).*(.jpg)', string)
        if result is not None:
            # replace 进行字符串替换,是返回一个新的字符串
            new_str = result.group().replace('\\', '')
            url_list.append(new_str)

    # 将列表进行更新,不在同一个列表里面操作, 将里面的 url 进行去重
    new_list = set(list(url_list))
    url_img_write(new_list)

def url_img_write(img_list):
    """获取图片地址将图片存放到本地"""
    # 这个值是用来获取图片的总个数
    temp_number = None
    for n, url in enumerate(img_list, start=1):
        obj = request.urlopen(url)
        image = obj.read()

        with open(img_path() + tieba() + '_' + str(n) + '.jpg', 'wb') as fp:
            fp.write(image)

        print('正在下载第 ' + str (n) + ' 请等待....')
        temp_number = n

    print('共计下载图片: ' + str(temp_number) + ' 张')
    print('*' * 30)

def img_path():
    """存放路径"""
    return r'C:\Users\Administrator\Desktop\image\\'

def tieba():
    """图片名字"""
    return '贴吧图片'


if __name__ == '__main__':
    main_init()