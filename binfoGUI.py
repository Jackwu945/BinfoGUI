from tkinter import *
from tkinter import ttk
import tkinter
import search
import os
from PIL import Image, ImageTk
import webbrowser
import time
import threading

global h
# 搜索下一个时列表索引值
index = 2


def basic_info():
    threading.Thread(target=roll).start()
    global h
    # 用户单击查询则查找下一个清零
    index = 2
    # 避免返回值为错误时按钮仍可点导致出错
    buttonopen['state'] = "disable"
    # 运行search.py的主函数，传入entry获得的字符串，
    # 返回值是一个元组，0是返回内容，1是https
    app.update()
    returntxt = search.mainSub(entry.get())
    # 通过正则去除\n
    # 如果是元组，则拆开
    try:
        returntxt = returntxt.translate(str.maketrans('', '', r'\n'))
    except:
        h = returntxt[1]
        returntxt = returntxt[0].translate(str.maketrans('', '', r'\n'))
    # 吧返回的字符串设置在info中
    info.set(returntxt)
    # 如果返回字符串不是出错，则使两个按钮变为可用状态
    if returntxt != 'b站没有此番（IdexError）Tips:假如是隐藏番剧，请输入全名，你也可以选择在m站搜索' and returntxt != '网络错误或服务端网络错误。（requests.exceptions.ConnectionError）':
        buttonopen['state'] = "active"
        buttonnext['state'] = "active"
        buttonbimi['state'] = "active"


def next_info():
    threading.Thread(target=roll).start()
    buttonopen['state'] = "disable"
    buttonnext['state'] = "disable"
    global hn
    global index
    # 获得entry的字符串
    now = entry.get()
    # 全局化变量供下方使用
    global last
    global index
    #如果索引大于三且之前获得的输入不等于现在获得的输入（判断用户是否更改输入），则索引重新设置。
    if index >3:
        if last != now:
            #索引值设为2而不是三虽然会导致用户更改输入后点下一个无法看到1的内容，但是能无缝衔接查询按钮，毕竟没有哪个人会这么SB。
            index=2

    # 避免返回值为错误时按钮仍可点导致出错
    buttonopen['state'] = "disable"
    # 返回值是一个元组，0是返回内容，1是https
    app.update()
    returntxt = search.get_next(entry.get(), index)
    # 如果是元组，则拆开
    try:
        returntxt = returntxt.translate(str.maketrans('', '', r'\n'))
    except:
        hn = returntxt[1]
        returntxt = returntxt[0].translate(str.maketrans('', '', r'\n'))

    last = entry.get()
    info.set(returntxt)
    if returntxt != '到底啦。（IndexError）' and returntxt != '网络错误或服务端网络错误。（requests.exceptions.ConnectionError）':
        buttonopen['state'] = "active"
        buttonnext['state'] = "active"
        buttonbimi['state'] = "active"
    if returntxt == '到底啦。（IdexError）':
        index = 1
        buttonnext['state'] = "disable"
        buttonopen['state'] = "disable"
        buttonbimi['state'] = "active"
    # 每次查完索引自增1
    index += 1


def op():
    global ol
    if index <= 2:
        for i in range(len(h)):
            if h[i]=='"':
                ol= h[0:i]
                break
            #假如字符串正常，直接赋值
            ol=h
        webbrowser.open(ol)

    else:
        print(hn)
        webbrowser.open(hn)

def openm():
    keyword=entry.get()
    error=search.openbimi(keyword)
    info.set(error)

def bimiinfo():
    # 避免返回值为错误时按钮仍可点导致出错
    buttonopen['state'] = "disable"
    # 运行search.py的bimi查询函数，传入entry获得的字符串，
    returntxt = search.bimisearch(entry.get())
    info.set(returntxt)
    # 如果返回字符串不是出错，则使两个按钮变为可用状态
    if returntxt != '泪目，m站也没有':
        buttonbimi['state'] = "active"

def roll():
    for i in range(100):
        mpb["value"] = i + 25
        app.update()
        time.sleep(0.0001)
        if i == 90:
            while True:
                if info.get() != "I am a console.\n你望着我，我也望着你~~":
                    break
            for i in range(10):
                mpb["value"] = i + 1
                app.update()
                time.sleep(0.001)


# 实例化TK类
app = Tk()
app.geometry('800x650')
app.wm_title('番剧信息获取 By Jack')

# 设置图标
dirpath = os.path.abspath(os.path.dirname(__file__))
try:
    # WINDOWS用户
    app.iconbitmap(default = dirpath+r'\img\favicon.ico')
except:
    #LINUX用户
    im = Image.open(dirpath+ r'/img/favicon.ico')
    img = ImageTk.PhotoImage(im)
    app.tk.call('wm', 'iconphoto', app._w, img)

# 设置bg
canvas = tkinter.Canvas(app, width=1200,height=699,bd=0, highlightthickness=0)
# 图片路径
try:
    # WINDOWS用户
    dp=dirpath + r'\img\bg.jpg'
    img = Image.open(dp)
    photo = ImageTk.PhotoImage(img)
except:
    # LINUX用户
    dp=dirpath + r'/img/bg.png'
    img = Image.open(dp)
    photo = ImageTk.PhotoImage(img)

canvas.create_image(310, 400, image=photo)
canvas.place(x=0,y=0)


# # 主标题
label = Label(
    app,
    text='番剧信息获取',
    font=('微软雅黑', '28', 'bold')
)
label.pack(pady=20)

# 输入框
entry = Entry(
    app, bd=3, font=('楷体', '14')
)
entry.place(width=525, height=50, x=10, y=100, anchor='nw')
entry.insert(0, "在这里输入番剧名称...")

# 该按钮连接到basic_info函数
button = Button(app, text='点我查询', font=('楷体', '28'), command=basic_info)
button.place(x=550, y=100, width=200, height=50)

# 这个flag供下方使用，设计之初是为上方函数服务的，现在懒得改了
flag = 'disable'

# 该按钮连接到next_info函数
button_search_bimi = Button(app, text='m站查询', font=('楷体', '20'), command=bimiinfo)
button_search_bimi.place(x=575, y=200, width=150, height=50)

# 该按钮连接到next_info函数
buttonnext = Button(app, text='查找下一个', font=('楷体', '20'), command=next_info, state=flag)
buttonnext.place(x=575, y=275, width=150, height=50)

# 该按钮连直接连接到search.py中的open函数
buttonopen = Button(app, text='B站打开', font=('楷体', '24'), command=op, state=flag)
buttonopen.place(x=575, y=350, width=150, height=50)

# 该按钮连接到openm函数
buttonbimi = Button(app, text='M站打开', font=('楷体', '20'), command=openm, state=flag)
buttonbimi.place(x=575, y=425, width=150, height=50)

# 该变量供上方传字符串与下方设置字符串使用
info = StringVar()

# 设置信息框
msg = Message(app, font=('楷体', '12'), textvariable=info)
# 设置务必要在放置之前完成
info.set("I am a console.\n你望着我，我也望着你~~")
msg.place(x=10, y=175, width=525, height=415)

mpb = ttk.Progressbar(app, orient="horizontal", length=200, mode="determinate")
mpb.place(x=10,y=600,width=550,height=35)
mpb["maximum"] = 100
mpb["value"] = 0

# 刷新
app.mainloop()
