import os #thư viện để điều khiển bật file
import serial # để giao tiếp với arduino 
import threading # để tạo luồng xử lý
import time # dùng để ngắt
import csv # đọc, viết file .csv
from datetime import date
from datetime import datetime #thời gian thực
import webbrowser # mở web

# nhập thư viện

f1 = open("device1.txt", "w")
f1.write("0")
f1.close()
data1_pre = "0" 

try:
    ser = serial.Serial('/dev/ttyUSB0',115200) #tạo cổng kết nối với arduino
except:
    print("Lỗi kết nối với arduino") #lỗi


def to_web(): # mở web
    try:
        webbrowser.open('https://console.thinger.io/dashboards/sensor_dashboard?authorization=eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJqdGkiOiJEYXNoYm9hcmRfc2Vuc29yX2Rhc2hib2FyZCIsInN2ciI6ImFwLXNvdXRoZWFzdC5hd3MudGhpbmdlci5pbyIsInVzciI6Imh1eW5oMTIzNDU2In0.l-Zzw4uP7vspVCHzX0G5iFeVDNZ1O8pZQ4LIOkHVBzk')
        webbrowser.open(
            'https://docs.google.com/spreadsheets/d/1x7WLm7B3yyI-Gr1RqjTotfqBgw-01y_1a6Ps18c1Cx0/edit#gid=1121424198')
        print("Đã mở web")
    except:
        pass


def new_raw_tem(): # tạo file để vẽ biểu đồ nhiệt độ
    try:
        with open("raw_tem.csv", 'r', newline='') as csvfile: #kiểm tra xem file raw_tem.csv có tồn tại hay không
            pass
    except:# nếu không
        with open("raw_tem.csv", 'w', newline='') as csvfile: # tạo file raw_tem.csv viết header vào file
            spamwriter = csv.writer(
                csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['Time']+['Temperature'])


def new_raw_hum(): # tạo file để vẽ biểu đồ độ ẩm
    try:
        with open("raw_hum.csv", 'r', newline='') as csvfile:
            pass
    except:
        with open("raw_hum.csv", 'w', newline='') as csvfile:
            spamwriter = csv.writer(
                csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['Time']+['Humidity'])


