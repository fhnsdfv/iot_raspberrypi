# thư viện: vẽ đồ thị, đọc file csv, luồng,...
from functools import partial
from tkinter import * 
from tkinter import messagebox
import matplotlib.figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime
from pandas import read_csv
from matplotlib import pyplot
from threading import Thread
import numpy as np
from mpl_toolkits.axisartist.axislines import Subplot
import serial
import threading
import time
import csv
from datetime import date
from datetime import datetime
from tkinter import ttk
import os
import webbrowser

temperature = -2
humidity = -2
rainfall = -2
dev_sta_1 = -2

win = Tk() #tạo cửa sổ GUI
win.title("IOT") # thiết lập tiêu đề cửa sổ
win.geometry("700x600") # thiết lập kích thước cửa sổ
win.resizable(False, False) # thiết lập không cho phép chỉnh sửa kích thước cửa sổ
menubar = Menu(win) # tạo menu
win.config(menu=menubar)
frame_mon = Frame(win)
frame_con = Frame(win)
frame_exp = Frame(win)


def to_frame_mon(): # hàm chuyển frame giám sát
    win.title("Monitoring")
    win.geometry("1300x600")
    frame_mon.pack(fill='both', expand=1) # đặt frame lên đầu
    frame_con.pack_forget() # ẩn frame
    frame_exp.pack_forget()


def to_frame_con(): # hàm chuyển frame điều khiển
    win.title("Control")
    win.geometry("900x600")
    frame_con.pack(fill='both', expand=1)
    frame_mon.pack_forget()
    frame_exp.pack_forget()


def to_frame_exp(): # hàm chuyển frame xuất file
    win.title("Export")
    win.geometry("900x600")
    frame_exp.pack(fill='both', expand=1)
    frame_mon.pack_forget()
    frame_con.pack_forget()


def to_web(): 
    try:
        webbrowser.open('https://console.thinger.io/dashboards/sensor_dashboard?authorization=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJEYXNoYm9hcmRfc2Vuc29yX2Rhc2hib2FyZCIsInN2ciI6ImFwLXNvdXRoZWFzdC5hd3MudGhpbmdlci5pbyIsInVzciI6Imh1eW5oMTIzNDU2In0.l-Zzw4uP7vspVCHzX0G5iFeVDNZ1O8pZQ4LIOkHVBzk')
        webbrowser.open(
            'https://docs.google.com/spreadsheets/d/1x7WLm7B3yyI-Gr1RqjTotfqBgw-01y_1a6Ps18c1Cx0/edit#gid=1121424198')
    except:
        pass


def to_exit(): # thoát
    if (messagebox.askquestion("Warning", "Exit?", icon="question") == 'yes'):
        quit()

#thêm vào menu
menubar.add_command(label="Monitoring", command=to_frame_mon)
menubar.add_command(label="Control", command=to_frame_con)
menubar.add_command(label="Export", command=to_frame_exp)
menubar.add_command(label="Web", command=to_web)
menubar.add_command(label="Exit", command=to_exit)


def create_frame_mon(): #tạo giao diện giám sát
    label1 = Label(frame_mon, text="Temperature", foreground="red",
                   bg="white", height=2, width=10, font=('Times', 20)) # tạo nhãn dán
    label1.place(x=10, y=20) #đặt nhãn dán ở vị trí x=, y=
    bt1 = Button(frame_mon, text="New", bg="white", command=click_bt1)
    bt1.place(x=210, y=30)

    label2 = Label(frame_mon, text="Humidity", foreground="blue",
                   bg="white", height=2, width=10, font=('Times', 20))
    label2.place(x=650, y=20)
    bt2 = Button(frame_mon, text="New", bg="white", command=click_bt2)
    bt2.place(x=860, y=30)

    label3 = Label(frame_mon, text="Rainfall", foreground="green",
                   bg="white", height=2, width=10, font=('Times', 20))
    label3.place(x=10, y=310)
    bt3 = Button(frame_mon, text="New", bg="white", command=click_bt3)
    bt3.place(x=210, y=320)


def click_bt1(): # hàm khi nhất nút "New" 
    with open("raw_tem.csv", 'w', newline='') as csvfile: #tạo mới file raw_tem.csv
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Time']+['Humidity'])


