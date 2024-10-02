'''
核心内容，写自己的策略
'''
from Program.Function import *

import numpy as np

def process_stop_loss_close(df, stop_loss_pct, leverage_rate):
    """
    止损函数
    :param df:
    :param stop_loss_pct: 止损比例
    :param leverage_rate: 杠杆倍数
    :return:
    """

    '''
    止损函数示例
     candle_begin_time                选币                   open               close           signal        原始信号           止损价格
    2021-04-23 04:00:00            IOST-USDT...            3.69380            3.69380            -1            -1              4.06318
    2021-04-23 05:00:00            IOST-USDT...            3.75580            3.75580            nan            nan            4.06318
    2021-04-23 06:00:00            IOST-USDT...            3.70157            3.70157            nan            nan            4.06318
    2021-04-23 07:00:00            IOST-USDT...            3.59443            3.59443            nan            nan            4.06318
    2021-04-23 08:00:00            IOST-USDT...            3.78299            3.78299            nan            nan            4.06318
    2021-04-23 09:00:00            IOST-USDT...            3.73637            3.73637            -1            -1              4.06318
    2021-04-23 10:00:00            IOST-USDT...            3.92761            3.92761            nan            nan            4.06318
    2021-04-23 11:00:00            IOST-USDT...            4.02816            4.02816            nan            nan            4.06318
    2021-04-23 12:00:00            IOST-USDT...            3.85746            3.85746            nan            nan            4.06318
    2021-04-23 13:00:00            IOST-USDT...            3.84017            3.84017            nan            nan            4.06318
    2021-04-23 14:00:00            IOST-USDT...            3.94633            3.94633            nan            nan            4.06318
    2021-04-23 15:00:00            IOST-USDT...            3.96164            3.96164            nan            nan            4.06318
    2021-04-23 16:00:00            IOST-USDT...            3.95144            3.95144            nan            nan            4.06318
    2021-04-23 17:00:00            IOST-USDT...            3.91294            3.91294            nan            nan            4.06318
    2021-04-23 18:00:00            IOST-USDT...            4.02094            4.02094            nan            nan            4.06318
    2021-04-23 19:00:00            IOST-USDT...            4.04794            4.04794            nan            nan            4.06318
    2021-04-23 20:00:00            IOST-USDT...            3.99289            3.99289            nan            nan            4.06318
    2021-04-23 21:00:00            IOST-USDT...            3.96215            3.96215            nan            nan            4.06318
    2021-04-23 22:00:00            IOST-USDT...            4.01350            4.01350            nan            nan            4.06318
    2021-04-23 23:00:00            IOST-USDT...            4.14397            4.14397            0              nan            4.06318
    '''

    # ===初始化持仓方向与开仓价格
    position = 0  # 持仓方向
    open_price = np.nan  # 开仓价格

    for i in df.index:
        # 开平仓   当signal不为空的时候 并且 open_price为空 或 position与当前方向不同
        if not np.isnan(df.loc[i, 'signal']) and (np.isnan(open_price) or position != int(df.loc[i, 'signal'])):
            position = int(df.loc[i, 'signal'])
            if df.loc[i, 'signal']:  # 开仓
                # 获取开仓的价格，为了符合实盘，所以获取下一周期的开盘价
                open_price = df.loc[i + 1, 'open'] if i < df.shape[0] - 1 else df.loc[i, 'close']
            else:  # 平仓，因为在python中非0即真，所以这里直接写else即代表0
                open_price = np.nan
        # 持仓
        if position:  # 判断当天是否有持仓方向，即是否为非0的值
            # 计算止损的价格   开仓价格 * (1 - 持仓方向 * 止损比例 / 杠杆倍数)
            stop_loss_price = open_price * (1 - position * stop_loss_pct / leverage_rate)
            # 止损条件等于 持仓方向 * (收盘价 - 止损价格) <= 0
            stop_loss_condition = position * (df.loc[i, 'close'] - stop_loss_price) <= 0  # 止损条件
            df.at[i, 'stop_loss_condition'] = stop_loss_price
            # 如果满足止损条件，并且当前的信号为空时将signal设置为0，避免覆盖其他信号
            if stop_loss_condition and np.isnan(df.loc[i, 'signal']):
                df.at[i, 'signal'] = 0
                position = 0
                open_price = np.nan

    return df

