import statistics
import time
from tkinter import *
import tkinter as tk
from tkinter import filedialog,scrolledtext
from tkinter.messagebox import showerror, showinfo

import numpy as np
from pyecharts.charts import Bar,Line
from ndsi import *
from pyecharts import options as opts

from snapshot_phantomjs import snapshot
from pyecharts.render import make_snapshot
from precision_analysis import precision
s1 = 'GFSI的最大值：'
s2 = 'GFSI的最小值：'
s3 = '总像元数量：'
s4 = 'Nodata数量：'
s5 = '有意义的像元数量：'
s6 = '雪的像元数量：'
s7 = '陈雪的像元数量：'
s8 = '新雪的像元数量：'
s9 = '非雪的像元数量：'
s10 = '雪的占比(%)：'
s11 = '新雪的占比(%)：'
s12 = '陈雪的占比(%)：'
s13 = '非雪的占比(%)：'

s = [s1, s2, s3, s4, s5, s6, s7, s8, s9]
c = [s10, s11, s12, s13]
x=[]
class Page_mian(object):#主界面，简短介绍加功能按钮
    def go_Page1(self):
        self.root.destroy()
        Page_1()

    def go_Page2(self):
        self.root.destroy()
        Page_2()

    def __init__(self):
        self.root=tk.Tk()
        self.root.title('积雪覆盖处理系统')
        FrameUP=tk.Frame(self.root)
        FrameUP.pack()
        lab1=tk.Label(FrameUP,text='欢迎使用积雪覆盖处理系统',font='Times 20 bold',fg='green',height=2)
        lab1.pack(anchor='n')
        lab2=tk.Label(FrameUP,text='功能简介：通过上传玛纳斯流域的遥感影像，可以对其积雪覆盖面积进行提取',font='Times 15 bold',fg='black',height=2)
        lab2.pack(anchor='n')
        lab3=tk.Label(FrameUP,text='单时相分析：提取单时相积雪覆盖度，并分析结果',font='Times 15 bold',fg='blue')
        lab3.pack(anchor='w')
        lab4=tk.Label(FrameUP,text='多时相分析：提取多时相积雪覆盖度，并分析结果',font='Times 15 bold',fg='blue',pady=50)
        lab4.pack(anchor='w')
        lab5=tk.Label(FrameUP,text='',font='Times 15 bold')
        lab5.pack(anchor='w')
        B = tk.Button(FrameUP, text="单时相分析", font='Times 15 bold',fg='blue',width=10,height=2,background='white',command=self.go_Page1)
        B.pack(side='left',anchor='n')
        c = tk.Button(FrameUP, text="多时相分析", font='Times 15 bold',fg='blue',width=10,height=2,background='white',command=self.go_Page2)
        c.pack(anchor='ne')
        screen_width,screen_height = self.root.maxsize()#获取屏幕最大长宽
        w = int((screen_width-1080)/2)
        h = int((screen_height-900)/2)
        self.root.geometry(f'1080x900+{w}+{h}')#设置窗口大小为1080*900，调整位置居中
        self.root.mainloop()

class Page_1():#功能一界面


    def go_pagemian(self):
        self.root.destroy()
        Page_mian()





    def __init__(self):
        def open_tb(file):
            open(file)
#entry_filename为输入的遥感影像路径
#input_filename为生成的遥感影像路径
#entry_csvname为精度文件的路径


        def open_file():
            filename = filedialog.askopenfilename(title='打开tif文件', filetypes=[('*', '*.*')])
            entry_filename.insert('insert', filename)

        def open_csv():
            filename = filedialog.askopenfilename(title='选择csv文件', filetypes=[('*', '*.csv')])
            entry_csvname.insert('insert', filename)


        def start():#开始提取，提取出积雪覆盖的遥感影像
            a = entry_filename.get()

            if a.endswith(('tif','tiff')):
                start=time.time()
                c=ndsi(a,a)
                output_file.set(c)
                end = time.time()
                Y_time = end - start
                mx4 = showinfo(title='用时', message='解析成功，共用时：' + str(Y_time) + 's')
                tk.Button(self.root, command=mx4).pack(padx=10, pady=5, anchor='w')  # 弹出共用时多久

            else:
                mx3 = showerror(title='错误消息框', message='文件格式非法')
                tk.Button(self.root, text='错误消息框', command=mx3).pack(padx=10, pady=5, anchor='w')

        def looktif():#用opencv打开生成的积雪覆盖遥感图像
            file=input_filename.get()
            if file.endswith(('tif','tiff')):
                img = cv.imread(file, 11)
                print(img)
                print(img.shape)
                print(img.dtype)
                print(img.min())
                print(img.max())
                # 创建窗口并显示图像
                cv.namedWindow("image", cv.WINDOW_NORMAL)
                cv.imshow("image", img)
                cv.waitKey(0)
                # 释放窗口
                cv.destroyAllWindows()
            else:
                mx3 = showerror(title='错误消息框', message='文件格式非法')
                tk.Button(self.root, text='错误消息框', command=mx3).pack(padx=10, pady=5, anchor='w')

        def anysis():#分析积雪覆盖的遥感图像把一些参数显示出来
            file = input_filename.get()
            csvname=entry_csvname.get()

            ndsi_num, ndsi_per,Bfile = ndsi_analyse(file)
            if file.endswith(('tif','tiff')):
                start=time.time()
                for i in range(9):
                    text.insert(INSERT, s[i])
                    text.insert(INSERT, ndsi_num[i])
                    text.insert(INSERT, '\n')
                for i in range(4):
                    text.insert(INSERT, c[i])
                    text.insert(INSERT, ndsi_per[i])
                    text.insert(INSERT, '\n')

                l1 = ["雪", "新雪", "陈雪", "非雪"]
