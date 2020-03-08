import tkinter as tk
import serial_port as po

class app_comSetting:

    COM_ON = True    #串口为打开状态
    COM_OFF= False    #串口为关闭状态

    def __init__(self,root):
        self.root = root
        self.comSwitch = self.COM_OFF    #默认串口为关闭状态
        
        
        #创建 下拉COM列表
        self.creat_optionMenu()
        #创建 “端口号”lable
        self.creat_comLable()
        self.creat_bootRateLable()
        self.creat_bootRateEntry()
        self.creat_on_offButton()
        #创建 测试按钮，打印当前选择的端口
        self.creat_testButton()
        #创建 测试按钮，更新端口列表
        #self.creat_testButton2()

    #创建 “端口号”lable
    def creat_comLable(self):
        self.comLable = tk.Label(self.root,text="端口号：")
        self.comLable.grid(row=0,column=0,padx=2,pady=10,sticky=tk.W+tk.E)
        

    #创建 "端口号"下拉列表
    def creat_optionMenu(self):
        self.update_used_com()  #获取当前有效端口
        self.celect_com = tk.StringVar()
        self.celect_com.set(self.comList[0])

        self.optionMenu = tk.OptionMenu(self.root, self.celect_com, *self.comList)
        self.optionMenu.grid(row=0,column=1,padx=2,pady=10,sticky=tk.W+tk.E) 
        self.optionMenu.bind('<Button-1>', self.optionMenuCallBack )

    #创建 “波特率”lable
    def creat_bootRateLable(self):
        self.bootRateLable = tk.Label(self.root,text="波特率：")
        self.bootRateLable.grid(row=1,column=0,padx=2,pady=10,sticky=tk.W+tk.E)

    #创建 波特率Entry输入框
    def creat_bootRateEntry(self):
        self.set_bootRate = tk.StringVar()
        self.set_bootRate.set("115200")

        self.bootRateEntry = tk.Entry(self.root,textvariable=self.set_bootRate,width=10)
        self.bootRateEntry.grid(row=1,column=1,padx=2,pady=10,sticky=tk.W+tk.E)
    
    #创建 开关串口按钮
    def creat_on_offButton(self):
        if self.comSwitch == self.COM_OFF:
            self.button = tk.Button(self.root,text="打开串口",command=self.comSwitchCallback)
            self.button.grid(row=2,column=0,columnspan=2,padx=2,pady=10,sticky=tk.W+tk.E) 
        else:
            self.button = tk.Button(self.root,text="关闭串口",command=self.comSwitchCallback,background="red")
            self.button.grid(row=2,column=0,columnspan=2,padx=2,pady=10,sticky=tk.W+tk.E) 

    #创建 测试按钮，打印当前选择的端口
    def creat_testButton(self):
        self.button = tk.Button(self.root,text="test",command=self.test)
        self.button.grid(row=3,column=0,columnspan=2,padx=2,pady=10,sticky=tk.W+tk.E) 

    #创建 测试按钮，更新端口列表
    def creat_testButton2(self):
        self.add_button = tk.Button(self.root,text="添加一个COM",command=self.creat_optionMenu)
        self.add_button.grid(row=3,column=0,columnspan=2,padx=2,pady=10,sticky=tk.W+tk.E)

    def comSwitchCallback(self):
        self.comSwitch = not self.comSwitch
        self.creat_on_offButton()

        self.update_settings_to_serial()

        
    def update_settings_to_serial(self):
        if self.comSwitch == self.COM_ON:    #需要打开串口
            self.Port = po.Port(self.celect_com.get(),self.set_bootRate.get(),1)
            if self.Port.Ret == False:  #打开串口失败
                self.failToOpenPort()
        else:   #需要关闭串口
            self.Port.Close_port()

    def update_used_com(self):
        #此处po.Port.Return_used_com()如果不加.copy()会报错：“AttributeError: 'str' object has no attribute 'device'”
        self.used_com_copy_list = po.Port.Return_used_com().copy()
        if len(self.used_com_copy_list)==0:
            self.comList=["None"]
            return

        self.comList = self.used_com_copy_list
        for i in range(len(self.comList)):
            self.comList[i] = str(self.comList[i]).split("(",-1)[-1][:-1]

    def optionMenuCallBack(self,event):
        # print(1)
        if self.used_com_copy_list.copy() != po.Port.Return_used_com():
            self.creat_optionMenu()
        else:
            return

    def failToOpenPort(self):
        pass

    def test(self):
        if self.comSwitch == self.COM_ON:
            print(self.Port.Read_line())
        print(self.celect_com.get())
        print(self.set_bootRate.get())




