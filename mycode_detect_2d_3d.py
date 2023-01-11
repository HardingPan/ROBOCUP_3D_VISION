import numpy as np
import math
import pyrealsense2 as rs
class detect_2d_3d():
	def __init__(self):
		print("Init mycode to detect 2d or 3d object")
		self.PrepParameters()
	
	def PrepParameters(self):
		self.x_slope_yuzhi=0.0055   #设置左阈值为10mm，即为1cm
		self.up_slope_yuzhi=0.015
		self.visible_yuzhi=1.60

	def weather_find_points_x_both(self,depth_img,x_left,x_right,y_middle,length_x):
		j=0
		index_in=0
		index_out_left=0
		index_out_right=0
		while j<length_x:
			real_leng=depth_img.get_distance((x_left+j),y_middle)
			if real_leng==0: #如果此点测量到的距离为0，表明可能超出测量范围，这是不可抗力
				index_in=index_in+1
			j=j+1
#------------------------
		j=0
		if (x_left-int(length_x/4))>0:
			lang_left=int(length_x/4)
		elif (x_left-int(length_x/4))<=0:
			lang_left=x_left-1
		while j<lang_left:
			real_leng=depth_img.get_distance((x_left-j),y_middle)
			if real_leng==0:
				index_out_left=index_out_left+1
			j=j+1
#-------------------------
		j=0
		if (x_right+int(length_x/4))>=640:
			lang_right=640-x_right-1
		elif (x_right+int(length_x/4))<640:
			lang_right=int(length_x/4)
		while j<lang_right:
			real_leng=depth_img.get_distance((x_right+j),y_middle)
			if real_leng==0:
				index_out_right=index_out_right+1
			j=j+1
