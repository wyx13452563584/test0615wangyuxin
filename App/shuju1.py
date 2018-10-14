from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

from App.fun import create_boll,fun_y,guiyi
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
from pandas import Series,DataFrame
import tushare as ts


def fenxi(request):
    if request.method == "GET":
        dict = {
            "title": '用户注册'
        }
        return render(request, 'register.html', context=dict)

    elif request.method == "POST":

        daima = request.POST.get("daima")
        if daima == '':
            daima = '600519'

        dict = {
            'daima': daima
        }

        listX = []
        listy = []
        data = ts.get_k_data(code=daima, ktype='15')
        data.index = data['date']
        data.pop('date')

        # 基于n日均线计算boll
        n = 26
        boll = create_boll(data, n)
        # 涨跌幅度
        boll['zdfu'] = boll['close'].pct_change()
        # 涨跌标签：1，-1
        boll['zd'] = np.sign(boll['zdfu'])
        boll['fen'] = boll['close'] - boll['bm']
        # 去掉含空值行
        con = boll.notnull().all(axis=1)
        boll = boll[con]



        lmc = pd.DataFrame(index=boll.index)
        lmc['zd'] = boll['zd']
        lmc['bm'] = boll['bm']
        lmc['close'] = boll['close']
        lmc['fengy'] = boll[['fen']].apply(guiyi)

        lmc['liang'] = boll['volume']
        lmc['liangfu'] = (boll['fen']) * lmc['liang']
        lmc['liangfugy'] = lmc[['liangfu']].apply(guiyi)
        # 量脉冲限制条件
        for i in range(0, len(lmc)):
            if (boll['close'][i] > boll['bl'][i]) and boll['zdfu'][i] < 0:
                lmc['liangfugy'][i] = lmc['fengy'][i]
            if (boll['close'][i] < boll['bm'][i]) and boll['zdfu'][i] > 0:
                lmc['liangfugy'][i] = 0

        figure = plt.figure(figsize=(14, 7))
        ax1 = figure.add_subplot(111)

        ax1.plot((boll['close'][-200:]), 'k', alpha=0.8)
        ax1.plot(lmc['liangfugy'][-200:] * np.min(boll['close'][-200:])/10 + np.min(boll['close'][-200:]), 'b', alpha=0.5)

        ax1.set_xticks(range(0, len(boll['close'][-200:]), 20))
        ax1.set_xticklabels(boll['close'][-200:].index[::20], rotation=30)
        ax1.grid(b=True, linestyle="--")
        ax1.set_title("{}".format(daima), fontsize=20, color="black")
        figure.savefig("./static/img_gupiao/{}01.jpg".format(daima), facecolor="w", pad_inches=5)



        X, y = fun_y(lmc)
        listX.append(X)
        listy.append(y)

        return render(request, 'fenxi.html', context= dict)

