import serial
import serial.tools.list_ports

class Port():

    #初始化
    def __init__(self,com,bps,timeout):
        self.port = com
        self.bps = bps
        self.timeout = timeout
        self.main_engine = None
        self.Ret = False
        try:
            # 打开串口，并得到串口对象
            self.main_engine = serial.Serial(self.port,self.bps,timeout=self.timeout)
            # 判断是否打开成功
            if (self.main_engine.is_open):
                self.Ret = True
            else:
                self.Ret = False
        except Exception as e:
            self.Ret = False
            print("---异常---：", e)

    # 打印设备基本信息
    def Print_name(self):
        print(self.main_engine.name) #设备名字
        print(self.main_engine.port)#读或者写端口
        print(self.main_engine.baudrate)#波特率
        print(self.main_engine.bytesize)#字节大小
        print(self.main_engine.parity)#校验位
        print(self.main_engine.stopbits)#停止位
        print(self.main_engine.timeout)#读超时设置
        print(self.main_engine.writeTimeout)#写超时
        print(self.main_engine.xonxoff)#软件流控
        print(self.main_engine.rtscts)#软件流控
        print(self.main_engine.dsrdtr)#硬件流控
        print(self.main_engine.interCharTimeout)#字符间隔超时

    #打开串口
    def Open_port(self):
        self.main_engine.open()
        #print("Serial is open?",self.main_engine.is_open)  # 检验串口是否打开

    #关闭串口
    def Close_port(self):
        self.main_engine.close()
        #print("Serial is open?",self.main_engine.is_open)  # 检验串口是否打开

    
    @staticmethod #声明下面Print_Used_Com方法不强制要求传递参数，（如不需要表示自身对象的self和自身类的cls参数，就跟使用函数一样。）
    def Return_used_com():
        return list(serial.tools.list_ports.comports())
        
    # 打印可用串口列表
    def Print_used_com(self):
        self.com_list = list(serial.tools.list_ports.comports())
        print(self.com_list)
    
    def Update_used_com(self):
        self.com_list = list(serial.tools.list_ports.comports())

    #接收指定大小的数据
    #从串口读size个字节。如果指定超时，则可能在超时后返回较少的字节；如果没有指定超时，则会一直等到收完指定的字节数。
    def Read_size(self,size):
        return self.main_engine.read(size=size)

    #接收一行数据
    # 使用readline()时应该注意：打开串口时应该指定超时，否则如果串口没有收到新行，则会一直等待。
    # 如果没有超时，readline会报异常。
    def Read_line(self):
        return self.main_engine.readline()

    #发数据
    def Send_data(self,data):
        self.main_engine.write(data)

    #清除输入缓冲区数据
    def Clear_rxbuff(self):
        self.main_engine.flushInput() 
    #中止当前输出并清除输出缓冲区数据
    def Clear_txbuff(self):
        self.main_engine.flushOutput() 

    #更多示例
    # self.main_engine.write(chr(0x06).encode("utf-8"))  # 十六制发送一个数据
    # print(self.main_engine.read().hex())  #  # 十六进制的读取读一个字节
    # print(self.main_engine.read())#读一个字节
    # print(self.main_engine.read(10).decode("gbk"))#读十个字节
    # print(self.main_engine.readline().decode("gbk"))#读一行
    # print(self.main_engine.readlines())#读取多行，返回列表，必须匹配超时（timeout)使用
    # print(self.main_engine.in_waiting)#获取输入缓冲区的剩余字节数
    # print(self.main_engine.out_waiting)#获取输出缓冲区的字节数
    # print(self.main_engine.readall())#读取全部字符。

    #接收数据
    #一个整型数据占两个字节
    #一个字符占一个字节

    # def Recive_data(self,way):
    #     # 循环接收数据，此为死循环，可用线程实现
    #     print("开始接收数据：")
    #     while True:
    #         try:
    #             # 一个字节一个字节的接收
    #             if self.main_engine.in_waiting:
    #                 if(way == 0):
    #                     for i in range(self.main_engine.in_waiting):
    #                         print("接收ascii数据："+str(self.Read_Size(1)))
    #                         data1 = self.Read_Size(1).hex()#转为十六进制
    #                         data2 = int(data1,16)#转为十进制
    #                         if (data2 == "exit"):  # 退出标志
    #                             break
    #                         else:
    #                              print("收到数据十六进制："+data1+"  收到数据十进制："+str(data2))
    #                 if(way == 1):
    #                     #整体接收
    #                     # data = self.main_engine.read(self.main_engine.in_waiting).decode("utf-8")#方式一
    #                     data = self.main_engine.read_all()#方式二
    #                     if (data == "exit"):  # 退出标志
    #                         break
    #                     else:
    #                          print("接收ascii数据：", data)
    #         except Exception as e:
    #             print("异常报错：",e)


# Port.Print_Used_Com()
# Ret =False #是否创建成功标志

# Engine1 = Port("com12",115200,0.5)
# if (Ret):
#     Engine1.Recive_data(0)