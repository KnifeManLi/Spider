# coding:utf-8

from urllib import request, parse
from bs4 import BeautifulSoup
import  time
import re

def main_init_():
    # 获取主页面 url 链接
    url = 'https://baike.baidu.com/item/%E5%BE%B7%E5%9B%BD/147953'
    dict_header = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36',
                   'Request URL':'https://baike.baidu.com/item/%E5%BE%B7%E5%9B%BD/147953'}

    # 先进行编码,编译成浏览器可以读取的编码
    page_dict_header = parse.urlencode(dict_header).encode('utf-8')
    # 将编码和 url 链接传进去, 就可以伪装成浏览器访问了
    obj_url = request.Request(url, page_dict_header)


    REQUEST = request.urlopen(obj_url)
    html_page = REQUEST.read()
    soup = BeautifulSoup(html_page, 'html.parser')

    link_list = []
    # 提取 link 标签里面的链接, 将其添加到列表里面去
    for link in soup.find_all('link'):
        link_list.append(link.get('href'))

    # 将拿到链接的列表进行更新,去除重复的
    new_list = set(list(link_list[2:]))
    open_css_file(new_list)

def open_css_file(link_list):
    """将拿到的 css 文件进行发起连接,将里面的字符进行分割
        好提取里面的图片地址
    """
    list_css_png = []
    for css_url in  link_list:
        obj = request.urlopen(css_url)
        list_str = obj.read().decode('utf-8').split()
        # 迭代出分割的字符,用正则进行匹配,查找出图片链接地址
        for result in list_str:
            data = re.search(r'https:.*png', result)
            if data is not None:
                list_css_png.append(data.group())


    new_list_css_png  = set(list(list_css_png))
    number = write_css_png(new_list_css_png)

    print('*************')
    print('*图片存储完毕.*')
    print("**************")
    print('共提取 css 里面的图片:', number-1)
    data_str = '百科 德国 图片提取,文件类型为 css, 今天爬取 css 图片想了两天, 以为网页里面的 class 的值,' \
               '可以提取到 css 里面的 url, 用了 N 多方法都不行, 网上查找也无头绪, 将 css 页面转换来转换去' \
               '转成 json 不行, 转成 dict 不行, 转成 str 不行, 就是提取不到数据, 想了又想,' \
               '将拿到的 css 页面返回的字符串分割成列表字符串["doc1","doc2"], 再用正则进行匹配,才拿到 css 里面的 url 地址' \
               '还是 解决问题的思路要提高, 把握问题的根本, 才是关键'

    with open(r'F:\德国_css_图片\\document.txt', 'w') as fp:
        fp.write(data_str + "\n\n" + str(time.ctime()))

def write_css_png(new_list_css_png):
    """存储图片到本地"""
    n = 1
    for url_png in new_list_css_png:
        obj_png = request.urlopen(url_png)
        png_data = obj_png.read()
        print('png', png_data)
        with open(r'F:\德国_css_图片\\' + '德国' + str(n) + '.png', 'wb') as fp:
            fp.write(png_data)

        n += 1
        print('图片正在下载...')
        time.sleep(2)
    return n


if __name__ == "__main__":
    main_init_()