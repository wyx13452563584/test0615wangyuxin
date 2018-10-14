from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.urls import reverse

import numpy as np
import pandas as pd
import math
from pandas import Series,DataFrame
import tushare as ts

import matplotlib.pyplot as plt

def create_boll(data, ndays):
    """
        计算布林线指标
        基于ndays日均线计算
    """

    ma = data['close'].rolling(ndays).mean()
    sd = data['close'].rolling(ndays).std()

    bu = ma + (2 * sd)
    upper = pd.Series(bu, name='bu')
    data = data.join(upper)

    bl = ma - (2 * sd)
    lower = pd.Series(bl, name='bl')
    data = data.join(lower)

    bm = pd.Series(ma, name='bm')
    data = data.join(bm)

    return data

#定义标准化函数
def guiyi(x):
    return (x - 0)/(max(x) - min(x))


def fun_y(lmc):
    # 创建偏移数据,shift(正数)向下移动数据。
    X = lmc[['liangfugy']]
    yy = lmc[['close', 'bm']]
    for i in range(0, 70):
        X['ls{}'.format(str(i + 1))] = lmc['liangfugy'].shift(i + 1)
    for i in range(0, 10):
        yy['wl{}'.format(str(i + 1))] = lmc['close'].shift(-1 - i)
    yy['bm32'] = lmc['bm'].shift(32)

    # 准备数据
    X0 = X[-1:]
    X = X[70:-10]
    yy = yy[70:-10]
    yy1 = yy.copy()
    close = yy.pop('close')
    bm32 = yy.pop('bm32')
    bm = yy.pop('bm')
    yy2 = yy.copy()

    # 计算买卖点条件
    yy['B1'] = (yy2.max(axis=1) - bm) / close * 100 > 2  # 未来16个周期最高涨幅
    yy['B2'] = (yy1[['wl1', 'wl2', 'wl3']].mean(axis=1) - bm) / close * 100 < 1  # 未来3个周期平均涨幅
    yy['B3'] = False
    for i in range(0, len(yy1)):
        # 均线值大于历史均线值
        if yy1['bm'][i] > yy1['bm32'][i]:
            yy['B3'][i] = True
    yy['B'] = yy['B1'] * yy['B2'] * yy['B3']  # 定位买点

    # yy['S1'] = (yy2.min(axis = 1)-bm)/close*100 < -2
    # yy['S2'] = (yy1[['wl1','wl2','wl3']].mean(axis = 1)-bm)/close*100 > -1
    # yy['S3'] = False
    # for i in range(0,len(yy1)):
    #     #均线值大于历史均线值
    #     if yy1['bm'][i] < yy1['bm32'][i]:
    #         yy['S3'][i] = True
    # yy['S'] = yy['S1']*yy['S2']*yy['S3']

    # 计算涨跌标签：1,0，-1
    yy['y'] = 0
    for i in range(0, len(yy)):
        if yy['B'][i]:
            yy['y'][i] = 1
    #     if yy['S'][i]:
    #         yy['y'][i] = -1
    y = yy['y']
    for i in range(1, len(y) - 1):
        if y[i] != y[i + 1] and y[i] != y[i - 1]:
            y[i] = y[i + 1]

    return X, y