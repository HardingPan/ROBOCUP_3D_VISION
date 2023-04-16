import cv2 as cv
import numpy as np

cap = cv.VideoCapture(0)

while (True):
    ret,frame = cap.read()
    frame = cv.flip(frame,2)

    if ret == True:

        # b = frame[0,:,:]
        # g = frame[:,0,:]
        # r = frame[:,:,0]
        # clahe = cv.createCLAHE(2.0,(8,8))
        # res_b = np.asarray(cv.resize(clahe.apply(b),(480,480)),np.uint8)
        # res_g = np.asarray(cv.resize(clahe.apply(g),(480,480)),np.uint8)
        # res_r = np.asarray(cv.resize(clahe.apply(r),(480,480)),np.uint8)
        # print(res_r.shape,res_g.shape,res_b.shape)
        # res = res_r + res_g + res_b0

        hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
        low_hsv = np.array([0, 127, 128])
        high_hsv = np.array([2, 255, 255])
        mask = cv.inRange(hsv,low_hsv,high_hsv)

        ret,thresh = cv.threshold(mask,0,255,cv.THRESH_BINARY)

        kernel1 = np.ones((15,15),np.uint8)
        kernel2 = np.ones((10,10),np.uint8)
        # erode = cv.erode(thresh,kernel1,iterations=1)
        dilate = cv.dilate(thresh,kernel1,iterations=1)
        erode = cv.erode(dilate, kernel2, iterations=1)
        # dilate = cv.dilate(erode, kernel2, iterations=1)
        opening = cv.morphologyEx(erode,cv.MORPH_OPEN,kernel1,iterations=2)
        close = cv.morphologyEx(opening,cv.MORPH_CLOSE,kernel2,iterations=2)

        contours,heirary = cv.findContours(close,cv.RETR_EXTERNAL,cv.CHAIN_APPROX_NONE)
        # cv.drawContours(frame,contours,-1,(0,255,0),2)
        if len(contours) > 0:
            t = contours[0]
            for i in range(len(contours)):
                if cv.contourArea(contours[i]) > cv.contourArea(t):
                    t = contours[i]
                # # x,y,w,h = cv.boundingRect(t)
                # print(x,y,w,h)
            r = cv.minAreaRect(t)
            box = cv.boxPoints(r)
            box = np.int0(box)
            x,y,w,h = cv.boundingRect(box)
            print(box)
            print(r[2])
            cv.drawContours(frame, [box], -1, (153, 153, 0), 2)

        cv.imshow('mask', mask)
        cv.imshow('dilate',dilate)
        cv.imshow('erode', erode)
        cv.imshow('frame', frame)
    key = cv.waitKey(2)
    if key == 27:
        break

cap.release()
cv.destroyAllWindows()

