import random

import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np


"""
定义图像处理的函数
"""

'''定义了一个判断点是否在多边形内的函数,返回值为是否在多边形内:是,返回1;否,返回0'''
def rayCasting(p, poly):
    # p是需要判断的点，ploy是多边形的顶点
    px = p['x']  # 取值
    py = p['y']
    flag = 0  # 射线穿过多边形边界的次数为奇数时点在多边形内

    i = 0
    l = len(poly)  # 获取多边形顶点的数量
    j = l - 1
    # for(i = 0, l = poly.length, j = l - 1; i < l; j = i, i++):
    while i < l:
        # 取两个顶点，顶点是顺时针排列的，两个顶点方便后面形成线段
        sx = poly[i]['x']
        sy = poly[i]['y']
        tx = poly[j]['x']
        ty = poly[j]['y']

        # 点与多边形顶点重合
        if (sx == px and sy == py) or (tx == px and ty == py):
            return (px, py)

        # 判断线段两端点是否在射线两侧
        if (sy < py <= ty) or (sy >= py > ty):
            # 线段上与射线 Y 坐标相同的点的 X 坐标
            x = sx + (py - sy) * (tx - sx) / (ty - sy)
            # 点在多边形的边上
            if x == px:
                return px, py
            # 射线穿过多边形的边界
            if x > px:
                flag = 1 - flag  # 以第一次为例，false变成了true，代表flag为true的时候点在多边形内
        j = i
        i += 1

    return flag


'''定义了一个把字符串中的点转化为列表的函数，返回的是包含(x,y)的坐标列表'''
def getpoint(a):
    i = 0
    p = []
    while i < len(a[1::2]):  # 除去','以后的元素，并且步长为2
        p.append({'x': float(a[::2][i]), 'y': float(a[1::2][i])})  # x为从0开始，step=2；y为从1开始，step=2
        i += 1
    return p


'''判断在多边形内的点的坐标与下标,都是列表形式,point_in是在多边形内的坐标值,point_in_index返回的是在多边形内点在原始列表中的下标'''
# 根据输入的点循环判断芝麻是否在多边形里面，如果全部在外面则输出no,否则输出芝麻的坐标
def judege(point, dbx):
    point_in = []
    point_in_index = []
    point = getpoint(point)
    dbx = getpoint(dbx)
    count = 0
    for p in point:
        count = count + 1
        if rayCasting(p, dbx) == 1:
            point_in.append(p)
            point_in_index.append(count)
            print(p, count)

    return point_in, point_in_index


'''对图像进行形态学处理：腐蚀，矩形膨胀，十字膨胀，矩形膨胀，返回值是经过处理以后的图像'''
def morphology(original_img):
    img_Erode = cv.erode(original_img, np.ones((40, 40), np.uint8))  # 进行腐蚀
    img_Dilate = cv.dilate(img_Erode, np.ones((20, 20), np.uint8))  # 进行第一次矩形膨胀
    img_Dilate = cv.dilate(img_Dilate, cv.getStructuringElement(cv.MORPH_CROSS, (10, 10)), iterations=2)  # 进行十字膨胀
    img_Dilate = cv.dilate(img_Dilate, np.ones((20, 20), np.uint8))  # 进行第二次矩形膨胀

    return img_Dilate


'''<测试函数>绘制轮廓并输出点集'''
def Contours_test(original_img, img):
    contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)  # 查找轮廓
    height, width = img.shape[:2]  # 获取图片的长和宽
    index = 0  # 对下标进行初始化
    max = 0  # 对最大面积值进行初始化
    for c in range(len(contours)):
        x, y, w, h = cv.boundingRect(contours[c])  # 获取图片的长和宽
        if h >= height or w >= width:  # 检测到的轮廓的长和宽等于图片的长和宽，代表此轮廓有问题
            continue  # 跳过有问题的轮廓
        area = cv.contourArea(contours[c])  # 对没有问题的轮廓求面积
        if area > max:  # 找最大面积的轮廓的下标
            max = area
            index = c

    cnt = contours[index]

    imgRes_1 = cv.drawContours(original_img, [cnt], -1, (0, 0, 255), 2)

    epsilon = 0.02 * cv.arcLength(cnt, True)  # 进行轮廓几何近似化处理，设置阈值，阈值越小，轮廓越近似
    approx = cv.approxPolyDP(cnt, epsilon, True)  # 输出点集

    imgRes_2 = cv.drawContours(original_img, [approx], -1, (0, 0, 255), 2)

    return approx, imgRes_1, imgRes_2


