import tushare as ts
import pandas as pd
import matplotlib.pyplot as plt
from ta.trend import SMAIndicator
from ta.momentum import RSIIndicator

# 替换为你的 tushare pro token
ts.set_token('5bc934e2264456cc3bd060bea06deda0fb5ab56e1c5b7216e4a9ffc2')
pro = ts.pro_api()

# 获取万科的股票信息
stock_code = '601012.SH'  # 万科股票代码
start_date = '20231001'
end_date = '20231231'

df = pro.daily(ts_code=stock_code, start_date=start_date, end_date=end_date)
df['trade_date'] = pd.to_datetime(df['trade_date'])
df.set_index('trade_date', inplace=True)

# 计算短期和长期移动平均线
short_window = 1
long_window = 7

df['Short_MA'] = df['close'].rolling(window=short_window, min_periods=1).mean()
df['Long_MA'] = df['close'].rolling(window=long_window, min_periods=1).mean()

# 计算相对强度指标（RSI）
rsi_window = 1
df['RSI'] = RSIIndicator(df['close'], window=rsi_window).rsi()

# 策略：当短期均线上穿长期均线并且 RSI 大于某个阈值时买入，反之卖出
buy_signal = (df['Short_MA'] > df['Long_MA']) & (df['RSI'] < 30)
sell_signal = (df['Short_MA'] < df['Long_MA']) & (df['RSI'] > 70)

# 绘制股价图和买卖点
plt.figure(figsize=(12, 6))
plt.plot(df['close'], label='Close Price', alpha=0.5)
plt.plot(df['Short_MA'], label=f'Short {short_window} days MA')
plt.plot(df['Long_MA'], label=f'Long {long_window} days MA')
plt.scatter(df.index[buy_signal], df['close'][buy_signal], marker='^', color='g', label='Buy Signal')
plt.scatter(df.index[sell_signal], df['close'][sell_signal], marker='v', color='r', label='Sell Signal')

# 在图上标记买卖点的日期
for date, price in zip(df.index[buy_signal].date, df['close'][buy_signal]):
    plt.annotate(f'Buy\n{date}\n{price:.2f}', (date, price), textcoords="offset points", xytext=(0, 10), ha='center', fontsize=8, color='g')

for date, price in zip(df.index[sell_signal].date, df['close'][sell_signal]):
    plt.annotate(f'Sell\n{date}\n{price:.2f}', (date, price), textcoords="offset points", xytext=(0, -15), ha='center', fontsize=8, color='r')

plt.title('Stock Price and Trading Signals')
plt.xlabel('Date')
plt.ylabel('Close Price')
plt.legend()
plt.show()
