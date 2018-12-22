# coding:utf-8

from tkinter import  *
import tkinter
from urllib import request
from urllib import parse
import pyttsx3
import engineio
from pyttsx3.drivers import sapi5
import json
import sys

# 建立画布
root = Tk()
# 画布的标题
root.title('中英文翻译官')

root.resizable(False, False)  # 固定窗口大小
windowWidth = 442  # 获得当前窗口宽
windowHeight = 140  # 获得当前窗口高
screenWidth, screenHeight = root.maxsize()  # 获得屏幕宽和高
geometryParam = '%dx%d+%d+%d' % (windowWidth, windowHeight, (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2)
root.overrideredirect(True)

# 将窗口变的透明
# root.attributes("-alpha",1)

# 制定画布的大小
root.geometry(geometryParam)
canvas = tkinter.Canvas(root)
# 画布颜色
canvas.configure(bg='white')

# 获取对象结果
ver2 = StringVar()
# 检测调用哪个翻译的对象
ver3 = StringVar()

SPEAK = []

# 以获取最新的输入数据
def test(content):
    if content.isdigit():
        return True
    return False

# 检查数据
def box_list():
    return [
            # '1','2','3','4','5','6','7','8','9','0',
            'a','b','c','d','e','f','g','h','i','j',
            'k','l','m','n','o','p','q','r','s','t',
            'u','v','w','s','y','z'
            ]

def fanyi_baidu():
    dict_baidu = {}
    headers_dict = {}
    # 获取输入的字符串给变量
    date = ver1.get()
    url = 'https://fanyi.baidu.com/transapi'
    # 将数据以表单的形式进行提交
    maker = dict_baidu['query'] = date

    try:
        if maker[0] in box_list():
            dict_baidu['from'] = 'en'
            dict_baidu['to'] = 'zh'
        else:
            dict_baidu['from'] = 'zh'
            dict_baidu['to'] = 'en'
    except:
        speak()

    headers_dict['Referer'] = 'https://fanyi.baidu.com/'
    headers_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                               'Chrome/69.0.3497.100 Safari/537.36'

    # 将字典数据转换成浏览器识别的数据
    url_utf8 = parse.urlencode(dict_baidu).encode('utf-8')

    try:
        # 发起连接返回一个 Request 对象
        request_s = request.Request(url, url_utf8, headers_dict)
        REQUEST = request.urlopen(request_s)
        # 进行读取并转换成可以识别的编码格式
        html_date = REQUEST.read().decode('utf-8')
        # 将其转换成 json 格式的数据好进行提取, 假如有 "\u7231" 这样的字符串,直接转换成 json 格式就可以正常读取
        result = json.loads(html_date)
    except:
        fanyi_youdao()

    try:
        SPEAK.append(result['data'][0]['dst'])
        # 将提到的数据放到另一个画板上面去
        ver2.set(result['data'][0]['dst'])
        ver3.set('百度翻译   OK')
    except:
        fanyi_youdao()

def fanyi_youdao():
    dict_youdao = {}
    headers = {}
    url = 'http://fanyi.youdao.com/translate?smartresult=dict&smartresult=rule'
    # 获取输入的字段
    dict_youdao['i'] = ver1.get()
    # 以 post 进行提交给浏览器的字段,也称伪装信息
    dict_youdao["from"] = "AUTO"
    dict_youdao["to"] = "AUTO"
    dict_youdao["smartresult"] = "dict"
    dict_youdao["client"] = 'fanyideskweb'
    dict_youdao['salt'] = '15436587812455'
    dict_youdao['sign'] = 'ce6e5f99bdf63146ef3ce4e38c4dcfe8'
    dict_youdao['ts'] = '1543658781245'
    dict_youdao['bv'] = '530358e1f56d925c582f7d2d49f07756'
    dict_youdao['doctype'] = 'json'
    dict_youdao['version'] = '2.1'
    dict_youdao['keyfrom'] = 'fanyi.web'
    dict_youdao["action"] = "FY_BY_CLICKBUTTION"
    dict_youdao["typoResult"] = "false"
    # 伪装成浏览器的形式提交数据
    dict_youdao['Referer'] = 'http://fanyi.youdao.com/'
    dict_youdao['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                              'Chrome/69.0.3497.100 Safari/537.36X-Requested-With: XMLHttpRequest'
    # 对提交的值进行编码
    sub_code = parse.urlencode(dict_youdao).encode('utf-8')
    try:
        # 发起一个 Request 请求
        REQUESET = request.Request(url, sub_code, headers)
        # 打开这个链接
        html = request.urlopen(REQUESET)
        data = html.read().decode('utf-8')
        # 转换 js 格式
        js_data = json.loads(data)
    except:
        fanyi_baidu()

    try:
        print('youdao-->>', js_data['translateResult'][0][0]['tgt'] + ' ')
        # 将翻译好的数据显示出来
        ver2.set(js_data['translateResult'][0][0]['tgt'] + ' ')
        ver3.set('有道翻译   OK')
    except:
        # 调用百度翻译
        fanyi_baidu()

def speak():
    "SPEAK 是存放输入字符串的列表,定义正全局变量"
    engineio = pyttsx3.init()# 初始化
    voices = engineio.getProperty('voices')
    engineio.setProperty('rate', 130)  # 这里是管控语音速度的
    engineio.setProperty('voice', voices[0].id)

    if len(SPEAK):
        engineio.say(SPEAK[len(SPEAK)-1])# 获取最新输入的值
        engineio.runAndWait()
        data = SPEAK[0]
        if data != SPEAK[len(SPEAK)-1]:# 比较两个值要是不同就证明有新的值进入了,将原先的给删除掉
            del SPEAK[0]
    else:
        engineio.say("请输入你要翻译的英文或者汉字")
        engineio.runAndWait()
        sys.exit()

def show():
    """删除输入文本框里面的字符"""
    ver1.delete(0, END)

testCMD = root.register(test)
Label(root, text='输入:', fg='red').grid(row=0, sticky=W)
Label(root, text='结果:', fg='red').grid(row=1, sticky=W)
Label(root, text='检测:', fg='red').grid(row=2, sticky=W)

# 输入文本框
ver1 = Entry(root, width=25, font = ('Helvetica', '15', 'bold'),)
ver1.grid(row=0, column=1)


Entry(root, textvariable=ver2, font = ('Helvetica', '15', 'bold'), validate="key", state='disabled',bd = '0.5',width=25, validatecommand=(testCMD, '%W')).grid(row=1, column=1)
Entry(root, textvariable=ver3, font = ('Helvetica', '15', 'bold'),       validate="key", state='disabled',bd = '0',width=25, validatecommand=(testCMD, '%W')).grid(row=2, column=1)


Button(root, text="清 空", width=5, command=show, activebackground='red', bd='1').grid(row=0, column=2, ipadx=0, ipady=1)
Button(root, text='翻译', fg='red', width=8, command=fanyi_baidu, bd='1').grid(row=3, column=1,columnspan=3, sticky=W, padx=10,pady=5)
Button(root, text='退出', fg='red', width=8, command=root.quit, bd='1').grid(row=3, column=1,sticky=E, columnspan=3, padx=10,pady=5)
Button(root, text='语音播报', fg='red', width=8, command=speak, bd='1').grid(row=3, column=1)
# bg 是用来修改按键颜色的
# activebackground 是用来变换字体颜色的
# 将画布渲染出来
# fg 按钮文字颜色
# relief 去除边框


# 进入事件循环
mainloop()


