# coding:utf-8

import os
from tkinter import *
import tkinter

root = Tk()
root.title('文件修改工具')

root.resizable(False, False)  # 固定窗口大小
windowWidth = 478  # 获得当前窗口宽
windowHeight = 175  # 获得当前窗口高
screenWidth, screenHeight = root.maxsize()  # 获得屏幕宽和高
geometryParam = '%dx%d+%d+%d' % (windowWidth, windowHeight, (screenWidth - windowWidth) / 2, (screenHeight - windowHeight) / 2)
root.overrideredirect(True)

# 将窗口变的透明
# root.attributes("-alpha",0.5)

# 制定画布的大小
root.geometry(geometryParam)
canvas = tkinter.Canvas(root)
# 画布颜色
canvas.configure(bg='white')

ver3 = StringVar()
ver4 = StringVar()

def PaTh_join(*args):
    # 当前目录和 listdir 返回里面文件的目录进行拼接,
    new_path = '\\'.join(args)
    return new_path

def D_dish(path_D, oid_file, new_file):
    for D in os.listdir(path_D)[1:]:
        # 如果 D 盘目录下存在这个文件直接进行修改 查看是否是一个文件夹, 要是文件夹返回 True
        if D.startswith(oid_file):
            oid = PaTh_join(path_D, D)
            new = PaTh_join(path_D, new_file)
            os.rename(oid, new)
            print('文件名修改成功-所在盘符:', new)
            return new

        # 如果 D 盘目录不存在 则向里面的文件夹进行查看, 和不等于 System 开头的文件,这个文件是不可以访问的(系统文件)
        elif os.path.isdir( PaTh_join(path_D, D) ) is not D.startswith('System'):
            for file in os.listdir( PaTh_join(path_D, D )):
                if file.startswith(oid_file):
                    # 进行替换
                    oid = PaTh_join(path_D, D, oid_file)
                    new = PaTh_join(path_D, D, new_file)
                    os.rename(oid, new)
                    print('文件名修改成功-所在盘符:', new)
                    return new

                # 向下个文件夹进行查看
                elif os.path.isdir( PaTh_join(path_D, D, file)):
                    for line in os.listdir( PaTh_join(path_D, D ,file)):
                        if line.startswith(oid_file):
                            oid = PaTh_join(path_D, D, file, oid_file)
                            new = PaTh_join(path_D, D, file,  new_file)
                            os.rename(oid, new)
                            print('文件名修改成功-所在盘符:', new)
                            return new
    return False

# 以获取最新的输入数据
def test(content):
    if content.isdigit():
        return True
    return False

def show_old():
    """删除输入文本框里面的字符 第一个文本框"""
    ver1.delete(0, END)

def show_new():
    """删除输入文本框里面的字符 第二个文本框"""
    ver2.delete(0, END)

def show_file():
    """删除输入文本框里面的字符 第三个文本框"""
    ver_check.delete(0, END)

def box_list_drive():
    """搜索的盘符"""
    return [r'C:\Users\Administrator\Desktop', 'D:', 'E:', 'F:']

def creat():
    """将拿到的文件名路径存储到本地"""
    li = []
    # ver1.get() 要是没有输入数据, 返回的是一个空字符串 ‘’
    old_name = ver1.get()
    new_name = ver2.get()
    search_file = ver_check.get()
    tp = box_list_drive()
    if old_name != '' and new_name  != '':
        for check_path in box_list_drive():
            data = D_dish(check_path, old_name, new_name)
            li.append(data)

        if not(any(li)):
            ver3.set('没有这个文件,请核对文件名...')
        else:
            top = Toplevel()
            top.title('文件路径')
            for path in li:
                mag = Message(top, font = ('Helvetica', '25', 'bold'),width=1200, text=path)
                mag.grid()
            ver3.set('找到文件: OK.')

    elif search_file != '':
        lis = []
        for path in box_list_drive():
            lis.append(check_file( path, search_file ))

        if len(lis):
            for li in lis:
                if len(li):
                    for string_path in li:
                        with open(r'C:\Users\Administrator\Desktop\file.txt', 'a') as fp:
                            fp.write(string_path + '\n' + len(string_path) * '*' + '\n')

                ver3.set('文件查找: OK.')
            # lis.clear()

    else:
        ver3.set('请输入文件名...')

