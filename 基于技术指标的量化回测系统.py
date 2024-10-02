from tkinter import *
import pandas as pd
import requests
import warnings
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import os

root = Tk()
root.geometry("515x320+550+250")
root.title("基于技术指标的量化回测系统")

frame01 = Frame(root, width=150, height=160)
frameKDJ = Frame(root, width=140, height=130)
frameCMO = Frame(root, width=140, height=130)
frameADX = Frame(root, width=140, height=130)
frameBLD = Frame(root, width=140, height=130)
frameDPO = Frame(root, width=140, height=130)
frameEMV = Frame(root, width=140, height=130)
frame01.place(x=10, y=100)
frameKDJ.place(x=190, y=110)

time_begin = StringVar()
time_end = StringVar()
money = IntVar()
code = StringVar()
KDJ01 = IntVar()
KDJ02 = IntVar()
CMO01 = IntVar()
DPO01 = IntVar()
EMV01 = IntVar()
time_begin.set("2020-01-01")
time_end.set("2022-01-01")
money.set(10000)
code.set("1.000300")
KDJ01.set(30)
KDJ02.set(70)
CMO01.set(0)
DPO01.set(0)
EMV01.set(0)
entry01 = Entry(root, textvariable=time_begin, width=10, justify="right")
entry02 = Entry(root, textvariable=time_end, width=10, justify="right")
entry03 = Entry(root, textvariable=money, width=10, justify="right")
entry04 = Entry(root, textvariable=code, width=10, justify="right")
entryKDJ01 = Entry(frameKDJ, textvariable=KDJ01, width=5, justify="center")
entryKDJ02 = Entry(frameKDJ, textvariable=KDJ02, width=5, justify="center")
entryCMO01 = Entry(frameCMO, textvariable=CMO01, width=5, justify="center")
entryDPO01 = Entry(frameDPO, textvariable=DPO01, width=5, justify="center")
entryEMV01 = Entry(frameEMV, textvariable=EMV01, width=5, justify="center")
entry01.place(x=10, y=10)
entry02.place(x=250, y=10)
entry03.place(x=240, y=40)
entry04.place(x=10, y=40)
entryKDJ01.place(x=80, y=50)
entryKDJ02.place(x=80, y=75)
entryCMO01.place(x=80, y=50)
entryDPO01.place(x=80, y=50)
entryEMV01.place(x=80, y=50)

label01 = Label(root, text="——至——", width=10, justify="left")
label02 = Label(root, text="￥", justify="left")
label03 = Label(root, text="选择指标", width=8, justify="center")
label04 = Label(root, text="股票代码", width=8, justify="left")
label05 = Label(root, text="本金", width=4, justify="left")
label06 = Label(root, text="策略", width=4, justify="center")
labelKDJ01 = Label(frameKDJ, text="当指标上穿信号时买入", width=24, justify="left")
labelKDJ02 = Label(frameKDJ, text="当指标下穿信号时卖出", width=24, justify="left")
labelKDJ03 = Label(frameKDJ, text="信号一：", width=8, justify="center")
labelKDJ04 = Label(frameKDJ, text="信号二：", width=8, justify="center")
labelCMO01 = Label(frameCMO, text="当指标大于信号时买入", width=24, justify="center")
labelCMO02 = Label(frameCMO, text="当指标小于信号时卖出", width=24, justify="center")
labelCMO03 = Label(frameCMO, text="信号一：", width=8, justify="center")
labelDPO01 = Label(frameDPO, text="当指标大于信号时买入", width=24, justify="center")
labelDPO02 = Label(frameDPO, text="否则卖出", width=8, justify="center")
labelDPO03 = Label(frameDPO, text="信号一：", width=8, justify="center")
labelEMV01 = Label(frameEMV, text="当指标大于信号时买入", width=24, justify="center")
labelEMV02 = Label(frameEMV, text="当指标小于信号时卖出", width=24, justify="center")
labelEMV03 = Label(frameEMV, text="信号一：", width=8, justify="center")
labelADX01 = Label(frameADX, text="该指标不需要输入信号", width=24, justify="center")
labelBLD01 = Label(frameBLD, text="该指标不需要输入信号", width=24, justify="center")
label01.place(x=130, y=10)
label02.place(x=315, y=40)
label03.place(x=40, y=80)
label04.place(x=100, y=40)
label05.place(x=200, y=40)
label06.place(x=240, y=80)
labelKDJ01.place(x=-10, y=0)
labelKDJ02.place(x=-10, y=25)
labelKDJ03.place(x=10, y=50)
labelKDJ04.place(x=10, y=70)
labelCMO01.place(x=-10, y=0)
labelCMO02.place(x=-10, y=25)
labelCMO03.place(x=10, y=50)
labelDPO01.place(x=-10, y=0)
labelDPO02.place(x=40, y=25)
labelDPO03.place(x=10, y=50)
labelEMV01.place(x=-10, y=0)
labelEMV02.place(x=-10, y=25)
labelEMV03.place(x=10, y=50)
labelADX01.place(x=-10, y=30)
labelBLD01.place(x=-10, y=30)

