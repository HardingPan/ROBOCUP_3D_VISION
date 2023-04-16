import cv2 as cv
import matplotlib.pyplot as plt
import numpy as np

'''设置中文的函数'''
def set_Chinese():
    import matplotlib
    matplotlib.rcParams['font.sans-serif'] = ['SimHei']
    matplotlib.rcParams['axes.unicode_minus'] = False


'''对图像进行形态学处理：腐蚀，矩形膨胀，十字膨胀，矩形膨胀'''
def morphology(original_img):
    img_Erode = cv.erode(original_img, np.ones((40, 40), np.uint8))
    img_Dilate = cv.dilate(img_Erode, np.ones((20, 20), np.uint8))
    img_Dilate = cv.dilate(img_Dilate, cv.getStructuringElement(cv.MORPH_CROSS, (10, 10)), iterations=2)
    img_Dilate = cv.dilate(img_Dilate, np.ones((20, 20), np.uint8))

    return img_Dilate


if __name__ == '__main__':
    set_Chinese()

    path = '../image/t6.jpg'
    img = plt.imread(path)

    imgRN = morphology(img)

    imgRN = cv.cvtColor(imgRN, cv.COLOR_BGR2GRAY)
    ret, imgRN = cv.threshold(imgRN, 20, 255, cv.THRESH_BINARY)

    # 提取轮廓并绘制轮廓
    contours, hierarchy = cv.findContours(imgRN, cv.RETR_TREE, cv.CHAIN_APPROX_NONE)
    cnt = contours[0]
    draw_img = img.copy()
    res1 = cv.drawContours(draw_img, [cnt], -1, (0, 0, 255), 2)

    # 近似轮廓
    epsilon = 0.02 * cv.arcLength(cnt, True)  # 设置阈值，阈值越小，轮廓越近似
    approx = cv.approxPolyDP(cnt, epsilon, True)
    draw_img = img.copy()
    res2 = cv.drawContours(draw_img, [approx], -1, (0, 0, 255), 2)
    print(approx)
    fig = plt.figure()

    ax1 = fig.add_subplot(2, 2, 1)
    ax1.set_title("原图")

    plt.xticks([]), plt.yticks([])
    ax1.imshow(img[..., ::-1])

    ax1 = fig.add_subplot(2, 2, 2)
    ax1.set_title("腐蚀")
    plt.xticks([]), plt.yticks([])
    ax1.imshow(imgRN, cmap='gray')

    ax1 = fig.add_subplot(2, 2, 3)
    ax1.set_title("轮廓检测")
    plt.xticks([]), plt.yticks([])
    ax1.imshow(res1)

    ax1 = fig.add_subplot(2, 2, 4)
    ax1.set_title("轮廓几何化")
    plt.xticks([]), plt.yticks([])
    ax1.imshow(res2)

    plt.show()