#-------------------------
		if index_in>=(length_x/2):
			return 0 #返回0代表将此物体看作是3D实物
		elif index_in<(length_x/2) and index_out_left<(lang_left/2) and index_out_right<(lang_right/2):
			return 1 #返回1代表两边都需要进一步判断
		elif index_in<(length_x/2) and index_out_left>=(lang_left/2) and index_out_right<(lang_right/2):
			return 2 #返回2代表左边不需要进一步判断了，右边需要判断
		elif index_in<(length_x/2) and index_out_left<(lang_left/2) and index_out_right>=(lang_right/2):
			return 3 #返回3代表右边不需要进一步判断了，左边需要判断
		elif index_in<(length_x/2) and index_out_left>=(lang_left/2) and index_out_right>=(lang_right/2):
			return 4 #两边都无法判断，进行上面判断

	def weather_find_points_y(self,depth_img,y_first,x_middle,length_y):
		j=0
		index_in=0
		index_out=0
		while j<length_y:
			real_leng=depth_img.get_distance(x_middle,(y_first+j))
			if real_leng==0:
				index_in=index_in+1
			j=j+1
		j=0
		if (y_first-int(length_y/4))>0:
			lang=int(length_y/4)
		elif (y_first-int(length_y/4))<=0:
			lang=y_first-1
		while j<lang:
			real_leng=depth_img.get_distance(x_middle,(y_first-j))
			if real_leng==0:
				index_out=index_out+1
			j=j+1
		if index_in>=(length_y/2):
			return 0 #代表将测物体视为3D
		elif index_in<(length_y/2) and index_out>(lang/2):
			return 0 #代表将此物体视为3D
		elif index_in<(length_y/2) and index_out<=(lang/2):
			return 1 #代表进一步判断

	def use_math_to_detect_y(self,depth_img,y_first,x_middle,length_y):
		i=0
		if (y_first-int(length_y/4))>0:
			lang=int(length_y/4)
		else:
			lang=y_first-1
		now_index=y_first-lang
		next_index=y_first-lang+1
		max_slope=0
		remember_slope=0
		while i<=(lang+int(length_y/2)):
			while(True):
				now_length=depth_img.get_distance(x_middle,now_index)
				next_length=depth_img.get_distance(x_middle,next_index)
				if now_length!=0 and next_length!=0:
					break
				if now_length==0 and next_length!=0:
					now_index=next_index
					next_index=next_index+1
					i=i+1
				elif now_length!=0 and next_length==0:
					next_index=next_index+1
					i=i+1
				elif now_length==0 and next_length==0:
					next_index=next_index+1
					now_index=next_index
					next_index=next_index+1
					i=i+2
			slope=next_length-now_length
			if abs(slope)>max_slope:
				max_slope=abs(slope)
				remember_slope=slope
			i=i+1
			now_index=now_index+1
			next_index=next_index+1
		if max_slope>=self.up_slope_yuzhi:
			return 0
		else:
			return 1

	def use_math_to_detect_x_left(self,depth_img,x,y_middle,length_x):
		i=0
		if (x-int(length_x/4))>0:
			lang=int(length_x/4)
		elif (x-int(length_x/4))<=0:
			lang=x-1
		now_index=x-lang
		next_index=x-lang+1
		max_slope=0
		remember_slope=0
		while i<=(lang+int(length_x/2)):
			while(True):
				now_length=depth_img.get_distance(now_index,y_middle)
				next_length=depth_img.get_distance(next_index,y_middle)
				if now_length!=0 and next_length!=0:
					break
				if now_length==0 and next_length!=0:
					now_index=next_index
					next_index=next_index+1
					i=i+1
				elif now_length!=0 and next_length==0:
					next_index=next_index+1
					i=i+1
				elif now_length==0 and next_length==0:
					next_index=next_index+1
					now_index=next_index
					next_index=next_index+1
					i=i+2
			#print("now_length=%f next_length=%f",now_length,next_length)
			slope=next_length-now_length
			if abs(slope)>max_slope:
				max_slope=abs(slope) #记录绝对值做对比
				remember_slope=slope #记录实际值判断正负号
			i=i+1
			now_index=next_index
			next_index=next_index+1
		if max_slope>=self.x_slope_yuzhi and remember_slope<0:
			return 0 #代表此处检测坡度大于阈值，同时符号为负
		elif max_slope>=self.x_slope_yuzhi and remember_slope>=0:
			return 1 #代表此处检测坡度大于阈值，但符号为正，前面有东西挡住了
		elif max_slope<self.x_slope_yuzhi:
			return 2 #代表此处检测坡度小于阈值

	def use_math_to_detect_x_right(self,depth_img,x,y_middle,length_x):
		i=0
		if (x+int(length_x/4))>=640:
			lang=640-x-1
		elif (x-int(length_x/4))<640:
			lang=int(length_x/4)
		now_index=x+lang
		next_index=x+lang-1
		max_slope=0
		remember_slope=0
		while i<=(lang+int(length_x/2)):
			while(True):
				now_length=depth_img.get_distance(now_index,y_middle)
				next_length=depth_img.get_distance(next_index,y_middle)
				if now_length!=0 and next_length!=0:
					break
				if now_length==0 and next_length!=0:
					now_index=next_index
					next_index=next_index-1
					i=i+1
				elif now_length!=0 and next_length==0:
					next_index=next_index-1
					i=i+1
				elif now_length==0 and next_length==0:
					next_index=next_index-1
					now_index=next_index
					next_index=next_index-1
					i=i+2
			#print("now_length=%f next_length=%f",now_length,next_length)
			slope=next_length-now_length
			if abs(slope)>max_slope:
				max_slope=abs(slope) #记录绝对值做对比
				remember_slope=slope #记录实际值判断正负号
			i=i+1
			now_index=next_index
			next_index=next_index-1
		if max_slope>=self.x_slope_yuzhi and remember_slope<0:
			return 0 #代表此处检测坡度大于阈值，同时符号为负
		elif max_slope>=self.x_slope_yuzhi and remember_slope>=0:
			return 1 #代表此处检测坡度大于阈值，但符号为正，前面有东西挡住了
		elif max_slope<self.x_slope_yuzhi:
			return 2 #代表此处检测坡度小于阈值

	def weather_visible(self,depth_img,x_first,y_middle,length_x):
		count_unvisible_num=0
		avg_distance=0
		count_visible_num=0
		i=0
		while(i<=length_x):
			real_distance=depth_img.get_distance((x_first+i),y_middle)
			if real_distance==0:
				count_unvisible_num=count_unvisible_num+1
			else:
				avg_distance=avg_distance+real_distance
				count_visible_num=count_visible_num+1
			i=i+1
		avg_distance_fin=avg_distance/count_visible_num
		if count_unvisible_num>=length_x*3/4 or avg_distance_fin>=self.visible_yuzhi:
			return True #代表需要将这个去掉并且跳过之后的
		else:
			return False

	def detect_2d_or_3d_code(self,depth_img,result_boxes, result_scores, result_classid,depth_intrin):
		index_del=[]
		max=0
		min=100
		print("detect_start",result_classid)
		i=0
		hight_store={}
