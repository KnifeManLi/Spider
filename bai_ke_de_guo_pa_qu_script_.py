# coding:utf-8

from urllib import request, parse
from bs4 import BeautifulSoup
import re
import time

def main_init_():
    """主函数 发起连接,提起图片链接地址"""
    dict_user = {}
    url = 'https://baike.baidu.com/item/%E5%BE%B7%E5%9B%BD/147953'
    dict_user['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 ' \
                             '(KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'
    dict_user['Request URL'] = 'https://gss0.bdstatic.com'
    # 将字典类型进行编码
    user_agent = parse.urlencode(dict_user).encode('utf-8')

    REQUEST = request.Request(url, user_agent)
    obj = request.urlopen(REQUEST)
    # 读取并解码
    html = obj.read().decode('utf-8')
    soup = BeautifulSoup(html, 'html.parser')

    box_list = []
    url_list = []
    # 获取 script 所有标签里面的内容, 之后将里面的字符串分割['a','b','c','d'] 这样的形式
    for ipt in soup.find_all('script'):
        box_list.append(ipt.get_text().split(','))

    # 这是一个列表嵌套,[['a','b'],['c','d']]
    for link in box_list:
        for str in link:

            data = re.search(r'https:..*jpg', str)
            if data is not None:
                string = data.group()
                # 将拿到的字符串,去重掉里面的 / 字符, 替换成空格
                new_str = string.replace('\\','')
                url_list.append(new_str)

    write_jpg(set(url_list))

def write_jpg(url_list):
    """存储函数 将图片存放到本地"""
    count = 0
    for n, link in enumerate(url_list, start=1):
        # 读取链接返回链接对象, 读取这个对象. 返回这张图片的字节码
        obj = request.urlopen(link)
        result = obj.read()
        with open(r'F:\德国_script_里面的图片\\' + "德国" + str(n) +".jpg", 'wb') as fp:
            fp.write(result)

        print('图片正在下载....')
        time.sleep(2)
        count = n

    print('*************')
    print('*图片存储完毕.*')
    print("**************")
    print('共计下载图片:', str(count) + ' 张')

    text = """
            这个图片的地址是在 script 里面的, 十分的不好找, 找了近 2 个小时都找不到这张图片的地址,\n
            最后发现是在主页面底部写在 js 里面去了, 那么,只需爬取这段 js 代码即可, 这个 url 链接 \n
            写的也蛮有趣,里面有 / 这个的反斜杠字符串， 只好给你替换下咯、\n\n
            ***********************************************************
            出现的问题: <urlopen error no host given> 无法打开这个 url 地址链接,
            解决问题: 是 url 里面出现了转义字符串, 比如 \\t, \\n, \\b 只需将这个 \ 替换成 \\ 即可
            url 链接事例:https:\/\/gss0.bdstatic.com\/-4o3dSag_xI4khGkpoWK1HF6hhy\/baike\/whfpf%3D685%2C390%2C0\/sign=1b8b8a398fd6277fe94761784e052908\/fd039245d688d43f1b1e8f70751ed21b0ff43bf8.jpg
            将 url 里面的 \ 去掉即可
            **********************
            \n\n
    """

    with open(r'F:\德国_script_里面的图片\德国_document.txt', 'w') as fp:
        fp.write(text + "\n\n" + str(time.ctime()))



if __name__ == "__main__":
    main_init_()