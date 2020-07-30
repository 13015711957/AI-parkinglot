import pandas as pd
import os
import conf
import pygame
import datetime
from statistics import *
cdir=os.getcwd()
path=cdir+'/datafile/'
if not os.path.exists(path+'停车场车辆表.xlsx'):
    os.makedirs(path)
    carsfile=pd.DataFrame(columns=['carnumber','date'])
    carnfile=pd.DataFrame(columns=['carnumber','in_date','out_date','duration','price'])
    carsfile.to_excel(path+'停车场车辆表.xlsx',   sheet_name='data')
    carnfile.to_excel(path + '停车场信息表.xlsx', sheet_name='data')

#读取文件内容
pi_table = pd.read_excel(path + '停车场车辆表.xlsx', sheet_name='data',index_col=0)
pi_infor_table=pd.read_excel(path+'停车场信息表.xlsx',sheet_name='data')

cars=list(pi_table.index)

#数据展示
def park_inf(screen,font):
    update_chart()
    image = pygame.image.load('img/a.png')
    image = pygame.transform.scale(image, (280, 500))
    screen.blit(image, (340, 0))

    pygame.draw.rect(screen, conf.BG, [660, 0, 500, 300], 0)

    headfont = pygame.font.SysFont('SimHei', 18)
    pi_table = pd.read_excel(path + '停车场车辆表.xlsx', sheet_name='data')
    nums=100-len(pi_table)
    txt='共有车位：100'+'    剩余车位：'+str(nums)+'(前10条)'
    print(txt)
    text = headfont.render(txt, True, conf.WHITE)
    textRect = text.get_rect()
    textRect.center = (830, 20)
    screen.blit(text, textRect)
    text = font.render('-------------------------------------', True, conf.WHITE)
    textRect = text.get_rect()
    textRect.center = (830, 35)
    screen.blit(text, textRect)

    text = font.render('车牌号          入库时间', True, conf.WHITE)
    textRect = text.get_rect()
    textRect.center = (810, 50)
    screen.blit(text, textRect)
    pi_table=pi_table.iloc[::-1]
    for i in range(10):
        txt=pi_table.iloc[i][0]+'  '+pi_table.iloc[i][1]
        text = font.render(txt, True, conf.WHITE)
        textRect = text.get_rect()
        textRect.center = (830, 70+i*20)
        screen.blit(text, textRect)


#车辆入库
def car_append(carnumber):
    try:
        pi_table = pd.read_excel(path + '停车场车辆表.xlsx', sheet_name='data')
        pi_infor_table = pd.read_excel(path + '停车场信息表.xlsx', sheet_name='data')
        now_time = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S ')

        temp = pd.read_excel(path + '停车场车辆表.xlsx', sheet_name='data', index_col=0)
        cars = list(temp.index)
        if carnumber in cars:
            return False

        pi_table = pi_table.append({'carnumber': carnumber, 'date': now_time}, ignore_index=True)
        pi_table.set_index(['carnumber'], inplace=True)


        pi_infor_table = pi_infor_table.append({'carnumber': carnumber, 'in_date': now_time}, ignore_index=True)
        pi_infor_table.set_index(['in_date'], inplace=True)

        pd.DataFrame(pi_table).to_excel(path + '停车场车辆表.xlsx', sheet_name='data', header=True)
        pd.DataFrame(pi_infor_table).to_excel(path + '停车场信息表.xlsx', sheet_name='data', header=True)
    except:
        return False

    return True

#车辆出库
def car_pop(carnumber):
    result={'state':1,'duration':0,'price':0}
    try:
        pi_table = pd.read_excel(path + '停车场车辆表.xlsx', sheet_name='data')
        pi_infor_table = pd.read_excel(path + '停车场信息表.xlsx', sheet_name='data')
        out_date = datetime.datetime.now()
        now_time = datetime.datetime.now().strftime('%Y.%m.%d %H:%M:%S ')

        pi_table.set_index(['carnumber'], inplace=True)
        in_date = pi_table.loc[carnumber, ['date']][0]
        in_time = datetime.datetime.strptime(in_date, '%Y.%m.%d %H:%M:%S ')

        pi_table = pi_table.drop(carnumber, axis=0)

        pi_infor_table.set_index(['in_date'], inplace=True)
        pi_infor_table.loc[in_date, ['out_date', ]] = [now_time]

        duration = (out_date - in_time).seconds * 1.00 / 3600
        duration = round(duration, 2)
        price = duration * 10

        result['duration']=duration
        result['price']=price

        pi_infor_table.loc[in_date, ['duration']] = [duration]
        pi_infor_table.loc[in_date, ['price']] = [price]

        pd.DataFrame(pi_table).to_excel(path + '停车场车辆表.xlsx', sheet_name='data', header=True)
        pd.DataFrame(pi_infor_table).to_excel(path + '停车场信息表.xlsx', sheet_name='data', header=True)
    except:
        result['state']=0

    return result