def generate_fibonacci_sequence(min_number, max_number):
    """
    生成费拨那契数列，支持小数的生成
    注意：返回的所有数据都是浮点类型(小数)的，如果需要整数需要额外处理
    :param min_number: 最小值
    :param max_number: 最大值
    :return:
    """
    sequence = []
    base = 1
    if min_number < 1:
        base = 10 ** len(str(min_number).split('.')[1])
    last_number = 0
    new_number = 1
    while True:
        last_number, new_number = new_number, last_number + new_number
        if new_number / base > min_number:
            sequence.append(new_number / base)
        if new_number / base > max_number:
            break
    return sequence[:-1]


# === 简单布林策略
# 策略
def signal_simple_bolling(df, para=[200, 2], proportion=1, leverage_rate=1):

    # ===== 获取策略参数
    n = int(para[0])  # 获取参数n，即para第一个元素
    m = para[1]  # 获取参数m，即para第二个元素

    # ===== 计算指标
    # 计算均线
    df['median'] = df['close'].rolling(n, min_periods=1).mean()  # 计算收盘价n个周期的均线，如果K线数据小于n就用K线的数量进行计算
    # 计算上轨、下轨道
    df['std'] = df['close'].rolling(n, min_periods=1).std(ddof=0)  # 计算收盘价n日的std，ddof代表标准差自由度
    df['upper'] = df['median'] + m * df['std']  # 计算上轨
    df['lower'] = df['median'] - m * df['std']  # 计算下轨

    # ===== 找出交易信号
    # === 找出做多信号
    condition1 = df['close'] > df['upper']  # 当前K线的收盘价 > 上轨
    condition2 = df['close'].shift(1) <= df['upper'].shift(1)  # 之前K线的收盘价 <= 上轨
    df.loc[condition1 & condition2, 'signal_long'] = 1  # 将产生做多信号的那根K线的signal设置为1，1代表做多

    # === 找出做多平仓信号
    condition1 = df['close'] < df['median']  # 当前K线的收盘价 < 中轨
    condition2 = df['close'].shift(1) >= df['median'].shift(1)  # 之前K线的收盘价 >= 中轨
    df.loc[condition1 & condition2, 'signal_long'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # === 找出做空信号
    condition1 = df['close'] < df['lower']  # 当前K线的收盘价 < 下轨
    condition2 = df['close'].shift(1) >= df['lower'].shift(1)  # 之前K线的收盘价 >= 下轨
    df.loc[condition1 & condition2, 'signal_short'] = -1  # 将产生做空信号的那根K线的signal设置为-1，-1代表做空

    # === 找出做空平仓信号
    condition1 = df['close'] > df['median']  # 当前K线的收盘价 > 中轨
    condition2 = df['close'].shift(1) <= df['median'].shift(1)  # 之前K线的收盘价 <= 中轨
    df.loc[condition1 & condition2, 'signal_short'] = 0  # 将产生平仓信号当天的signal设置为0，0代表平仓

    # ===== 合并做多做空信号，去除重复信号
    # === 合并做多做空信号
    df['signal'] = df[['signal_long', 'signal_short']].sum(axis=1, min_count=1,
                                                           skipna=True)  # 合并多空信号，即signal_long与signal_short相加，得到真实的交易信号
    # === 去除重复信号
    temp = df[df['signal'].notnull()][['signal']]  # 筛选siganla不为空的数据，并另存一个变量
    temp = temp[temp['signal'] != temp['signal'].shift(1)]  # 筛选出当前周期与上个周期持仓信号不一致的，即去除重复信号
    df['signal'] = temp['signal']  # 将处理后的signal覆盖到原始数据的signal列

    # ===== 删除无关变量
    df.drop(['std', 'signal_long', 'signal_short'], axis=1, inplace=True)  # 删除std、signal_long、signal_short列

    # ===== 止盈止损
    # 校验当前的交易是否需要进行止盈止损
    df = process_stop_loss_close(df, proportion, leverage_rate=leverage_rate)  # 调用函数，判断是否需要止盈止损，df需包含signal列

    return df


# 策略参数组合
def signal_simple_bolling_para_list(m_list=range(20, 1000 + 20, 20),
                                    n_list=[i / 10 for i in list(np.arange(3, 50 + 2, 2))]):
    # ==== 输出一下参数的范围
    # print('参数遍历范围：')
    # print('m_list', list(m_list))  # 输出m的遍历范围
    # print('n_list', list(n_list))  # 输出n的遍历范围

    # ===== 构建遍历的列表
    para_list = []  # 定义一个新的列表，用于存储遍历参数

    # === 遍历参数
    for m in m_list:  # 遍历m的参数
        for n in n_list:  # 遍历n的参数
            para = [m, n]  # 构建每个遍历列表的每个参数
            para_list.append(para)  # 将参数累加到para_list
    # ===== 返回参数列表
    return para_list