def click_bt2():
    with open("raw_hum.csv", 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Time']+['Humidity'])


def click_bt3():
    with open("raw_rain.csv", 'w', newline='') as csvfile:
        spamwriter = csv.writer(csvfile, delimiter=',',
                                quoting=csv.QUOTE_MINIMAL)
        spamwriter.writerow(['Time']+['Humidity'])


def create_frame_con(): # tạo frame điều khiển
    font1 = Label(frame_con, bg="white", height=10, width=30)
    font1.place(x=40, y=30)
    lb_dv1 = Label(frame_con, text="Device 1", bg="white", font=('Times', 24))
    lb_dv1.place(x=40, y=30)


create_frame_con() #gọi hàm


def update_bt_con1(): # hàm ấn nút điều khiển thiết bị
    global bt_con1, dev_sta_1
    file_data = open("cur_data.txt", "r") # mở file
    data = file_data.read()
    file_data.close() #đóng file
    try: 
        temperature, humidity, rainfall, dev_sta_1 = data.split(',') #tách dữ liệu
    except:
        pass
    bt_con1 = Button(frame_con, font=('Times', 18), width=5, height=1, command=click_bt_con1)
    #print(dev_sta_1)
    if (dev_sta_1 == "1"): # điều chỉnh text của nút nhấn
        bt_con1["text"] = "Tắt"
    elif (dev_sta_1 == "0"):
        bt_con1["text"] = "Bật"
    bt_con1.place(x=100, y=90)
    #print(bt_con1["text"])
    win.after(700, update_bt_con1)

def click_bt_con1(): #hàm gửi dữ liệu khi nhấn nút điều khiển thiết bị
    if (bt_con1['text'] == "Bật"):
        bt_con1['text'] = "Tắt"
    else:
        bt_con1['text'] = "Bật"
    f = open("device1.txt", "r")
    data = f.read()
    f.close()
    f = open("device1.txt", "w")
    if (data=="1"):
        f.write("0")
    elif (data=="0"):
        f.write("1")
    f.close()
    bt_con1["state"] = "disabled"
    time.sleep(1)
    bt_con1["state"] = "active"

update_bt_con1()

def create_frame_exp(): #tạo frame xuất file
    global sel_cb
    lb_titile = Label(frame_exp, text="Please select a file:")
    lb_titile.pack(fill=X, padx=5, pady=5)
    selected_month = StringVar()
    sel_cb = ttk.Combobox(frame_exp, textvariable=selected_month)
    sel_cb.pack(fill=X, padx=5, pady=5)
    dir_list = os.listdir('data') # danh sách file
    sel_cb['values'] = dir_list
    bt = Button(frame_exp, text='OK', command=open_file) 
    bt.pack()


def open_file(): # hàm mở file
    global sel_cb
    link = str('geany data/')+str(sel_cb.get())
    try:
        os.system(link)
    except:
        pass


def update_chart(): # hàm vẽ đồ thị donut
    global fig1, fig2, fig3, temperature, humidity, rainfall, dev_sta_1, temp_text, hum_text, rain_text
    file_data = open("cur_data.txt", "r")
    data = file_data.read()
    file_data.close()
    try:
        temperature, humidity, rainfall, dev_sta_1 = data.split(',')
        temperature = float(temperature)
        humidity = float(humidity)
        rainfall = float(rainfall)
    except:
        pass
    try: #xóa biểu đồ cũ
        fig1.get_tk_widget().place_forget()
        fig2.get_tk_widget().place_forget()
        fig3.get_tk_widget().place_forget()
        temp_text.place_forget()
        hum_text.place_forget()
        rainfall.place_forget()
    except:
        pass
    # Chart 1: nhiệt độ
    fig1 = matplotlib.figure.Figure(figsize=(2.1, 2.1), dpi=100) # kích cỡ
    ax1 = fig1.add_subplot(111)
    ax1.pie([abs(temperature), (100-abs(temperature))], colors=["red", "gray"])
    circle1 = matplotlib.patches.Circle((0, 0), 0.8, color='white')
    ax1.add_artist(circle1)
    canvas1 = FigureCanvasTkAgg(fig1, master=frame_mon)
    canvas1.get_tk_widget().place(x=10, y=70)
    temp_text = Label(frame_mon, text=(str(temperature)+"°C"),
                      bg="white", fg="red", font=('Times', 18))
    if (temperature < 0):
        temperature = 0
        temp_text['text'] = "Erorr"
    temp_text.place(x=75, y=160)

    # Chart 2: độ ẩm
    fig2 = matplotlib.figure.Figure(figsize=(2.1, 2.1), dpi=100)
    ax2 = fig2.add_subplot(111)
    ax2.pie([abs(humidity), (100-abs(humidity))], colors=["blue", "gray"])
    circle2 = matplotlib.patches.Circle((0, 0), 0.8, color='white')
    ax2.add_artist(circle2)
    canvas2 = FigureCanvasTkAgg(fig2, master=frame_mon)
    canvas2.get_tk_widget().place(x=650, y=70)
    hum_text = Label(frame_mon, text=(str(humidity)+"%"),
                     bg="white", fg="red", font=('Times', 18))
    if (humidity < 0):
        hum_text['text'] = "Erorr"
        humidity = 0
    hum_text.place(x=720, y=160)

    # Chart 3: lượng mưa
    fig3 = matplotlib.figure.Figure(figsize=(2.1, 2.1), dpi=100)
    ax3 = fig3.add_subplot(111)
    ax3.pie([abs(rainfall)/10, (100-abs(rainfall)/10)], colors=["green", "gray"])
    circle3 = matplotlib.patches.Circle((0, 0), 0.8, color='white')
    ax3.add_artist(circle3)
    canvas = FigureCanvasTkAgg(fig3, master=frame_mon)
    canvas.get_tk_widget().place(x=10, y=360)
    rain_text = Label(frame_mon, text=(str(rainfall)+"mm"),
                      bg="white", fg="red", font=('Times', 16))
    if (rainfall < 0):
        rain_text['text'] = "Erorr"
        rainfall = 0
    rain_text.place(x=73, y=455)

    win.after(5000, update_chart) # update biểu đồ sau 5s


def update_series_chart(): # vẽ biểu đồ theo thời gian
    global line1, line2, line3
    try:
        line1.get_tk_widget().place_forget()
        line2.get_tk_widget().place_forget()
        line3.get_tk_widget().place_forget()
    except:
        pass
    seri1 = matplotlib.figure.Figure(figsize=(4.2, 2.1), dpi=100)
    ay1 = Subplot(seri1, 111)
    seri1.add_subplot(ay1)
    line1 = FigureCanvasTkAgg(seri1, master=frame_mon)
    line1.get_tk_widget().place(x=210, y=70)
    dataArray = np.genfromtxt('raw_tem.csv', delimiter=',', names=True)
    for col_name in dataArray.dtype.names:
        ay1.plot(dataArray[col_name], label=col_name, color='red')
    ay1.axis["right"].set_visible(False)
    ay1.axis["top"].set_visible(False)

    seri2 = matplotlib.figure.Figure(figsize=(4.2, 2.1), dpi=100)
    ay2 = Subplot(seri2, 111)
    seri2.add_subplot(ay2)
    line2 = FigureCanvasTkAgg(seri2, master=frame_mon)
    line2.get_tk_widget().place(x=850, y=70)
    dataArray = np.genfromtxt('raw_hum.csv', delimiter=',', names=True)
    for col_name in dataArray.dtype.names:
        ay2.plot(dataArray[col_name], label=col_name, color='blue')
    ay2.axis["right"].set_visible(False)
    ay2.axis["top"].set_visible(False)

    seri3 = matplotlib.figure.Figure(figsize=(4.2, 2.1), dpi=100)
    ay3 = Subplot(seri3, 111)
    seri3.add_subplot(ay3)
    line3 = FigureCanvasTkAgg(seri3, master=frame_mon)
    line3.get_tk_widget().place(x=210, y=360)
    dataArray = np.genfromtxt('raw_rain.csv', delimiter=',', names=True)
    for col_name in dataArray.dtype.names:
        ay3.plot(dataArray[col_name], label=col_name, color='green')
    ay3.axis["right"].set_visible(False)
    ay3.axis["top"].set_visible(False)

    win.after(5000, update_series_chart)


update_chart()
update_series_chart()

create_frame_mon()
create_frame_exp()
to_frame_mon()

win.mainloop() # vòng lặp chính
