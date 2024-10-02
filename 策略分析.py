import quantstats as qs
import pandas as pd


df = pd.read_csv(r'')
df['candle_begin_time'] = pd.to_datetime(df['candle_begin_time'])  # 确保 'Time' 列是 datetime 类型
df.set_index('candle_begin_time', inplace=True)  # 将 'Time' 列设置为索引

# 提取收益率 Series
returns = df['r_line_equity_curve']

# 生成HTML报告
qs.reports.html(returns, output='strategy_analysis.html')

# 打印基本统计信息
qs.reports.basic(returns)

# 绘制图表
qs.plots.drawdown(returns)
qs.plots.cumulative_returns(returns)
qs.plots.monthly_returns_heatmap(returns)

# 打印详细统计信息
print(qs.stats(returns))