#D:\PythonProject\NDSI_GF_WFV\20220412205755_NDSI.tiff
                bar = (
                    Bar()
                        .add_xaxis(l1)
                        .add_yaxis("比例", ndsi_per)
                        .set_global_opts(title_opts=opts.TitleOpts(title="积雪比例柱状图", subtitle="天山玛纳斯流域"))
                )
                bar.render(r'D:\PythonProject\Snow_GF_WFV\bar.html')
                pfile=file.split('.')[0]+'.gif'
                make_snapshot(snapshot, bar.render(), pfile)
                if csvname.endswith('csv'):
                    prep = precision(file, csvname)
                    text.insert(INSERT, '精度(%):' + str(prep) + '\n')



                text.insert(INSERT,'积雪比例柱状图路径：'+pfile+'\n')
                text.insert(INSERT, '二值图像路径：' + Bfile)

                end = time.time()
                Y_time = end - start
                mx4 = showinfo(title='用时', message='解析成功，共用时：' + str(Y_time) + 's')
                tk.Button(self.root, command=mx4).pack(padx=10, pady=5, anchor='w')  # 弹出共用时多久



            else:
                mx3 = showerror(title='错误消息框', message='文件格式非法')
                tk.Button(self.root, text='错误消息框', command=mx3).pack(padx=10, pady=5, anchor='w')

        self.root=tk.Tk()
        self.root.title('单时相分析')
        FrameUP=tk.Frame(self.root)
        FrameUP.grid(row=0,sticky='nw',ipady=15)
        Frame2 = tk.Frame(self.root)
        Frame2.grid(row=1,sticky='nw')
        Frame3 = tk.Frame(self.root)
        Frame3.grid(row=2,columnspan=1,sticky='nw')
        Frame4 = tk.Frame(self.root)
        Frame4.grid(row=3,sticky='n')
        Frame5 = tk.Frame(self.root)
        Frame5.grid(row=4, sticky='nw')
        Frame6 = tk.Frame(self.root)
        Frame6.grid(row=5, sticky='n')
        Frame7 = tk.Frame(self.root)
        Frame7.grid(row=6,columnspan=1, sticky='nw')

        Frame8 = tk.Frame(self.root)
        Frame8.grid(row=7, sticky='nw')
        Frame9 = tk.Frame(self.root)
        Frame9.grid(row=8, columnspan=1, sticky='n')

        Frame10= tk.Frame(self.root)
        Frame10.grid(row=9, columnspan=1, sticky='nw')


        B = tk.Button(FrameUP, text="返回主界面", font='Times 15 bold',fg='black',width=10,background='white',command=self.go_pagemian)
        B.pack()
        input_B = tk.Button(Frame2, text="上传遥感影像", font='Times 15 bold', fg='blue', width=10,  background='white',
                      command=open_file)
        input_B.pack()

        entry_filename = tk.Entry(Frame3, width=80, font=("宋体", 20, 'bold'))
        entry_filename.pack(side='left')

        input_start = tk.Button(Frame4, text="开始提取", font='Times 15 bold', fg='blue', width=10,
                            background='white',
                            command=start)
        input_start.pack()

        input_C = tk.Button(Frame5, text="打开生成的影像", font='Times 15 bold', fg='blue', width=15, background='white',
                            command=looktif)
        input_C.pack()


        output_file = tk.StringVar()
        input_filename = tk.Entry(Frame6, width=80, font=("宋体", 20, 'bold'),textvariable=output_file)
        input_filename.pack()



        input_D = tk.Button(Frame7, text="上传精度分析文件", font='Times 15 bold', fg='blue', width=15, background='white',
                            command=open_csv)
        input_D.pack()
        entry_csvname = tk.Entry(Frame8, width=80, font=("宋体", 20, 'bold'))
        entry_csvname.pack(side='left')

        input_d = tk.Button(Frame9, text="结果分析", font='Times 15 bold', fg='blue', width=10, background='white',
                            command=anysis)
        input_d.pack()


        text = tk.Text(Frame10,  undo=True,width=75, autoseparators=False,wrap='word',font=("宋体", 20, 'bold'))
        # 适用 pack(fill=X) 可以设置文本域的填充模式。比如 X表示沿水平方向填充，Y表示沿垂直方向填充，BOTH表示沿水平、垂直方向填充
        text.pack(fill='x')
        # INSERT 光标处插入；END 末尾处插入
        text.insert(INSERT, '结果显示区域\n')
        screen_width,screen_height = self.root.maxsize()#获取屏幕最大长宽
        w = int((screen_width-1080)/2)
        h = int((screen_height-900)/2)
        self.root.geometry(f'1080x900+{w}+{h}')#设置窗口大小为1080*900，调整位置居中
        self.root.mainloop()