#-------------------------------------------------------------------------------------------------------------------------------
		for i in range(len(result_boxes)):
			j=0
			box=result_boxes[i]
			middle_x=int((int(box[0])+int(box[2]))/2)  #识别物外框中心点x坐标
			middle_y=int((int(box[1])+int(box[3]))/2)  #识别物外框中心点y坐标
			while(1):
				real_distance=depth_img.get_distance((middle_x),(middle_y+j))
				if real_distance!=0:
					camera_coordinate = rs.rs2_deproject_pixel_to_point(depth_intrin,[(middle_x),(middle_y+j)],real_distance)
					hight=real_distance*math.sin(3.14159/4)+camera_coordinate[1]*math.cos(3.14159/4)
					hight_store[i]=hight
					if i==0:
						min=hight
						max=hight
					else:
						if hight>=max:
							max=hight
						if hight<=min:
							min=hight
					break
				else:
					j=j+1
		mid_yuzhi=min+0.315
		mid_distance=(min+max)/2
		if mid_distance>=mid_yuzhi:
			mid=mid_distance
		else:
			mid=mid_yuzhi
		print('hightest:'+str(max))
		print('lowest:'+str(min))
		print('mid:'+str(mid))
		i=0
#-------------------------------------------------------------------------------------------------------------------------------
		for i in range(len(result_boxes)):
			box=result_boxes[i]
			jj=0
			self.middle_x=int((int(box[0])+int(box[2]))/2)  #识别物外框中心点x坐标
			self.middle_y=int((int(box[1])+int(box[3]))/2)  #识别物外框中心点y坐标
			length_x=(int(box[2])-int(box[0])) #识别物外框x方向长度为多少个像素
			length_y=(int(box[3])-int(box[1]))
#-------------------------------------------------------------------------------------------------------------------------------
			# bool_num0=self.weather_visible(depth_img,int(box[0]),self.middle_y,length_x)
			# if bool_num0:
			# 	index_del.append(i)
			# 	continue
			# while(1):
			# 	real_distance=depth_img.get_distance((middle_x),(middle_y+jj))
			# 	if real_distance!=0:
			# 		camera_coordinate = rs.rs2_deproject_pixel_to_point(depth_intrin,[(self.middle_x),(self.middle_y+jj)],real_distance)
			# 		hight=real_distance*math.sin(3.14159/4)+camera_coordinate[1]*math.cos(3.14159/4)
			# 		break
			# 	else:
			# 		jj=jj+1
			if hight_store[i]>mid:
				print('this is too low'+str(hight_store[i]))
				index_del.append(i)
				continue
			else:
				print(str(result_classid[i])+'this is good hight'+str(hight_store[i]))
