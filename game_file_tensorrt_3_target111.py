from Game_Test_3 import Ui_game_MainWindow
import sys
from PyQt5.QtWidgets import QApplication,QMainWindow,QFileDialog
from PyQt5.QtCore import QTimer,QCoreApplication
from PyQt5.QtGui import QPixmap
import cv2
import qimage2ndarray
import time
import socket

from test_tensorrt import YoLov5TRT
from test_tensorrt import detect
from test_tensorrt import categories
import time
import pycuda.autoinit  # This is needed for initializing CUDA driver
import numpy as np
import pyrealsense2 as rs
import ctypes
import pycuda.driver as cuda
from collections import Counter

import threading
import random
PLUGIN_LIBRARY = "/home/nano/tensorrtx/yolov5/build/libmyplugins.so"
engine_file_path = "/home/nano/tensorrtx/yolov5/build/best_M_last.engine"


#yolov5=Yolov5Manager_class()
tensorrt=detect()
pipeline=rs.pipeline()
config=rs.config()
config.enable_stream(rs.stream.color,640,480,rs.format.bgr8,30)
config.enable_stream(rs.stream.depth,640,480, rs.format.z16,30)


ctypes.CDLL(PLUGIN_LIBRARY)
yolov5_wrapper = YoLov5TRT(engine_file_path)
client=socket.socket(socket.AF_INET,socket.SOCK_STREAM)
client.connect(('192.168.1.66',6666))
#start_msg_head='\x00\x00\x00\x00\x00\x00\x00\x07'
start_msg_end='WHUT001'
#start_msg=start_msg_head+start_msg_end
ID_name='目标ID：'
ID_num='数量：'