'''绘制轮廓并输出点集,返回值是多边形顶点坐标列表，两个图像'''
def Contours(img):
    contours, hierarchy = cv.findContours(img, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)  # 查找轮廓
    height, width = img.shape[:2]  # 获取图片的长和宽
    index = 0  # 对下标进行初始化
    max = 0  # 对最大面积值进行初始化
    for c in range(len(contours)):
        x, y, w, h = cv.boundingRect(contours[c])  # 获取图片的长和宽
        if h >= height or w >= width:  # 检测到的轮廓的长和宽等于图片的长和宽，代表此轮廓有问题
            continue  # 跳过有问题的轮廓
        area = cv.contourArea(contours[c])  # 对没有问题的轮廓求面积
        if area > max:  # 找最大面积的轮廓的下标
            max = area
            index = c

    cnt = contours[index]

    # imgRes_1 = cv.drawContours(img, [cnt], -1, (0, 0, 255), 2)

    epsilon = 0.02 * cv.arcLength(cnt, True)  # 进行轮廓几何近似化处理，设置阈值，阈值越小，轮廓越近似
    approx = cv.approxPolyDP(cnt, epsilon, True)  # 输出点集

    imgRes = cv.drawContours(img, [approx], -1, (0, 0, 255), 2)

    return approx, imgRes


'''测试函数，确定几何轮廓顶点与桌面实际重叠情况，输出为一张带有蒙版的图片'''
def put_mask(img_no_mask, approx_points):

    img_mask = img_no_mask.copy()

    # 获取原图大小，和需要画的蒙版的顶点
    x_y_w_h = np.zeros(img_no_mask.shape, dtype=np.uint8)
    points = np.array([approx_points], dtype=np.int32)

    cv.polylines(img_mask, points, isClosed=True, thickness=2, color=(255, 0, 0))

    return img_mask


'''测试函数，随机生成10个点在图内，检测是否是在桌面内，返回值是点的坐标列表和含点的图片'''
def random_points(image):
    image_points = image.copy()
    height, weight = image.shape[:2]
    ax = []

    point_size = 5
    point_color = (0, 0, 255)
    thickness = 5

    for i in range(20):
        x = random.randint(0, weight)
        y = random.randint(0, height)
        ax.append(x)
        ax.append(y)
        cv.circle(image_points, (x, y), point_size, point_color, thickness)
    print("生成的随机点坐标为" + str(ax))

    return ax, image_points

# def judege_test(image, points, border):
#     index = 0
#     p = getpoint(points)
#     b = getpoint(border)
#     point_in, point_in_index = judege(p, b)
#
#     print(point_in, point_in_index)


if __name__ == '__main__':

    path = '../image/t1.jpg'
    img = plt.imread(path)

    imgRN = morphology(img)

    imgRN = cv.cvtColor(imgRN, cv.COLOR_BGR2GRAY)
    ret, imgRN = cv.threshold(imgRN, 20, 255, cv.THRESH_BINARY)

    approx, res = Contours(imgRN)
    # print(approx)
    imgMask = put_mask(img, approx)
    ax, imgPoints = random_points(imgMask)
    # judege_test(imgPoints, ax, approx)

    fig = plt.figure()

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.set_title("img")

    plt.xticks([]), plt.yticks([])
    ax1.imshow(img[..., ::-1])

    ax1 = fig.add_subplot(2, 2, 2)
    ax1.set_title("1")
    plt.xticks([]), plt.yticks([])
    ax1.imshow(imgRN, cmap='gray')

    ax1 = fig.add_subplot(2, 2, 3)
    ax1.set_title("2")
    plt.xticks([]), plt.yticks([])
    ax1.imshow(imgMask)

    ax1 = fig.add_subplot(2, 2, 4)
    ax1.set_title("3")
    plt.xticks([]), plt.yticks([])
    ax1.imshow(imgPoints)

    plt.show()