text01 = Text(root, width=25, height=19)
text01.insert(1.0, "KDJ指标，由George Lane首创，最早用于期货市场。他的主要理论依据是：当价格上涨时，收市价倾向于接近当日价格区间的上端；相反"
                   "，在下降趋势中收市价趋向于接近当日价格区间的下端。在股市和期市中，因为市场趋势上升而未转向前，每日多数都会偏向于高价位收市，"
                   "而下跌时收市价就常会偏于低位。")
text01.place(x=340, y=0)


def refresh():
    frameKDJ.place_forget()
    frameCMO.place_forget()
    frameADX.place_forget()
    frameBLD.place_forget()
    frameDPO.place_forget()
    frameEMV.place_forget()
    text01.delete(1.0, END)
    if zhibiao.get() == "KDJ":
        frameKDJ.place(x=190, y=110)
        text01.insert(1.0, "KDJ指标，由George Lane首创，最早用于期货市场。他的主要理论依据是：当价格上涨时，收市价倾向于接近当日价格区间的"
                           "上端；相反，在下降趋势中收市价趋向于接近当日价格区间的下端。在股市和期市中，因为市场趋势上升而未转向前，每日多数都"
                           "会偏向于高价位收市，而下跌时收市价就常会偏于低位。")
    elif zhibiao.get() == "CMO":
        frameCMO.place(x=190, y=110)
        text01.insert(1.0, "CMO指标即钱德动量摆动指标，是由Tushar S.Chande提出的类似于RSI的指标，其在计算公式的分子中采用上涨日和下跌日"
                           "的数据，寻找极度超买和极度超卖的条件。")
    elif zhibiao.get() == "ADX":
        frameADX.place(x=190, y=110)
        text01.insert(1.0, "平均趋向指数（ADX）是一种常用的趋势衡量指标，利用多空趋向之变化差离与总和判定股价变动之平均趋势，可反映股价走势之"
                           "高低转折。ADX指标不能确定行情发展方向，但是能够行情趋势强弱。也就是说，它可以判断行情延着当前趋势运行的可能程度，"
                           "用以判断未来行情延续趋势还是反转。")
    elif zhibiao.get() == "BLD":
        frameBLD.place(x=190, y=110)
        text01.insert(1.0, "BOLL指标利用统计原理，求出股价的标准差及其信赖区间，从而确定股价的波动范围及未来走势，利用波带显示股价的安全高低"
                           "价位，因而也被称为布林带。\nBOLL指标中的上、中、下轨线所形成的股价信道的移动范围时不确定的，信道的上下限随着股价"
                           "的上下波动而变化。股价涨跌幅度加大时，带状区变宽，涨跌幅度狭小盘整时，带状区则变窄。在正常情况下，股价应始终处于股"
                           "价信道内运行。如果股价脱离股价信道运行，则意味着行情处于极端的状态下。")
    elif zhibiao.get() == "DPO":
        frameDPO.place(x=190, y=110)
        text01.insert(1.0, "区间震荡线（DPO）是一个排除价格趋势的震荡指标。他试图通过扣除前期移动平均价来消除长期趋势对价格波动的干扰，从而便"
                           "于发现价格短期的波动和超买超卖水平。")
    elif zhibiao.get() == "EMV":
        frameEMV.place(x=190, y=110)
        text01.insert(1.0, "简单波动指标（EMV），是位数不多的考虑价量关系的技术指标。它刻画了股价在下地的过程中，由于买气不断的萎靡退缩，致使"
                           "成交量逐渐的减少，EMV数值也因而尾随下降，知道股价下跌至某一个合理支撑区，捡便宜货的买单促使成交量再度活跃，EMV数"
                           "值于是作相对反应向上攀升，当EMV数值由负值向上趋近于零时，表示部分信心坚定的资金，成功的扭转了股价的跌势，行情不断"
                           "反转上扬，并且形成另一次的买进讯号。")