class CamShow(QMainWindow,Ui_game_MainWindow):
    def __init__(self,parent=None):
        super(CamShow,self).__init__(parent)
        self.setupUi(self)
        self.read_img()
        self.PrepWidgets()
        self.PrepParameters()
        self.CallBackFunctions()
        self.Timer = QTimer()
        self.Timer.timeout.connect(self.TimerOutFun)
        self.Timer2 = QTimer()
        self.Timer2.timeout.connect(self.Timer2OutFun)

        self.Msg_state.clear()
        self.Msg_state.setPlainText('             待启动')

        self.Timer.start(1)

    def DispImg2(self):
    	img1_2 =cv2.cvtColor(self.picture, cv2.COLOR_BGR2RGB)
    	qimg1_2=qimage2ndarray.array2qimage(img1_2)
    	self.picture_label.setPixmap(QPixmap(qimg1_2))
    	self.picture_label.hide()
    def DispImg3(self):
    	img1_2 =cv2.cvtColor(self.picture, cv2.COLOR_BGR2RGB)
    	qimg1_2=qimage2ndarray.array2qimage(img1_2)
    	self.picture_label.setPixmap(QPixmap(qimg1_2))
    	self.picture_label.show()

    def read_img(self):
    	self.picture=cv2.imread('/home/nano/tensorrtx/yolov5/build/picture.png',1)
    	self.DispImg2()

    def from_code_to_tcp(self,weather_start_or_end,msg_data):
        if weather_start_or_end==0:#代表是开始，要发0
            tcp_head='00 00 00 00 00 00 00 '
            num=str(len(msg_data))
            if len(msg_data)>=16:
                gg=hex(len(msg_data)).lstrip('0x')
            else:
                gg='0'+num
            tcp_head=tcp_head+gg
            start_msg_end_hex=''
            for i in range(len(msg_data)):
                start_msg_end_hex=start_msg_end_hex+hex(ord(msg_data[i]))[2:]+''
            start_msg=bytes.fromhex(tcp_head)
            start_msg=start_msg+bytes.fromhex(start_msg_end_hex)
            #print(start_msg)
            client.send(start_msg)
        elif weather_start_or_end==1:#代表要结束，发1
            tcp_head='00 00 00 01 00 00 00 '
            end_str='END'
            num=str(len(msg_data)+3)
            if len(msg_data)+3>=16:
                gg=hex(len(msg_data)+3).lstrip('0x')
            else:
                gg='0'+num
            tcp_head=tcp_head+gg
            end_msg=bytes.fromhex(tcp_head)
            end_msg_end_hex=''
            str_split=msg_data.split('#')
            for i in range(msg_data.count('#')):
            	for j in range(len(str_split[i])):
            		end_msg_end_hex=end_msg_end_hex+hex(ord((str_split[i])[j]))[2:]+''
            	end_msg_end_hex=end_msg_end_hex+' 0D'
            for i in range(len(end_str)):
                end_msg_end_hex=end_msg_end_hex+hex(ord(end_str[i]))[2:]+''
            end_msg=end_msg+bytes.fromhex(end_msg_end_hex)
            client.send(end_msg)

        elif weather_start_or_end==3:#要发3
            tcp_head='00 00 00 03 00 00 00 '
            start_msg=start_msg+bytes.fromhex(start_msg_end_hex)
            client.send(start_msg)


    def PrepWidgets(self):
        self.PrepCamera()

    def PrepParameters(self):
        self.R=1
        self.G=1
        self.B=1
        self.weather_decide=0
        self.weather_0=0
        self.count_num=0
        self.remeber_list=[]
        self.remeber_clss=[]
        self.remeber_list_num=0
        self.which_epoch=0 #判断这是第几次识别
        self.sleep=0

    def PrepCamera(self):
        try:
            profile = pipeline.start(config)
            sensor_dep=profile.get_device().first_depth_sensor()
            exp=sensor_dep.get_option(rs.option.visual_preset)
            print("---------------------------------------------------")
            print("before_visual_preset="+str(exp))
            exp=sensor_dep.set_option(rs.option.visual_preset,1)
            exp=sensor_dep.get_option(rs.option.visual_preset)
            print("after_visual_preset="+str(exp))
            print("---------------------------------------------------")
			# 获取深度传感器的深度标尺（参见rs - align示例进行说明）
            depth_sensor = profile.get_device().first_depth_sensor()
            depth_scale = depth_sensor.get_depth_scale()
            print("Depth Scale is: ", depth_scale)
            align_to = rs.stream.color
            self.align = rs.align(align_to)
       #     self.Msg_message.clear()
        #    self.Msg_state.clear()
        except Exception as e:
        	print("ERROR")
        	self.Msg_message.clear()
        	self.Msg_state.clear()

    def CallBackFunctions(self):
        self.Start_Button.clicked.connect(self.start_button_code)

    def pyqt_append(self,msg_list):
    	set_msg_list=set(msg_list)
    	if len(set_msg_list)==len(msg_list):
    		for i in range(len(msg_list)):
    			self.Msg_message.append(ID_name+categories[int(msg_list[i])]+'       '+ID_num+'1')
    		self.Timer.stop()
    	else:
    		dict_list=dict(Counter(msg_list))
    		for i in range(len(set_msg_list)):
    			self.Msg_message.append(ID_name+categories[int(list(set_msg_list)[i])]+'       '+ID_num+str(dict_list[list(set_msg_list)[i]]))
    		self.Timer.stop()


    def msg_append(self,msg_list):#向界面输出区发送信息及向裁判软件发送信息
        set_msg_list=set(msg_list)
        result_file=open("/home/nano/Desktop/result/result4.txt","w")
        result_file.write("START\n")
        if len(set_msg_list)==len(msg_list):#如果没有重复的物体
            self.tcp_msg='START#'
            for i in range(len(msg_list)):
                #self.Msg_message.append(ID_name+categories[int(msg_list[i])]+'       '+ID_num+'1')
                self.tcp_msg=self.tcp_msg+'Goal_ID='+categories[int(msg_list[i])]+';Num='+'1#'
                file_str="Goal_ID="+categories[int(msg_list[i])]+";Num=1\n"
                result_file.write(file_str)
            #self.tcp_msg=self.tcp_msg+'END'
            result_file.write("END")
            result_file.close()
            self.from_code_to_tcp(1,self.tcp_msg)
            self.Msg_state.clear()
            self.Msg_state.setPlainText('               结束')
            print(self.tcp_msg)
            self.Timer.stop()

        else:#如果有重复的物体
            dict_list=dict(Counter(msg_list))
            self.tcp_msg='START#'
            for i in range(len(set_msg_list)):
                #self.Msg_message.append(ID_name+categories[int(list(set_msg_list)[i])]+'       '+ID_num+str(dict_list[list(set_msg_list)[i]]))
                self.tcp_msg=self.tcp_msg+'Goal_ID='+categories[int(list(set_msg_list)[i])]+';Num='+str(dict_list[list(set_msg_list)[i]])+'#'
                file_str="Goal_ID="+categories[int(list(set_msg_list)[i])]+";Num="+str(dict_list[list(set_msg_list)[i]])+"\n"
                result_file.write(file_str)
            #self.tcp_msg=self.tcp_msg+'END'
            result_file.write("END")
            result_file.close()
            self.from_code_to_tcp(1,self.tcp_msg)
            self.Msg_state.clear()
            self.Msg_state.setPlainText('               结束')
            print(self.tcp_msg)
            self.Timer.stop()


    def start_button_code(self):
        #self.picture_label.hide()
        self.Timer.stop()
        self.timelb=time.perf_counter()
        self.Msg_state.clear()
        self.Msg_state.setPlainText('             运行中')
        self.from_code_to_tcp(0,start_msg_end)
        self.weather_decide=1
        self.Timer2.start(1)
        self.Msg_state.setPlainText('             识别中')

    def TimerOutFun(self):
        self.img_before=pipeline.wait_for_frames()
        self.img=(self.img_before).get_color_frame()
        self.img = np.asanyarray((self.img).get_data())
        self.Image = self.img
        self.DispImg()

    def Timer2OutFun(self):
        self.img_before=pipeline.wait_for_frames()
        self.aligned_frames=self.align.process(self.img_before)
        self.img=(self.aligned_frames).get_color_frame()
        self.depth_img=(self.aligned_frames).get_depth_frame()
        self.depth_intrin=(self.depth_img).profile.as_video_stream_profile().intrinsics

        self.img = np.asanyarray((self.img).get_data())
        if self.sleep==1:
        	time.sleep(6)
        	#self.picture_label.hide()
        	#self.DispImg2()
        	self.sleep=0
        	self.Msg_state.clear()
        	self.Msg_state.setPlainText('             识别中')
        	self.picture_label.hide()
        if self.weather_decide==0:
            self.Image = self.img
        elif self.weather_decide==1:
            self.Image ,self.clss= tensorrt.detect_one(self.img,yolov5_wrapper,self.depth_img,self.depth_intrin)
            if self.weather_0==0:
                self.remeber_list=(self.clss).sort()
                self.remeber_list_num=len(self.clss)
                self.weather_0=1
            elif self.weather_0!=0:
                if ((self.clss).sort()==self.remeber_list) and (len(self.clss)!=0) and (self.remeber_list_num==len(self.clss)):
                    print('相同')
                    self.count_num=self.count_num+1
                    if self.count_num==2:
                    	print("应该暂停")
                    	if self.which_epoch!=2:
                    		self.Msg_state.clear()
                    		self.Msg_state.setPlainText('            待旋转')
                    		self.from_code_to_tcp(3,0000)
                    		self.picture_label.show()
                    		(self.remeber_clss).extend(self.clss)
                    		self.Msg_message.clear()
                    		self.pyqt_append(self.remeber_clss)
                    		#time.sleep(5)
                    		self.sleep=1
                    		self.which_epoch=self.which_epoch+1
                    		self.count_num=0
                    		self.weather_0=0
                    		self.remeber_list=[]
                    		self.remeber_list_num=0
                    		#self.Msg_state.clear()
                    		#self.Msg_state.setPlainText('             识别中')
                    	else:#到了最后一次
                    		self.from_code_to_tcp(3,0000)
                    		(self.remeber_clss).extend(self.clss)
                    		self.msg_append(self.remeber_clss)
                    		self.Msg_message.clear()
                    		self.pyqt_append(self.remeber_clss)
                    		self.Timer.stop()
                    		self.Timer2.stop()
                elif ((self.clss).sort()!=self.remeber_list) or (len(self.clss)==0) or (self.remeber_list_num!=len(self.clss)):
                    self.remeber_list=(self.clss).sort()
                    self.remeber_list_num=len(self.clss)
                    self.count_num=0
        self.DispImg()

    def DispImg(self):
        img1 =cv2.cvtColor(self.Image, cv2.COLOR_BGR2RGB)
        qimg1=qimage2ndarray.array2qimage(img1)
        self.common_video_label.setPixmap(QPixmap(qimg1))
        self.common_video_label.show()
    # def DispImg2(self):
    #     img1_2 =cv2.cvtColor(self.picture, cv2.COLOR_BGR2RGB)
    #     qimg1_2=qimage2ndarray.array2qimage(img1_2)
    #     self.picture_label.setPixmap(QPixmap(qimg1_2))
        #self.picture_label.show()
'''
    def ColorAdjust(self,img):
        try:
            B = img[:, :, 0]
            G = img[:, :, 1]
            R = img[:, :, 2]
            B = B * self.B
            G = G * self.G
            R = R * self.R
            img1 = img
            img1[:, :, 0] = B
            img1[:, :, 1] = G
            img1[:, :, 2] = R
            return img1
        except Exception as e:
            self.Msg_state.clear()
            self.Msg_message.clear()
'''

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ui=CamShow()
    ui.show()
    sys.exit(app.exec_())