class app_parameter_tuning:
    DefaultPara = 2000.0
    ScaleRange = 0.1
    ScaleSize  = 100
    MouseWheelStep = 0.001

    def __init__(self,root,para_name):
        self.root = root
        self.para_name = para_name
        self.setParameter = self.DefaultPara

        self.EntrySetParameter = tk.DoubleVar()
        self.EntrySetParameter.set(self.DefaultPara)
        self.ScaleSetParameter = tk.DoubleVar()
        self.ScaleSetParameter.set(self.DefaultPara)
        self.CheckButtonFlag = tk.BooleanVar()
        self.CheckButtonFlag.set(False)

        self.creat_Lable()
        self.creat_Entry()
        self.creat_Scale()
        self.creat_CheckButton()
        self.creat_confirmButton()



    #创建 “参数”lable
    def creat_Lable(self):
        self.LableUnit = tk.Label(self.root,text=self.para_name,width=5)
        self.LableUnit.grid(row=0,column=0,padx=2,pady=0,sticky=tk.W)

    #创建 参数Entry输入框
    def creat_Entry(self):
        self.EntryUnit = tk.Entry(self.root,textvariable=self.EntrySetParameter,width=10)
        self.EntryUnit.grid(row=0,column=1,padx=2,pady=0,sticky=tk.W)
        self.EntryUnit.bind('<KeyRelease-Return>',self.EntryKeyCallback)
        self.EntryUnit.bind('<FocusOut>',self.EntryKeyCallback)
                    
    def creat_Scale(self):
        para = self.ScaleSetParameter.get()
        range_ = self.ScaleRange*para
        self.scaleUnit = tk.Scale(self.root, from_=para-range_, to=para+range_,resolution=self.MouseWheelStep*range_,\
            length=self.ScaleSize, variable=self.ScaleSetParameter, orient=tk.HORIZONTAL, digits=7 ,command=self.ScaleChangeCallback,\
                sliderrelief = tk.FLAT ,sliderlength=10,width=10)
        self.scaleUnit.grid(row=1,column=0,columnspan=2,padx=2,pady=0,sticky=tk.W+tk.E)
        self.scaleUnit.bind('<MouseWheel>',self.ScaleWheelCallback)
        #self.scaleUnit.bind('<Button-1>',self.ScaleEnterCallback)
        #self.paraTunScale.bind()

    def creat_CheckButton(self):
        self.checkUnit = tk.Checkbutton(self.root, text=" ", variable=self.CheckButtonFlag, onvalue=True, offvalue=False,command=self.CheckButtonCallback)
        self.checkUnit.grid(row=1,column=2,columnspan=2,padx=2,pady=5)

    def creat_confirmButton(self):
        self.confirmButton = tk.Button(self.root,text="确认",command=self.ConfirmButtomCallback)
        self.confirmButton.grid(row=0,column=2,columnspan=2,padx=2,pady=10) 

    def ConfirmButtomCallback(self):
        self.confirmButton.focus_set()
        self.setParameter = self.EntrySetParameter.get()
        print(self.setParameter)
    
    def CheckButtonCallback(self):
        self.checkUnit.focus_set()

    def updateSetPara(self):
        if self.CheckButtonFlag.get() == True:
            self.setParameter = self.EntrySetParameter.get()
            print(self.setParameter)
        
    def ScaleWheelCallback(self,event):
        if event.delta > 0:# 滚轮往上滚动，放大
            self.scaleUnit.set(self.ScaleSetParameter.get()*(1+self.MouseWheelStep))
        else:   # 滚轮往下滚动，缩小
            self.scaleUnit.set(self.ScaleSetParameter.get()*(1-self.MouseWheelStep))

    def ScaleChangeCallback(self,text):
        self.EntrySetParameter.set(self.ScaleSetParameter.get())

        self.updateSetPara()


    # def ScaleEnterCallback(self,event):
    #     self.scaleUnit.focus_set()

    def EntryKeyCallback(self,event):
        self.scaleUnit.destroy()
        self.ScaleSetParameter.set(self.EntrySetParameter.get()) 
        #print( self.ScaleSetParameter.get())
        self.creat_Scale()

        self.updateSetPara()
        

if __name__ == '__main__':
    root=tk.Tk()
    frame0 = tk.Frame(root,bd=1, relief=tk.SUNKEN)
    frame1 = tk.Frame(root,bd=1, relief=tk.SUNKEN)
    frame2 = tk.Frame(root,bd=1, relief=tk.SUNKEN)
    frame3 = tk.Frame(root,bd=1, relief=tk.SUNKEN)
    frame4 = tk.Frame(root,bd=1, relief=tk.SUNKEN)
    frame5 = tk.Frame(root,bd=1, relief=tk.SUNKEN)
    frame6 = tk.Frame(root,bd=1, relief=tk.SUNKEN)
    frame7 = tk.Frame(root,bd=1, relief=tk.RAISED)
    frame8 = tk.Frame(root,bd=1, relief=tk.RAISED)
    
    
    frame1.grid(row=0,column=0,padx=2,pady=5)
    frame2.grid(row=1,column=0,padx=2,pady=5)
    frame3.grid(row=2,column=0,padx=2,pady=5)
    frame7.grid(row=0,column=1,padx=2,pady=5,rowspan=3,sticky=tk.N+tk.S)
    frame4.grid(row=0,column=2,padx=2,pady=5)
    frame5.grid(row=1,column=2,padx=2,pady=5)
    frame6.grid(row=2,column=2,padx=2,pady=5)
    frame8.grid(row=0,column=3,padx=2,pady=5,rowspan=3,sticky=tk.N+tk.S)
    frame0.grid(row=0,column=4,padx=2,pady=5,rowspan=3,sticky=tk.N)
    
    # a = tk.Label(frame7,text="")
    # a.grid(sticky=tk.N+tk.S)
    # b = tk.Label(frame8,text="")
    # b.grid(sticky=tk.N+tk.S)
    test0 = app_comSetting(frame0)
    test1 = app_parameter_tuning(frame1,"参数1")
    test2 = app_parameter_tuning(frame2,"参数2")
    test3 = app_parameter_tuning(frame3,"参数3")
    test4 = app_parameter_tuning(frame4,"参数4")
    test5 = app_parameter_tuning(frame5,"参数5")
    test6 = app_parameter_tuning(frame6,"参数6")

    root.mainloop()