def new_raw_rain(): # tạo file để vẽ biểu đồ lượng mưa
    try:
        with open("raw_rain.csv", 'r', newline='') as csvfile:
            pass
    except:
        with open("raw_rain.csv", 'w', newline='') as csvfile:
            spamwriter = csv.writer(
                csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
            spamwriter.writerow(['Time']+['Rain flow'])


new_raw_hum()
new_raw_tem()
new_raw_rain()

# Khởi tạo biến global
temperature = -2 # nhiệt độ
humidity = -2 # độ ẩm
rainfall = -2 # lượng mưa
dev_sta_1 = -2 # trạng thái thiết bị


def rec_data(): # hàm nhận dữ liệu từ arduino
    global data_rec, temperature, humidity, dev_sta_1, rainfall, cur_date, cur_time # khai báo sử dụng biến globbal
    while True: 
        try:
            if ser.in_waiting: # kiểm tra xem có dữ liệu gửi về không
                data_rec = ser.readline() # đọc, dịch dữ liệu
                data_rec = data_rec.decode('utf').rstrip('\n')
                cur_date = 'data/' + \
                    str(date.today().strftime("%d.%m.%Y"))+'.csv'
                cur_time = str(datetime.now().strftime("%H:%M:%S")) # lấy ngày hiện tại để lưu vào lịch sử dữ liệu
                #print(data_rec)
                # Data nhận có dạng: A27.10B80.00C0D0$
                try:
                    with open(cur_date, 'r', newline='') as csvfile: #tạo file lưu dữ liệu nếu không có
                        pass
                except:
                    with open(cur_date, 'w', newline='') as csvfile:
                        spamwriter = csv.writer(
                            csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                        spamwriter.writerow(
                            ['Time']+['Temperature']+['Humidity']+['Rain flow']) #ghi header
                new_raw_hum()
                new_raw_tem()
                new_raw_rain()
                if (data_rec.startswith('A') == True): #tách dữ liệu nhận được nếu có lỗi gán giá trị là -2
                    try:
                        temperature = float(
                            data_rec[data_rec.index('A')+1:data_rec.index('B')])
                    except:
                        temperature = -2
                    try:
                        humidity = float(
                            data_rec[data_rec.index('B')+1:data_rec.index('C')])
                    except:
                        humidity = -2
                    try:
                        rainfall = float(
                            data_rec[data_rec.index('C')+1:data_rec.index('D')])
                    except:
                        rainfall = -2
                    try:
                        dev_sta_1 = int(
                            data_rec[data_rec.index('D')+1:data_rec.index('$')])
                    except:
                        dev_sta_1 = -2
                    #print(temperature, humidity, rainfall, dev_sta_1)
        except:
            print('Lỗi truyền dữ liệu')
            pass
        time.sleep(0.5) # ngắt giữa các lần lặp


def save_data(): # hàm lưu dữ liệu
    global temperature, humidity, rainfall
    while (True):
        if (temperature != -2 and humidity != -2 and rainfall != -2): # nếu dữ liệu hợp lệ thì ghi vào file
            with open(cur_date, 'a', newline='') as csvfile:
                spamwriter = csv.writer(
                    csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow(
                    [str(cur_time)]+[str(temperature)]+[str(humidity)]+[str(rainfall)])
            with open("raw_tem.csv", 'a', newline='') as csvfile:
                spamwriter = csv.writer(
                    csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([str(cur_time)]+[str(temperature)])
            with open("raw_hum.csv", 'a', newline='') as csvfile:
                spamwriter = csv.writer(
                    csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([str(cur_time)]+[str(humidity)])
            with open("raw_rain.csv", 'a', newline='') as csvfile:
                spamwriter = csv.writer(
                    csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL)
                spamwriter.writerow([str(cur_time)]+[str(rainfall)])
        time.sleep(10)


def sen_data(): # hàm gửi dữ liệu
    global dev_sta_1, humidity, temperature, rainfall, data1_pre
    while (True):
        f = open("device1.txt", "r") # kiểm tra trạng thái thiết bị từ file device1.txt
        data = f.read()
        f.close()
        #print(temperature, humidity, rainfall, dev_sta_1)
        f2 = open("cur_data.txt", "w")
        f2.write(str(temperature)+',' +
                str(humidity)+','+str(rainfall)+','+str(dev_sta_1))
        f2.close()
        if (data!=data1_pre): #truyền dữ liệu bật/tắt thiết bị đến arduino
            if (dev_sta_1 == 0):
                for n in range(1, 3):
                    ser.write(b"1$")
            elif (dev_sta_1 == 1):
                for n in range(1, 3):
                    ser.write(b"0$")
            data1_pre=data
        time.sleep(0.6)

# Luồng đọc dữ liệu
t1 = threading.Thread(target=rec_data) # tạo luồng
t1.daemon = False #thiết lập lặp
t1.start() # bắt đầu luồng
# Luồng ghi dữ liệu
t2 = threading.Thread(target=save_data)
t2.daemon = False
t2.start()
# Luồng gửi dữ liệu
t3 = threading.Thread(target=sen_data)
t3.daemon = False
t3.start()

while True: # giao diện console
    print(format("#############", '^60'))
    print("1. Xem dữ liệu hiện tại")
    print("2. Điều khiển thiết bị")
    print("3. Mở web")
    print("4. Mở giao diện")
    print("5. Mở lịch sử dữ liệu")
    print("6. Thoát")
    var_1 = str(input("Nhập lựa chọn: "))
    if var_1 == "1":
        print(format("Temperature", '^30'),
              format("Humidity", '^30'),
              format("Rain flow", '^30'))
        print(format(temperature, '^30'),
              format(humidity, '^30'),
              format(rainfall, '^30'))
    elif var_1 == "2":
        print("1. Bật")
        print("2. Tắt")
        var_2 = str(input("Nhập lựa chọn: "))
        if var_2 == "1":
            for n in range (1,3):
                ser.write(b"1$")
            print("Đã bật thiết bị")
        elif var_2 == "2":
            for n in range (1,3):
                ser.write(b"0$")
            print("Đã tắt thiết bị")
    elif var_1 == "3":
        to_web()
    elif var_1 == "4":
        try:
            os.system('python gui.py')
        except:
            print("Lỗi khi mở giao diện")
    elif var_1 == "5":
        print("1. Xem danh sách file")
        print("2. Mở file")
        select = str(input("Nhập lựa chọn: "))
        dir_list = os.listdir('data')
        if select == "1":
            for n in range(0, len(dir_list)):
                print(str(n+1)+'.', dir_list[n])
        elif select == "2":
            name_file = str(input("Nhập tên file: "))
            link = str('geany data/')+name_file
            try:
                f2 = open("data/"+name_file, "r")
                f2.close()
                os.system(link)
            except:
                print("Không có file tương ứng")
        else:
            print("Không có lựa chọn tương ứng")
    elif var_1 == "6":
        break
    else:
        print("Không có lựa chọn tương ứng")
