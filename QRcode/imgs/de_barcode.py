# -*- coding:utf-8 -*-
from QRMatrix import *
import cv2
import sys
import numpy as np

#获得数组中最大值
def Max(list):
    max=-1
    for i in range(list.length):
        if(max<list[i]):
            max=list[i]
    return max

#获得数组中最小值
def Min(list):
    min=9999
    for i in range(list.length):
        if(min>list[i]):
            min=list[i]
    return min

#读入图像,以灰度图方式读入
#img=cv2.imread("G:\IP_Class\generate.png",0)#以灰度图方式读入
img = cv2.imread("barcode1.png",1)
img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#需要预处理
#TODO

#使用canny算法提取边缘
edges=cv2.Canny(img_gray,100,200)
cv2.imshow('edges',edges)
cv2.imwrite("edges.png",edges)
cv2.waitKey(0)

#提取全部轮廓并获得轮廓的嵌套关系
img_fc, contours, hierarchy = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
hierarchy = hierarchy[0]
found = []
#找到边缘嵌套超过5层的外轮廓，即定位点
for i in range(len(contours)):
    k = i
    c = 0
    while hierarchy[k][2] != -1:
        k = hierarchy[k][2]
        c = c + 1
    if c >= 5:
        found.append(i)

#绘制符合要求的轮廓，即大于等于5层的嵌套
img_dc = img.copy()
for i in found:
    cv2.drawContours(img_dc, contours, i, (0, 255, 0), 2)
cv2.imshow('draw_contour',img_dc)
cv2.imwrite("contours.png",img_dc)
cv2.waitKey(0)

draw_img = img.copy()
boxes=[]  #包围盒组

for i in found:
    rect = cv2.minAreaRect(contours[i]) #获得轮廓的最小外接矩形
    box = cv2.boxPoints(rect)
    box = np.int0(box)
    cv2.drawContours(draw_img,[box],0,(0,0,255),2)
    box = map(tuple, box)
    boxes.append(box)
 
cv2.imshow('minAreaRect',draw_img)
cv2.imwrite("minAreaRect.png",draw_img)
cv2.waitKey(0)

Xs=[]
Ys=[]

for box in boxes:
    for point in box:
        Xs.append(point[0])
        Ys.append(point[1])

#获得对角线点坐标
x1=min(Xs)
y1=min(Ys)
x2=max(Xs)
y2=max(Ys)

location=img.copy()

cv2.rectangle(location,(x1-3,y1-3), (x2+6,y2+6), (0, 255, 0), 3)
cv2.imshow('Location',location)
cv2.imwrite("location.png",location)
cv2.waitKey(0)

#选取感兴趣域
roi=img_gray[y1-3:y2+6,x1-3:x2+6]
cv2.imshow("ROI",roi)  
cv2.imwrite("Roi.png",roi)  
cv2.waitKey(0)



#二值化
binary=roi.copy()
ret,binary=cv2.threshold(roi,127,255,cv2.THRESH_BINARY)

#显示图像
cv2.imshow('binary',binary)
cv2.imwrite("Binary.png",binary)
cv2.waitKey(0)

#初始化解码类，并进行解码
QRCode = QRMatrix('decode', binary)
print(QRCode.decode())
cv2.waitKey(0)

#关闭所有窗口释放资源
cv2.destroyAllWindows()