def check_file(Path, search_file):
    """查找文件函数.根据文件后缀名来查找"""
    lis = []
    for PATH in os.listdir(Path)[1:]:
        if PATH.endswith(search_file):
            new_path = PaTh_join( Path, PATH)
            lis.append(new_path)

        # 这里是一个文件夹, 而且开头不等于 System 文件名的路径, 这个文件是系统文件不可以访问
        if os.path.isdir( PaTh_join(Path, PATH)) is not PATH.startswith('System'):
            for feil_jia in os.listdir( PaTh_join(Path, PATH) ):
                if feil_jia.endswith(search_file):
                    new_path = PaTh_join(Path, PATH, feil_jia)
                    lis.append(new_path)

                if os.path.isdir( PaTh_join(Path, PATH, feil_jia)):
                    for file_depth in os.listdir( PaTh_join( Path, PATH, feil_jia)):
                        if file_depth.endswith(search_file):
                            new_path = PaTh_join(Path, PATH, feil_jia, file_depth)
                            lis.append(new_path)
                        if os.path.isdir( PaTh_join(Path, PATH, feil_jia, file_depth) ):
                            for file in os.listdir( PaTh_join(Path, PATH, feil_jia, file_depth) ):
                                if file.endswith(search_file):
                                    new_path = PaTh_join(Path, PATH, feil_jia, file_depth, file)
                                    lis.append(new_path)
                                if os.path.isdir( PaTh_join( Path, PATH, feil_jia, file_depth, file)):
                                    for f in os.listdir( PaTh_join(Path, PATH, feil_jia, file_depth, file) ):
                                        if f.endswith(search_file):
                                            new_path = PaTh_join(Path, PATH, feil_jia, file_depth, file, f)

                                            lis.append(new_path)
    return lis

testCMD = root.register(test)
Label(root, text='原文件名:', fg='red').grid(row=0, sticky=W)
Label(root, text='新文件名:', fg='red').grid(row=1, sticky=W)
Label(root, text='搜索文件:', fg='red').grid(row=2, sticky=W)
Label(root, text='        检测:', fg='red').grid(row=3, sticky=W)

# 输入文本框
ver1 = Entry(root, width=25, font = ('Helvetica', '15', 'bold'),)
ver1.grid(row=0, column=1)

ver2 = Entry(root,  font = ('Helvetica', '15', 'bold'), width=25)
ver2.grid(row=1, column=1)

ver_check = Entry(root,  font = ('Helvetica', '15', 'bold'), width=25)
ver_check.grid(row=2, column=1)

Entry(root, textvariable=ver3, font = ('Helvetica', '15', 'bold'), validate="key", state='disabled',bd = '0',width=25, validatecommand=(testCMD, '%W')).grid(row=3, column=1)

Button(root, text="清 空", width=5, command=show_old, activebackground='red', bd='1').grid(row=0, column=2, ipadx=0, ipady=1)
Button(root, text="清 空", width=5, command=show_new, activebackground='red', bd='1').grid(row=1, column=2, ipadx=0, ipady=1)
Button(root, text="清 空", width=5, command=show_file, activebackground='red', bd='1').grid(row=2, column=2, ipadx=0, ipady=1)
Button(root, text='提交', fg='red',command=creat, width=8,  bd='1').grid(row=4, column=1,columnspan=3, sticky=W, padx=10,pady=5)
Button(root, text='退出', fg='red', width=8, command=root.quit, bd='1').grid(row=4, column=1,sticky=N+S, columnspan=3, padx=10,pady=5)


mainloop()