class Page_2():#功能二的实现页面
    def go_pagemian(self):
        self.root.destroy()
        Page_mian()

    def __init__(self):

        def upload_files():#上传多个文件，和按钮绑定
            selectFiles = tk.filedialog.askopenfilenames(
                title='可选择1个或多个文件')  # askopenfilename 1次上传1个；askopenfilenames1次上传多个
            for selectFile in selectFiles:
                text1.insert(tk.END, selectFile + '\n')  # 更新text中内容
                text1.update()


        def print_file():#读取多个文件，如果文件都合法进行批量处理
            count=0
            a = text1.get('1.0','end')  # 用get提取entry中的内容
            x=(a.strip()).split('\n')#去除多余的空白，用\n来把文件分开
            File_num=len(x)
            for i in range(File_num):#看一下文件是不是都是栅格文件
                if x[i].endswith(('tif','tiff')):
                    count=count+1
            if count==File_num:#如果都是矢量文件，就开始批量处理
                start=time.time()
                for i in range(File_num):
                    new_file_name=ndsi(x[i],x[i])
                    text2.insert(INSERT, new_file_name + '\n')
                end=time.time()
                Y_time=end-start
                mx4 = showinfo(title='用时', message='解析成功，共用时：'+str(Y_time)+'s')
                tk.Button(self.root,  command=mx4).pack(padx=10, pady=5, anchor='w')#弹出共用时多久

            else:#不是我就弹窗哭
                mx3 = showerror(title='错误消息框', message='文件格式非法')
                tk.Button(self.root, text='错误消息框', command=mx3).pack(padx=10, pady=5, anchor='w')



        def anysis_many():#对一堆遥感图像进行分析
            text.configure(state=tk.NORMAL)
            gfsi_max=[]
            gfsi_min=[]
            snow_per=[]
            new_snow_per = []
            past_snow_per = []
            none_snow_per = []
            a = text2.get('1.0', 'end')  # 用get提取生成的积雪文件
            filenames = (a.strip()).split('\n')#把积雪文件用\n分开，写入数组
            file_num=len(filenames)#共有多少个文件
            a = text1.get('1.0', 'end')  # 用get提取entry中的内容
            fn = (a.strip()).split('\n')
            timess=[]
            for i in fn:
                fff = i[-18:-8]
                timess.append(fff)
            start = time.time()
            for i in range(file_num):
                num=i+1
                text.insert(INSERT, '-------↓↓↓↓↓第'+str(num)+'幅图分析结果↓↓↓↓↓---------\n')
                file_np,file_per,bf=ndsi_analyse(filenames[i])
                gfsi_max.append(file_np[0])
                gfsi_min.append(file_np[1])
                snow_per.append(file_per[0])
                new_snow_per.append(file_per[1])
                past_snow_per.append(file_per[2])
                none_snow_per.append(file_per[3])



                for i in range(9):
                    text.insert(INSERT, s[i])
                    text.insert(INSERT, file_np[i])
                    text.insert(INSERT, '\n')
                for i in range(4):
                    text.insert(INSERT, c[i])
                    text.insert(INSERT, file_per[i])
                    text.insert(INSERT, '\n')
                text.insert(INSERT, '-------↑↑↑↑↑第' + str(num) + '幅图分析结果↑↑↑↑↑---------\n\n')
            line = (
                Line()
                    .add_xaxis(timess)
                    .add_yaxis(series_name="总积雪", y_axis=snow_per, is_smooth=True, symbol='circle',symbol_size=10)
                    .add_yaxis(series_name="新雪", y_axis=new_snow_per, is_smooth=True,symbol='rect',symbol_size=10)
                    .add_yaxis(series_name="陈雪", y_axis=past_snow_per, is_smooth=True,symbol='roundRect',symbol_size=10)
                    .add_yaxis(series_name="非雪", y_axis=none_snow_per, is_smooth=True,symbol='triangle',symbol_size=10)
                    .set_global_opts(title_opts=opts.TitleOpts(title="积雪变化折线图"))
                    .set_global_opts(xaxis_opts=opts.AxisOpts(name='Year_Month_Day',name_location='center',name_gap = 35))
                    .set_global_opts(yaxis_opts=opts.AxisOpts(name='Percentage(%)'))
            )
            line.render('D:\PythonProject\Snow_GF_WFV\line.html')

            pfile = filenames[0].split('.')[0] + '.gif'
            make_snapshot(snapshot, line.render(), pfile)
            iput1='最大的GFSI值为：'+str(max(gfsi_max))+'-----'+'图像是第'+str(np.argmax(gfsi_max)+1)+'幅'
            iput2='最小的GFSI值为：'+str(min(gfsi_min))+'-----'+'图像是第'+str(np.argmin(gfsi_min)+1)+'幅'
            iput3='最大积雪覆盖率：'+str(max(snow_per))+'-----'+'图像是第'+str(np.argmax(snow_per)+1)+'幅'
            iput4='最小积雪覆盖率：'+str(min(snow_per))+'-----'+'图像是第'+str(np.argmin(snow_per)+1)+'幅'
            iput5='平均的积雪覆盖率：'+str(statistics.mean(snow_per))
            text.insert(INSERT,iput1+'\n')
            text.insert(INSERT, iput2 + '\n')
            text.insert(INSERT, iput3 + '\n')
            text.insert(INSERT, iput4 + '\n')
            text.insert(INSERT, iput5 + '\n')
            text.insert(INSERT, '积雪比例折线图路径：' + pfile+'\n\n')
            text.see(END)
            end = time.time()
            Y_time = end - start
            mx4 = showinfo(title='用时', message='解析成功，共用时：' + str(Y_time) + 's')
            tk.Button(self.root, command=mx4).pack(padx=10, pady=5, anchor='w')  # 弹出共用时多久



















        self.root=tk.Tk()
        self.root.title('多时相分析')
        FrameUP=tk.Frame(self.root)
        FrameUP.grid(row=0,sticky='nw',ipady=15)

        Frame2 = tk.Frame(self.root)
        Frame2.grid(row=1,sticky='nw')
        Frame3 = tk.Frame(self.root)
        Frame3.grid(row=2,columnspan=1,sticky='nw')

        Frame4 = tk.Frame(self.root)
        Frame4.grid(row=3,sticky='nw')

        Frame5 = tk.Frame(self.root)
        Frame5.grid(row=4, sticky='nw')
        Frame6 = tk.Frame(self.root)
        Frame6.grid(row=5, sticky='nw')
        Frame7 = tk.Frame(self.root)
        Frame7.grid(row=6,columnspan=1, sticky='nw')


        B = tk.Button(FrameUP, text="返回主界面", font='Times 15 bold',fg='black',width=10,background='white',command=self.go_pagemian)
        B.pack()


        input_B = tk.Button(Frame2, text="上传遥感影像", font='Times 15 bold', fg='blue', width=10,  background='white',
                      command=upload_files)
        input_B.pack()

        text1 = tk.Text(Frame3, width='80', height='10',font='Times 12 bold')
        text1.grid()



        input_start = tk.Button(Frame4, text="开始提取", font='Times 15 bold', fg='blue', width=10,
                            background='white',
                            command=print_file)
        input_start.pack()

        text2 = tk.Text(Frame5, width='80', height='10',font='Times 12 bold')
        text2.grid()





        input_d = tk.Button(Frame6, text="结果分析", font='Times 15 bold', fg='blue', width=10, background='white',command=anysis_many)
        input_d.pack()
        text = tk.Text(Frame7, font=("宋体", 15, 'bold'))
        scr1 = Scrollbar(Frame7)  # 垂直滚动条
        scr1.pack(side=RIGHT, fill=Y)  # 靠右，上下扩展


        text.config(yscrollcommand=scr1.set)  # 多行文本框绑定垂直滚动条的Set
        scr1.config(command=text.yview)  # 垂直滚动条的command绑定文本框的yview
        # 适用 pack(fill=X) 可以设置文本域的填充模式。比如 X表示沿水平方向填充，Y表示沿垂直方向填充，BOTH表示沿水平、垂直方向填充
        text.pack(fill='both')
        # INSERT 光标处插入；END 末尾处插入
        text.insert(INSERT, '结果显示区域\n')




        screen_width,screen_height = self.root.maxsize()#获取屏幕最大长宽
        w = int((screen_width-1080)/2)
        h = int((screen_height-1080)/2)
        self.root.geometry(f'1080x1080+{w}+{h}')#设置窗口大小为1080*900，调整位置居中
        self.root.mainloop()
if __name__ == '__main__':
    Page_mian()