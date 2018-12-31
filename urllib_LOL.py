# coding:utf-8

from urllib import request
from random import randint
import os
import re


def main_init():
    """启动函数"""
    runes_img()
    props_img()
    Summoner_img()

def lol_Agent():
    """浏览器信息"""
    lol_dict = {}
    # 添加浏览器身份验证
    lol_dict['User-Agent'] = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ' \
                             'Chrome/69.0.3497.100 Safari/537.36'
    lol_dict['Request'] = 'http://lol.duowan.com/hero/'

    return lol_dict

def path(name):
    """返回文件的路径,或者创建文件夹的名字"""
    if name == 'temp':
        if not os.path.isdir(r'C:\Users\Administrator\Desktop\lol\%s' %'temp'):
            os.mkdir(r'C:\Users\Administrator\Desktop\lol\%s' %'temp')
        return '\\'.join([r'C:\Users\Administrator\Desktop\lol\%s' %'temp'])
    return '\\'.join([r'C:\Users\Administrator\Desktop\lol\%s' %name])

def the_props(url):
    """发起 url 链接"""
    try:
        print('url:', url)
        obj = request.Request(url, headers=lol_Agent())
        response = request.urlopen(obj)
        return response
    except:
        return ''

def runes_img():
    """爬取 lol 符文页图片,这个页面是动态加载的,
    在页面里提取不到,只有用浏览器调试工具 查找这个页面的js
    来获取里面的数据
    分别:提取 符文名字,符文图片,符文加成说明
    """
    url = 'http://lol.duowan.com/s/js/runes.js'
    response = the_props(url)
    html = response.read().decode('utf-8')
    # runes.js 返回的数据里面有换行符,用 正则匹配不到, 所以要将 换行符去掉, 才可匹配
    fu_wen_list = html.split('\n')
    for data in fu_wen_list:
        # 提取里面的数据
        result = re.search(r'{.*}', data)

        if result is not None:
            string = result.group()
            # 删除里面没有用字符串包裹的字段
            new_str = string.replace('iconpath+','')
            # 将外面的字符串去掉就是一个字典格式的 '{"":""}'
            dict_str = eval(new_str)
            for rune in dict_str:
                # 拼接图片路径
                rune_img = '/'.join(['http://lol.duowan.com','s','images',dict_str[rune]['icon']])
                obj = the_props(rune_img)
                content = obj.read()
                if not os.path.isdir(path('符文')):
                    os.mkdir(path('符文'))
                # 存放图片
                with open(path('符文') + '\\' + dict_str[rune]['name'] + '.gif', 'wb') as fp:
                    fp.write(content)
                # 存放图片文档
                with open(path('符文') + "\\" + '符文说明文档' + '.txt', 'a') as fp:
                    fp.write(len(dict_str[rune]['description']) * 2 * '*')
                    fp.write('\n')
                    fp.write('**:' + dict_str[rune]['name'] + '->: ' + dict_str[rune]['description'] + ':**')
                    fp.write('\n')

def props_img():
    """爬取 lol 道具图片和属性,存放本地, 用法和爬取 符文图片相同"""
    url = 'http://lolbox.duowan.com/js/itemDetailDataForEditor.js'
    response = the_props(url)
    file_data = response.read().decode('utf-8')

    result = file_data.split('\n')
    for tool in result:
        value = re.search(r'{.*}', tool)
        if value is not None:
            # 将其外面的字符串去掉 '{}', 剩下的是字典格式
            new_value = eval(value.group())

            for name in new_value:
                tiems_img_url = ''.join(['http://static.lolbox.duowan.com/images/items/',str(new_value[name]['icon']),'.png'])
                obj = the_props(tiems_img_url)
                image = obj.read()
                if not os.path.isdir(path('召唤师道具')):
                    os.mkdir(path('召唤师道具'))
                # 存放 lol 道具图片
                with open(path('召唤师道具') + '\\' + str(new_value[name]['name']) + '.png', 'wb') as fp:
                    fp.write(image)
                # 存放 lol 道具属性说明
                with open(path('召唤师道具') + '\\' + '召唤师道具文档' + '.txt', 'a') as Fp:
                    Fp.write('\n'+'&' + '\n' + '  ' + str(new_value[name]['name']) + ': ' + str(new_value[name]['filter']) + ',' + '\n')
                    Fp.write( '  ' + '价格: ' + str(new_value[name]['price']) + ',' + '\n')
                    Fp.write('  ' + '属性: ' + str(new_value[name]['attr']) + ',' + '\n' + '&' + '\n')


def Summoner_img():
    """获取召唤师 大小图片"""
    url = 'http://lol.duowan.com/s/js/spells.js'
    response = the_props(url)
    text = response.read().decode('utf-8').split('\n')

    for value in text:
        # 删除里面的字符,里面有用字符串包裹的字段
        new_string = value.replace('name', '"name"')
        two_string = new_string.replace('icon:spellicon+', '')
        desc = two_string.replace('description', '"desc"')
        data = desc.replace(',video:spellicon+','')
        level = data.replace('level', '"level"')

        tf_new = re.sub(r'"tf_\d+.jpg",','', level)
        new_level = re.sub(r'"show\d+.jpg"', '', tf_new)
        result = re.search(r'{.*}', new_level)

        if result is not None:
            # 将外面的字符串去掉
            new_level_dict = eval(result.group())
            # 获取小图 tf_1.jpg
            tf = re.search(r'tf_\d+.jpg', level)
            # 获取大图 show1.jpg
            show = re.search(r'show\d+.jpg', level)
            if tf is not None:
                # 存放小图
                Summoner(tf.group(), new_level_dict['name'])

            if show is not None:
                # 存放大图
                Summoner(show.group(), new_level_dict['name'])

def Summoner(img, name):
    """发起图片链接和将图片存放到本地"""
    skills_url = ''.join(['http://lol.duowan.com/s/images/', img])
    obj = the_props(skills_url)
    skills_img = obj.read()

    if not os.path.isdir(path('召唤师技能')):
        os.mkdir(path('召唤师技能'))
    with open(path('召唤师技能') + '\\' + name + "_" +str(randint(1,999)) + '.jpg', 'wb') as fp:
        fp.write(skills_img)


if __name__ == '__main__':
    main_init()