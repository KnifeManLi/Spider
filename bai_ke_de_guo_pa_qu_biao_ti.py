# coding:utf-8

from urllib import request
from bs4 import BeautifulSoup
import os

def main_init_():
    url = 'https://baike.baidu.com/item/%E5%BE%B7%E5%9B%BD/147953'
    obj = request.urlopen(url)
    html_page = obj.read()
    Entry = BeautifulSoup(html_page, 'html.parser')

    # 删除文件, 要是文件存在直接删除, 每次都使用新文件,保证文件里面的数据都是最新的
    os.remove(path_str())

    box_list = []
    # 获取所有 a 标签
    for soup in Entry.find_all('a'):
        # 获取 a 标签里面的内容
        result = soup.get_text()
        # 将内容添加到列表里面去
        box_list.append(result)

    # 修改里面指定字符串
    box_list[12] = '详情'
    # 要输出字符串的个数
    li = ['13','4','12','7','7','5','4']
    for i in li:
        iteration(box_list, int(i))

    string = """
            ********************************
            *2018年12月18日23:01分_爬虫练习*
            ********************************
        """
    with open(path_str(), 'a') as fp:
        fp.write('\n\n' + string)

def iteration(value_list, n):
    """
      Python 列表是可变类型数据, 如果将一个 列表 当函数参数进行传递时,
      在函数里面 添加, 删除, 修改,等操作,原有列表的值也会改变
    """
    new_list = []
    for i in range(0, n):
        # n 代表要输出字符串的个数, 每次弹出列表的第一个字符串
        result = value_list.pop(0)
        # 去除里面的换行
        if result.startswith('\n'):
            pass
        else:
            # 拼接成一个新的字符串
            string = ''.join(result)
            # 将拼接好的字符串添加到列表里面去
            new_list.append(string)

    write_file(new_list)

def write_file(txt_list):
    """存储函数.将爬取到的字符串存放到本地"""
    # 流程转向
    temp = True
    for txt in txt_list:
        if temp:
            # 这里的存储格式是 北京:--> 朝阳区
            with open(path_str(), 'a') as fp:
                fp.write(txt + ":--> ")
            temp = False
        else:
            with open(path_str(), 'a') as fp:
                fp.write(' ' + txt)
    # 使存储字符串后面加上一个逗号
    with open(path_str(), 'a') as fp:
        fp.write(',' + '\n\n')

def path_str():
    """返回文件路径"""
    return r'C:\Users\Administrator\Desktop\pa-chong\百科_德国_标题\de_guo.txt'

if __name__ == "__main__":
    main_init_()