#-------------------------------------------------------------------------------------------------------------------------------
			bool_num1=self.weather_find_points_x_both(depth_img,int(box[0]),int(box[2]),self.middle_y,length_x) #如果返回的为True，则将此物体看作是3D实物，返回的是False，则进一步判断
			if bool_num1==0:
				print("in_points_too_few, it is a 3D")
				continue #将此视为3D实体
			elif bool_num1==1:  #两边都需要判断
				bool_num2=self.use_math_to_detect_x_left(depth_img,int(box[0]),self.middle_y,length_x)
				bool_num3=self.use_math_to_detect_x_right(depth_img,int(box[2]),self.middle_y,length_x)
				if bool_num2==0 and bool_num3==0:
					print("both_x_side_slope_is_enough")
					continue
				elif bool_num2==2 or bool_num3==2:
					print("x_slope_is too few")
					index_del.append(i)
					continue
				elif (bool_num2!=2 and bool_num3!=2) and (bool_num2==1 or bool_num3==1):
					print("slope is + start y detect")
					bool_num4=self.weather_find_points_y(depth_img,int(box[1]),self.middle_x,length_y)
					if bool_num4==0:
						print("y_points_detect,it is a 3D")
						continue
					else:#进行slope判断
						bool_num5=self.use_math_to_detect_y(depth_img,int(box[1]),self.middle_x,length_y)
						if bool_num5==0:
							print("y_slope_ok")
							continue
						else:
							index_del.append(i)
							print("y_slope_not_ok")
							continue
			elif bool_num1==2: #只判断右边
				bool_num3=self.use_math_to_detect_x_right(depth_img,int(box[2]),self.middle_y,length_x)
				if bool_num3==0:
					print("x_right_side_slope_is_enough")
					continue
				elif bool_num3==2:
					print("x_right_slope_is not_ok")
					index_del.append(i)
					continue
				elif bool_num3==1:
					print("x_right_slope is + start y detect")
					bool_num4=self.weather_find_points_y(depth_img,int(box[1]),self.middle_x,length_y)
					if bool_num4==0:
						print("y_points_detect it is a 3D")
						continue
					else:#进行slope判断
						bool_num5=self.use_math_to_detect_y(depth_img,int(box[1]),self.middle_x,length_y)
						if bool_num5==0:
							print("y_slope_ok")
							continue
						else:
							index_del.append(i)
							print("y_slope_not_ok")
							continue
			elif bool_num1==3: #只判断左边
				bool_num2=self.use_math_to_detect_x_left(depth_img,int(box[0]),self.middle_y,length_x)
				if bool_num2==0:
					print("x_left_side_slope_is_enough")
					continue
				elif bool_num2==2:
					print("x_left_slope_is not_ok")
					index_del.append(i)
					continue
				elif bool_num2==1:
					print("x_left_slope is + start y detect")
					bool_num4=self.weather_find_points_y(depth_img,int(box[1]),self.middle_x,length_y)
					if bool_num4==0:
						print("y_points_detect it is a 3D")
						continue
					else:#进行slope判断
						bool_num5=self.use_math_to_detect_y(depth_img,int(box[1]),self.middle_x,length_y)
						if bool_num5==0:
							print("y_slope_ok")
							continue
						else:
							index_del.append(i)
							print("y_slope_not_ok")
							continue
			elif bool_num1==4: #进行上面的检测
				bool_num4=self.weather_find_points_y(depth_img,int(box[1]),self.middle_x,length_y)
				if bool_num4==0:
					print("y_points_detect it is a 3D")
					continue
				else:#进行slope判断
					bool_num5=self.use_math_to_detect_y(depth_img,int(box[1]),self.middle_x,length_y)
					if bool_num5==0:
						print("y_slope_ok")
						continue
					else:
						index_del.append(i)
						print("y_slope_not_ok")
						continue
#--------------------------------------------------------------------------------------------------------------------------------
		print("type of result_boxes_before"+str(type(result_boxes)))
		print("result_boxes_before"+str(result_boxes))
		print("result_scores_before"+str(result_scores))
		print("result_classid_before"+str(result_classid))
		result_boxes_new1=np.delete(result_boxes,index_del,0)
		result_scores_new1=np.delete(result_scores,index_del,0)
		result_classid_new1=np.delete(result_classid,index_del,0)
		print("result_boxes_after"+str(result_boxes_new1))
		print("result_scores_after"+str(result_scores_new1))
		print("result_classid_after"+str(result_classid_new1))
		return result_boxes_new1,result_scores_new1,result_classid_new1