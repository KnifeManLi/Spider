# coding:utf-8

from urllib import request
from urllib import parse
from bs4 import BeautifulSoup
from tkinter import *
import os

root = Tk()
# 选择个性签名的 对象
var = StringVar()
# 显示信息的 对象
var_add = StringVar()
# 存放要设计的签名字体
STR = ''

def main_init():
    """进行获取链接,爬取,将图片存储到本地"""
    dict = {}
    head = {}
    data = {'个性签':'jfcs.ttf','连笔签':'qmt.ttf','潇洒签':'bzcs.ttf','草体签':'lfc.ttf','和文签':'haku.ttf','商务签':'zql.ttf','可爱签':'yqk.ttf'}

    # var_data.get() 是获取文本框输入的字符, 这是以 post 进行提交
    dict['word'] = var_data.get()
    dict['sizes'] = 60
    # 根据选择的键来获取相应的值
    dict['fonts'] = data[STR]
    dict['fontcolor'] = '#000000'
    # 添加浏览器信息
    url = 'http://www.uustv.com/'
    head['Referer'] = 'http://www.uustv.com/'
    head['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/69.0.3497.100 Safari/537.36'

    try:
        # 先将 dict 转换成 unicode 编码, 再转换成浏览器识别的编码 utf-8
        code = parse.urlencode(dict).encode('utf-8')
        obj = request.Request(url, code, head)
        response = request.urlopen(obj)
    except:
        var_add.set('网络出现错误, 请稍后再试')

    # 读取文件，进行解码
    text = response.read().decode('utf-8')
    # 解析方式
    soup = BeautifulSoup(text, 'html.parser')

    try:
        # 查找标签
        scr = soup.find('img')
        # 获取图片链接
        src_url = scr.get('src')
        # 拼接 http:\\... + 图片链接地址
        new_url = ''.join([url,src_url])
        REQUEST = request.urlopen(new_url)
        result = REQUEST.read()
    except:
        var_add.set('程序出 Bug 咯, 请拨打,8888 求救')

    # 查看这个签名是否存在,
    if not os.path.isfile(path()  + var_data.get() + '_' + STR + '.gif'):
        with open(path() + var_data.get() + '_' + STR + '.gif', 'wb') \
                as fp:
            fp.write(result)
        var_add.set('签名设计完成.请 退出 查看')
    else:
        var_add.set('签名设计 失败 请重新设计')

def path():
    """图片存放路径"""
    return r'C:\Users\Administrator\Desktop\pa-chong\urllib_包_练习\\'

def show():
    """清空文本框"""
    var_data.delete(0,END)

def test(content):
    if content.isdigit():
        return True
    return False

def temp(event):
    # 修改全局变量的值,好将新值替换,
    # var.get() == 是下拉框选中的值
    global STR
    STR = var.get()

def qianming_list():
    """选择不同的签名"""
    return ['个性签','连笔签','潇洒签','草体签','和文签','商务签','可爱签']



Label(root, text="作品:",fg='red').grid(row=0, sticky=E)
Label(root, text="检测:",fg='red').grid(row=1)

testCMD = root.register(test)
var_data = Entry(root, width=25, font=('Helvetica', '15', 'bold'), )
var_data.grid(row=0, column=1)

Entry(root, textvariable=var_add, font = ('Helvetica', '15', 'bold'), validate="key", state='disabled',bd = '0',width=25, validatecommand=(testCMD, '%W')).grid(row=1, column=1)

var.set(qianming_list()[0])
data = OptionMenu(root, var, *qianming_list())
data.grid(row=3, column=1,sticky=W)
data.bind_all('<Button-1>', temp)

Button(root, text="清空", width=5, fg='red',command=show).grid(row=0, column=2, ipadx=0, ipady=1)
Button(root, text="退出",  width=5, fg='red',command=root.quit) \
    .grid(row=3, column=1,sticky=E, columnspan=3, padx=10,pady=5)

Button(root, text='马上设计', command=main_init, fg='red', width=8, bd='1').grid(row=3, column=1)

mainloop()