zhibiao = StringVar()
zhibiao.set("KDJ")
rdbtn01 = Radiobutton(frame01, text="KDJ", value="KDJ", variable=zhibiao, command=refresh)
rdbtn02 = Radiobutton(frame01, text="CMO动量指标", value="CMO", variable=zhibiao, command=refresh)
rdbtn03 = Radiobutton(frame01, text="ADX平均趋向指标", value="ADX", variable=zhibiao, command=refresh)
rdbtn04 = Radiobutton(frame01, text="布林带", value="BLD", variable=zhibiao, command=refresh)
rdbtn05 = Radiobutton(frame01, text="DPO区间震荡线", value="DPO", variable=zhibiao, command=refresh)
rdbtn06 = Radiobutton(frame01, text="EMV", value="EMV", variable=zhibiao, command=refresh)
rdbtn01.place(relx=0, rely=0)
rdbtn02.place(relx=0, rely=0.16)
rdbtn03.place(relx=0, rely=0.32)
rdbtn04.place(relx=0, rely=0.48)
rdbtn05.place(relx=0, rely=0.64)
rdbtn06.place(relx=0, rely=0.8)


def begin():
    warnings.filterwarnings("ignore")
    lst = []
    sdate = time_begin.get()
    s2date = time_end.get()
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/107.0.0.'
                      '0 Safari/537.36 Edg/107.0.1418.52'}

    def craw(sid):
        url = 'http://push2his.eastmoney.com/api/qt/stock/kline/get?fields1=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f11,f12' \
              ',f13&fields2=f51,f52,f53,f54,f55,f56,f57,f58,f59,f60,f61&beg=0&end=20500101&rtntype=6&secid={}&klt=101' \
              '&fqt=1'.format(sid)
        html = requests.get(url=url, headers=headers)
        sj_lst = html.json()['data']['klines']
        for i in sj_lst:
            sj = i.split(',')
            data = {}
            data['股票名称'] = html.json()['data']['name']
            data['代码'] = str(sid).split('.')[1]
            data['换手率'] = float(sj[10]) / 100
            data['收盘'] = float(sj[2])
            data['开盘'] = float(sj[1])
            data['最高'] = float(sj[3])
            data['最低'] = float(sj[4])
            data['涨跌幅'] = float(sj[8]) / 100
            data['涨跌额'] = float(sj[9])
            data['成交量'] = float(sj[5])
            data['成交额'] = float(sj[6])
            data['振幅'] = float(sj[7]) / 100
            data['日期'] = sj[0]
            lst.append(data)

    sid = code.get()
    craw(sid)
    result = pd.DataFrame(lst)
    result['日期筛选'] = pd.to_datetime(result['日期'])
    result = result.set_index('日期筛选')
    result = result.sort_values(by=["日期"], ascending=[True])
    result = result.truncate(before=sdate, after=s2date)
    result = result.sort_values(by=["股票名称", "日期"], ascending=[True, True])
    result.to_excel('result.xlsx', index=True, index_label=None)
    data0 = pd.read_excel('result.xlsx')
    data = data0.copy()
    data.rename(columns={'开盘': 'open', '最高': 'high', '最低': 'low', '收盘': 'close', '涨跌幅': 'pct_chg'},
                inplace=True)
    data['pre_close'] = data['close'].shift(1)
    data['pct_chg'] = (data['close'] - data['pre_close']) / data['pre_close']

    def calc_KDJ(data, n=14, m=3, l=3, S=3):
        close = data['close']
        low = data['low']
        high = data['high']
        rolling_low = low.rolling(n)
        rolling_high = high.rolling(n)
        RSV = (close - rolling_low.min()) / (rolling_high.max() - rolling_low.min()) * 100
        K = RSV.fillna(100).ewm(com=m - 1, adjust=False, min_periods=n).mean()
        D = K.fillna(100).ewm(com=l - 1, adjust=False, min_periods=n).mean()
        J = S * D - (S - 1) * K
        data['RSV'] = RSV
        data['K'] = K
        data['D'] = D
        data['J'] = J
        return data

    def calc_CMO(mkt_data, n=14, method='TA'):
        close = mkt_data['close']
        up = close.rolling(2).max() - close.shift(1)
        down = close.shift(1) - close.rolling(2).min()
        up_n = up.rolling(n).sum()
        down_n = down.rolling(n).sum()
        CMO = (up_n - down_n) / (up_n + down_n) * 100
        if method == 'own':
            mkt_data['up'] = up
            mkt_data['down'] = down
            mkt_data['up_n'] = up_n
            mkt_data['down_n'] = down_n
        mkt_data['CMO'] = CMO
        return mkt_data

    def calc_ADX(mkt_data, n=14):
        high = mkt_data['high']
        low = mkt_data['low']
        close = mkt_data['close']
        DMIp = high.rolling(2).max() - high.shift(1)
        DMIn = low.shift(1) - low.rolling(2).min()
        DMIp = DMIp * (DMIp >= DMIn)
        DMIn = DMIn * (DMIp < DMIn)
        TR = pd.concat([high, close.shift(1)], axis=1).max(axis=1) - pd.concat([low, close.shift(1)], axis=1).min(
            axis=1)
        DIp = DMIp.rolling(n).sum() / TR.rolling(n).sum()
        DIn = DMIn.rolling(n).sum() / TR.rolling(n).sum()
        # DIp = DMIp.rolling(n).sum() / abs(close - close.shift(n))
        # DIn = DMIn.rolling(n).sum() / abs(close - close.shift(n))
        DX = abs(DIp - DIn) / (DIp + DIn) * 100
        mkt_data['DMIp'] = DMIp
        mkt_data['DMIn'] = DMIn
        mkt_data['DIp'] = DIp
        mkt_data['DIn'] = DIn
        mkt_data['DX'] = DX
        return mkt_data

    def calc_BBand(mkt_data, n=20, m=2):
        close = mkt_data['close']
        high = mkt_data['high']
        low = mkt_data['low']
        TP = (high + low + close) / 3
        MID = TP.rolling(n).mean()
        BANDUP = MID + m * TP.rolling(n).std()
        BANDDOWN = MID - m * TP.rolling(n).std()
        mkt_data['MID'] = MID
        mkt_data['BANDUP'] = BANDUP
        mkt_data['BANDDOWN'] = BANDDOWN
        return mkt_data

    def calc_DPO(mkt_data, N1=10, N2=None, N3=6):
        close = mkt_data['close']
        # DPO = ta.dpo(close, length=N1)
        if not N2:
            N2 = N1 // 2 + 1
        DPO = close - close.rolling(N1).mean().shift(N2)
        MADPO = DPO.rolling(N3).mean()
        mkt_data['DPO'] = DPO
        mkt_data['MADPO'] = MADPO
        return mkt_data

    def calc_EMV(mkt_data, n=14, m=5):
        close = mkt_data['close']
        high = mkt_data['high']
        low = mkt_data['low']
        MID = ((high + low) - (high + low).shift(1)) / 2
        BRO = high - low
        EM = MID / BRO
        EMV = EM.rolling(n).mean()
        MAEMV = EMV.rolling(m).mean()
        mkt_data['MID'] = MID
        mkt_data['BRO'] = BRO
        mkt_data['EM'] = EM
        mkt_data['EMV'] = EMV
        mkt_data['MAEMV'] = MAEMV
        return mkt_data

    def calc_signal_KDJ(data):
        K = data['K']
        signals = []
        for pre_k, k in zip(K.shift(1), K):
            signal = None
            if pre_k < KDJ01.get() and k >= KDJ01.get():  # K上穿30
                signal = 1
            elif pre_k >= KDJ01.get() and k < KDJ01.get():  # K下穿30
                signal = -1
            elif pre_k < KDJ02.get() and k >= KDJ02.get():  # K上穿70
                signal = 1
            elif pre_k >= KDJ02.get() and k < KDJ02.get():  # K下穿70
                signal = -1
            signals.append(signal)
        data['signal'] = signals
        return data

    def calc_signal_CMO(mkt_data):
        CMO = mkt_data['CMO']
        signals = []
        for cmo, cmo1 in zip(CMO, CMO):
            signal = None
            if cmo > CMO01.get():
                signal = 1
            elif cmo < CMO01.get():
                signal = -1
            signals.append(signal)
        mkt_data['signal'] = signals
        return mkt_data

    def calc_signal_ADX(mkt_data):
        DIp = mkt_data['DIp']
        DIn = mkt_data['DIn']
        signals = []
        for dip, din, pre_dip, pre_din in zip(DIp, DIn, DIp.shift(1), DIn.shift(1)):
            signal = None
            if pre_dip < pre_din and dip >= din:
                signal = 1
            elif pre_dip >= pre_din and dip < din:
                signal = -1
            signals.append(signal)
        mkt_data['signal'] = signals
        return mkt_data

    def calc_signal_BLD(mkt_data):
        BANDUP = mkt_data['BANDUP']
        BANDDOWN = mkt_data['BANDDOWN']
        close = mkt_data['close']
        signals = []
        for bup, bdown, close, pre_bup, pre_bdown, pre_close in zip(BANDUP, BANDDOWN, close,
                                                                    BANDUP.shift(1), BANDDOWN.shift(1), close.shift(1)):
            signal = None
            if pre_close < pre_bup and close >= bup:
                signal = 1
            elif pre_close >= pre_bdown and close < bdown:
                signal = -1
            signals.append(signal)
        mkt_data['signal'] = signals
        return mkt_data

    def calc_signal_DPO(mkt_data):
        DPO = mkt_data['DPO']
        MADPO = mkt_data['MADPO']
        signals = []
        for dpo, madpo in zip(DPO, MADPO):
            signal = None
            if dpo >= DPO01.get():
                signal = 1
            else:
                signal = -1
            signals.append(signal)
        mkt_data['signal'] = signals
        return mkt_data

    def calc_signal_EMV(mkt_data):
        EMV = mkt_data['EMV']
        signals = []
        for emv, pre_emv in zip(EMV, EMV.shift(1)):
            signal = None
            if emv > EMV01.get():
                signal = 1
            elif emv < EMV01.get():
                signal = -1
            signals.append(signal)
        mkt_data['signal'] = signals
        return mkt_data

    def position(data):
        data['signal_last'] = data['signal'].shift(1)
        data['position'] = data['signal'].fillna(method='ffill').shift(1).fillna(0)
        return data

    data_signal = None
    if zhibiao.get() == 'KDJ':
        data_metrics = calc_KDJ(data)
        data_signal = calc_signal_KDJ(data_metrics)
    elif zhibiao.get() == 'CMO':
        data_metrics = calc_CMO(data)
        data_signal = calc_signal_CMO(data_metrics)
    elif zhibiao.get() == 'ADX':
        data_metrics = calc_ADX(data)
        data_signal = calc_signal_ADX(data_metrics)
    elif zhibiao.get() == 'BLD':
        data_metrics = calc_BBand(data)
        data_signal = calc_signal_BLD(data_metrics)
    elif zhibiao.get() == 'DPO':
        data_metrics = calc_DPO(data)
        data_signal = calc_signal_DPO(data_metrics)
    elif zhibiao.get() == 'EMV':
        data_metrics = calc_EMV(data)
        data_signal = calc_signal_EMV(data_metrics)
    data_position = position(data_signal)

    def statistic_performance(data, r0=0.03, data_period=1440):
        position = data['position']
        hold_r = data['pct_chg'] * position
        hold_win = hold_r > 0
        hold_cumu_r = (1 + hold_r).cumprod() - 1
        drawdown = (hold_cumu_r.cummax() - hold_cumu_r) / (1 + hold_cumu_r).cummax()
        ex_hold_r = hold_r - r0 / (250 * 1440 / data_period)
        data['hold_r'] = hold_r
        data['hold_win'] = hold_win
        data['hold_cumu_r'] = hold_cumu_r
        data['drawdown'] = drawdown
        data['ex_hold_r'] = ex_hold_r
        v_hold_cumu_r = hold_cumu_r.tolist()[-1]
        v_pos_hold_times = 0
        v_pos_hold_win_times = 0
        v_pos_hold_period = 0
        global v_pos_hold_win_period
        v_pos_hold_win_period = 0
        v_neg_hold_times = 0
        v_neg_hold_win_times = 0
        v_neg_hold_period = 0
        global v_neg_hold_win_period
        v_neg_hold_win_period = 0
        for w, r, pre_pos, pos in zip(hold_win, hold_r, position.shift(1), position):
            if pre_pos != pos:
                if pre_pos == pre_pos:
                    if pre_pos > 0:
                        v_pos_hold_times += 1
                        v_pos_hold_period += tmp_hold_period
                        v_pos_hold_win_period += tmp_hold_win_period
                        if tmp_hold_r > 0:
                            v_pos_hold_win_times += 1
                    elif pre_pos < 0:
                        v_neg_hold_times += 1
                        v_neg_hold_period += tmp_hold_period
                        v_neg_hold_win_period += tmp_hold_win_period
                        if tmp_hold_r > 0:
                            v_neg_hold_win_times += 1
                tmp_hold_r = 0
                tmp_hold_period = 0
                tmp_hold_win_period = 0
            else:
                if abs(pos) > 0:
                    tmp_hold_period += 1
                    if r > 0:
                        tmp_hold_win_period += 1
                    if abs(r) > 0:
                        tmp_hold_r = (1 + tmp_hold_r) * (1 + r) - 1
        v_hold_period = (abs(position) > 0).sum()
        v_hold_win_period = (hold_r > 0).sum()
        v_max_dd = drawdown.max()
        v_annual_ret = pow(1 + v_hold_cumu_r,
                           1 / (data_period / 1440 * len(data) / 250)) - 1
        v_annual_std = ex_hold_r.std() * np.sqrt(250 * 1440 / data_period)
        v_sharpe = v_annual_ret / v_annual_std
        performance_cols = ['累计收益',
                            '多仓次数', '多仓胜率', '多仓平均持有期',
                            '空仓次数', '空仓胜率', '空仓平均持有期',
                            '日胜率', '最大回撤', '年化收益/最大回撤',
                            '年化收益', '年化标准差', '年化夏普'
                            ]
        performance_values = ['{:.2%}'.format(v_hold_cumu_r),
                              v_pos_hold_times,
                              '{:.2%}'.format(v_pos_hold_win_times / v_pos_hold_times),
                              '{:.2f}'.format(v_pos_hold_period / v_pos_hold_times),
                              v_neg_hold_times,
                              '{:.2%}'.format(v_neg_hold_win_times / v_neg_hold_times),
                              '{:.2f}'.format(v_neg_hold_period / v_neg_hold_times),
                              '{:.2%}'.format(v_hold_win_period / v_hold_period),
                              '{:.2%}'.format(v_max_dd),
                              '{:.2f}'.format(v_annual_ret / v_max_dd),
                              '{:.2%}'.format(v_annual_ret),
                              '{:.2%}'.format(v_annual_std),
                              '{:.2f}'.format(v_sharpe)
                              ]
        performance = pd.DataFrame(performance_values, index=performance_cols)
        return data, performance

    result, performance = statistic_performance(data_position)

    def percent_to_int(string):
        new_int = float(string.strip("%")) / 100
        return new_int

    show_result = Toplevel(root)
    show_result.geometry("800x500+200+200")
    show_result.title("回测结果")
    frame03 = Frame(show_result, width=400, height=200)
    frame04 = Frame(show_result, width=400, height=200)
    frame05 = Frame(show_result, width=800, height=200)
    frame03.place(x=0, rely=0.4)
    frame04.place(x=400, rely=0.4)
    frame05.place(relx=0, rely=0)
    label06 = Label(frame05, text="累计持仓收益", width=16, justify="center")
    label07 = Label(frame05, text="多仓开仓次数", width=16, justify="center")
    label08 = Label(frame05, text="多仓胜率", width=16, justify="center")
    label09 = Label(frame05, text="多仓持有盈利周期数", width=16, justify="center")
    label10 = Label(frame05, text="空仓开仓次数", width=16, justify="center")
    label11 = Label(frame05, text="空仓胜率", width=16, justify="center")
    label12 = Label(frame05, text="空仓持有盈利周期数", width=16, justify="center")
    label13 = Label(frame05, text="最大回撤", width=16, justify="center")
    label14 = Label(frame05, text="年化标准差", width=16, justify="center")
    label15 = Label(frame05, text="年化收益", width=16, justify="center")
    label16 = Label(frame05, text="夏普率", width=16, justify="center")
    label17 = Label(frame05, text="实际收益", width=16, justify="center")
    l18 = IntVar()
    l19 = IntVar()
    l20 = IntVar()
    l21 = IntVar()
    l22 = IntVar()
    l23 = IntVar()
    l24 = IntVar()
    l25 = IntVar()
    l26 = IntVar()
    l27 = IntVar()
    l28 = IntVar()
    l29 = IntVar()
    l18.set(performance[0]['累计收益'])
    l19.set(performance[0]['多仓次数'])
    l20.set(performance[0]['多仓胜率'])
    l21.set(v_pos_hold_win_period)
    l22.set(performance[0]['空仓次数'])
    l23.set(performance[0]['空仓胜率'])
    l24.set(v_neg_hold_win_period)
    l25.set(performance[0]['最大回撤'])
    l26.set(performance[0]['年化标准差'])
    l27.set(performance[0]['年化收益'])
    l28.set(performance[0]['年化夏普'])
    l29.set((1 + percent_to_int(performance[0]['累计收益'])) * money.get())
    label18 = Label(frame05, textvariable=l18, width=16, justify="center")
    label19 = Label(frame05, textvariable=l19, width=16, justify="center")
    label20 = Label(frame05, textvariable=l20, width=16, justify="center")
    label21 = Label(frame05, textvariable=l21, width=16, justify="center")
    label22 = Label(frame05, textvariable=l22, width=16, justify="center")
    label23 = Label(frame05, textvariable=l23, width=16, justify="center")
    label24 = Label(frame05, textvariable=l24, width=16, justify="center")
    label25 = Label(frame05, textvariable=l25, width=16, justify="center")
    label26 = Label(frame05, textvariable=l26, width=16, justify="center")
    label27 = Label(frame05, textvariable=l27, width=16, justify="center")
    label28 = Label(frame05, textvariable=l28, width=16, justify="center")
    label29 = Label(frame05, textvariable=l29, width=16, justify="center")
    label06.place(relx=0, rely=0)
    label07.place(relx=0, rely=0.16)
    label08.place(relx=0, rely=0.32)
    label09.place(relx=0, rely=0.48)
    label10.place(relx=0, rely=0.64)
    label11.place(relx=0, rely=0.8)
    label12.place(relx=0.5, rely=0)
    label13.place(relx=0.5, rely=0.16)
    label14.place(relx=0.5, rely=0.32)
    label15.place(relx=0.5, rely=0.48)
    label16.place(relx=0.5, rely=0.64)
    label17.place(relx=0.5, rely=0.8)
    label18.place(relx=0.25, rely=0)
    label19.place(relx=0.25, rely=0.16)
    label20.place(relx=0.25, rely=0.32)
    label21.place(relx=0.25, rely=0.48)
    label22.place(relx=0.25, rely=0.64)
    label23.place(relx=0.25, rely=0.8)
    label24.place(relx=0.75, rely=0)
    label25.place(relx=0.75, rely=0.16)
    label26.place(relx=0.75, rely=0.32)
    label27.place(relx=0.75, rely=0.48)
    label28.place(relx=0.75, rely=0.64)
    label29.place(relx=0.75, rely=0.8)
    f1 = plt.figure(figsize=(4, 2))
    plt.title(zhibiao.get() + 'Performance')
    cumu_hold_close = (result['hold_cumu_r'] + 1) * data_position['close'].tolist()[0]
    plt.plot(data_position['日期'], cumu_hold_close, color='black')
    plt.plot(data_position['日期'], data_position['close'], color='red')
    plt.legend([zhibiao.get(), code.get()])
    canvas01 = FigureCanvasTkAgg(f1, frame03)
    canvas01.draw()
    canvas01.get_tk_widget().grid(row=4, column=0)
    f2 = plt.figure(figsize=(4, 2))
    plt.title('Drawdown')
    plt.plot(data_position['日期'], -result['drawdown'], color='black')
    plt.ylim([-0.8, 0])
    canvas02 = FigureCanvasTkAgg(f2, frame04)
    canvas02.draw()
    canvas02.get_tk_widget().grid(row=4, column=0)
    os.remove("result.xlsx")
    btn04 = Button(show_result, text="结束", command=root.quit)
    btn05 = Button(show_result, text="返回", command=show_result.destroy)
    btn04.place(x=350, y=450)
    btn05.place(x=450, y=450)


btn01 = Button(root, text="开始计算", command=begin)
btn02 = Button(root, text="结束", command=root.quit)
btn01.place(x=250, y=260)
btn02.place(x=150, y=280)
root.mainloop()
