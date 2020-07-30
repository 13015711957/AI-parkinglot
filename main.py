import pygame
import cv2
import pandas as pd
import os
import btn
import conf
from OCRUtil import *
from fileUtil import *
import numpy as np
from tkinter import *
from tkinter import messagebox
import re
pygame.init()
pygame.display.set_caption("AI停车场车牌识别计费系统")
ico=pygame.image.load("img/ico.png")
pygame.display.set_icon(ico)
screen=pygame.display.set_mode(conf.size)
screen.fill(conf.BG)
clock=pygame.time.Clock()

try:
    cam=cv2.VideoCapture(0)
    #由于电脑只有一个摄像头，所以就出入库共用一个
    #cam1=cv2.VideoCapture(1)
except:
    print("请连接摄像头")



font = pygame.font.SysFont('SimHei',18)

button_in=btn.Button(screen, (190,215), 100, 35, conf.BLUE, conf.WHITE, '入库识别', 20)
button_in.draw_button()


button_out=btn.Button(screen, (190,445), 100, 35, conf.BLUE, conf.WHITE, '出库识别', 20)
button_out.draw_button()

park_inf(screen,font)
Running=True

def button_click(pos):
    if pos[0]>90 and pos[0]<190 and pos[1]>180 and pos[1]<215:
        print('入库识别')
        return 0
    if pos[0]>90 and pos[0]<190 and pos[1]>410 and pos[1]<445:
        print('出库识别')
        return 1
#隐藏TK主窗口
Tk().wm_withdraw()
while Running:

    #这里只写了一个摄像头
    suces,img=cam.read()
    cv2.imwrite('img/test.jpg',img)

    image1=pygame.image.load('img/test.jpg')
    image1=pygame.transform.scale(image1,(300,175))
    screen.blit(image1,(0,0))

    image2 = pygame.image.load('img/test.jpg')
    image2 = pygame.transform.scale(image2, (300, 175))
    screen.blit(image2, (0, 230))

    for event in pygame.event.get():
        if event.type ==pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type==pygame.MOUSEBUTTONDOWN:
            print(event.pos,event.button)
            type=button_click(event.pos)

            if type==0:
                cv2.imwrite('img/img_in.jpg', img)
                carnumber = getch(type)
                if not carnumber:
                    messagebox.showinfo('提示', '识别失败')
                    continue
                if car_append(carnumber):
                    messagebox.showinfo('提示', '车牌号：'+carnumber+'入库成功')
                else:
                    messagebox.showinfo('提示', '车牌号：' + carnumber + '入库失败')
                pass
            elif type==1:
                cv2.imwrite('img/img_out.jpg', img)
                carnumber = getch(type)
                if not carnumber:
                    messagebox.showinfo('提示', '识别失败')
                    continue
                result=car_pop(carnumber)
                if result['state']==1:
                    messagebox.showinfo('提示', '车牌号：' + carnumber + '出库成功  '+'停车时长'+str(result['duration'])+'个小时，收入'+str(result['price'])+'元')
                else:
                    messagebox.showinfo('提示', '车牌号：' + carnumber + '出库失败')
                pass
            park_inf(screen, font)


    pygame.display.flip()
    clock.tick(conf.FPS)




