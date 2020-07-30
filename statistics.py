import pandas as pd
import os
import matplotlib.pyplot as plt
import datetime
import matplotlib
def update_chart():

    cdir=os.getcwd()
    path=cdir+'/datafile/'
    pi_infor_table=pd.read_excel(path+'停车场信息表.xlsx',sheet_name='data')
    pi_infor_table.set_index(['in_date'], inplace=True)

    matplotlib.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文

    attr=list(range(1,31))
    print(attr)
    money=[0 for _ in range(30)]
    for i in pi_infor_table.values:
        if isinstance(i[1],str):
            temp=datetime.datetime.strptime(i[1], '%Y.%m.%d %H:%M:%S ')
            money[temp.day-1]+=i[3]
    print(money)

    plt.figure(figsize=(4, 8))
    plt.ylabel("日期")
    plt.xlabel("收入（元）")
    plt.title("本月收入")


    y_major_locator=plt.MultipleLocator(1)
    ax=plt.gca()
    ax.yaxis.set_major_locator(y_major_locator)
    b=plt.barh(attr,money,0.8,color="green")

    for rect in b:
        w=rect.get_width()
        if not w==0:
            ax.text(w,rect.get_y()+rect.get_height()/2,'%d'%int(w),ha='left',va='center')
    plt.savefig("img/a.png")
