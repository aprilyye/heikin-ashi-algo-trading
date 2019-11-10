import numpy as np
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

class Heikin_Automation:

    def __init__(self):
        self.stock_data = []
        self.indicator_dates = []
        self.indicator_nums = []

        self.ha_close = []
        self.ha_open = []
        self.ha_high = []
        self.ha_low = []

        self.ha_upper = []
        self.ha_lower = []
        self.ha_candle = []

    def automation(self, stock_file):
        # stock_file is str type
        self.stock_data = pd.read_csv(stock_file)
        # FOR PRINTING VISUALIZATION
        # stock_data.tail(3)

        self.ha_close = np.zeros(len(stock_data['Date']))
        self.ha_open = np.zeros(len(stock_data['Date']))
        self.ha_high = np.zeros(len(stock_data['Date']))
        self.ha_low = np.zeros(len(stock_data['Date']))

        self.ha_upper = np.zeros(len(stock_data['Date']))
        self.ha_lower = np.zeros(len(stock_data['Date']))
        self.ha_candle = np.zeros(len(stock_data['Date']))

    def heikin_setup(self):
        for x in range(0, len(self.ha_close)):
            self.ha_close[x] = (self.stock_data["Open"][x] + self.stock_data["High"][x] + self.stock_data["Low"][x] + self.stock_data["Close"][x]) / 4
            if x == 0:
                self.ha_open[0] = (self.stock_data["Open"][0] + self.stock_data["Close"][0]) / 2
            else:
                self.ha_open[x] = (self.ha_open[x-1] + self.ha_close[x-1]) / 2
            self.ha_high[x] = max(self.stock_data["High"][x], self.ha_open[x], self.ha_close[x])
            self.ha_low[x] = min(self.stock_data["Low"][x], self.ha_open[x], self.ha_close[x])
            self.ha_upper[x] = self.ha_high[x] - max(self.ha_open[x], self.ha_close[x])
            self.ha_lower[x] = min(self.ha_open[x], self.ha_close[x]) - self.ha_low[x]
            self.ha_candle[x] = abs(self.ha_open[x] - self.ha_close[x])
            if self.ha_upper[x] > 0 and self.ha_lower[x] > 0:
                if self.ha_upper[x] > 3 * self.ha_candle[x] and self.ha_lower[x] > 3 * self.ha_candle[x]:
                    self.indicator_dates.append(self.stock_data["Date"][x])
                    self.indicator_nums.append(x)

        print(self.indicator_dates)
        print(self.indicator_nums)

# converted up to here

original = go.Figure(data=[go.Candlestick(x=cvs_data['Date'],
                open=cvs_data['Open'],
                high=cvs_data['High'],
                low=cvs_data['Low'],
                close=cvs_data['Close'])])

fig = go.Figure(data=[go.Candlestick(x=cvs_data['Date'],
                open=ha_open,
                high=ha_high,
                low=ha_low,
                close=ha_close)])
fig.update_layout(
    shapes = [dict(
        x0=date, x1=date, y0=0, y1=1, xref='x', yref='paper',
        line=dict(
                color="MediumPurple",
                width=1,
                dash="dashdot",
            )) for date in indicator_dates]
)
original.show()
fig.show()


# In[8]:


trimmed_cvs_data = cvs_data[cvs_data['Date'] < "2019-03-28"]
trim_cvs_data = trimmed_cvs_data[trimmed_cvs_data['Date'] > "2019-02-20"]


# In[9]:


# trim_cvs_data.head(100)


# In[10]:


# ha_close_trim = np.zeros(len(trim_cvs_data['Date']))
# ha_open_trim = np.zeros(len(trim_cvs_data['Date']))
# ha_high_trim = np.zeros(len(trim_cvs_data['Date']))
# ha_low_trim = np.zeros(len(trim_cvs_data['Date']))
#print(ha_close)
trim_ha_close = ha_close[97:122]
trim_ha_open = ha_open[97:122]
trim_ha_high = ha_high[97:122]
trim_ha_low = ha_low[97:122]

print(trim_ha_open)


# In[11]:


trim_fig = go.Figure(data=[go.Candlestick(x=trim_cvs_data['Date'],
                open=trim_ha_open,
                high=trim_ha_high,
                low=trim_ha_low,
                close=trim_ha_close)])
trim_fig.update_layout(
#     title='The Great Recession',
#     yaxis_title='AAPL Stock',
     shapes = [dict(
         x0='2019-03-11', x1='2019-03-11', y0=0, y1=1, xref='x', yref='paper',
         line_width=2)],
#     annotations=[dict(
#         x='2019-03-11', y=0.05, xref='x', yref='paper',
#         showarrow=False, xanchor='left', text='Increase Period Begins')]
)

trim_fig.show()


# In[12]:


# calculating bearish engulfing pattern

bearish_dates = []
bullish_dates = []
green_cnt = 0
red_cnt = 0

for x in range(10, len(cvs_data['Date'])):
    # if we see a red and green count >= 3, check if engulfing or not
    # else, increment green
    # vice versa for bullish
    cur_close = cvs_data['Close'][x]
    cur_open = cvs_data['Open'][x]

    if (cur_close < cur_open) and green_cnt >= 3:
        prev_close = cvs_data['Close'][x-1]
        prev_open = cvs_data['Open'][x-1]

        if abs(cur_close - cur_open) > abs(prev_close - prev_open):
            bearish_dates.append(cvs_data['Date'][x])
            green_cnt = 0
        else:
            # not engulfing
            green_cnt = 0
    elif (cur_close < cur_open):
        green_cnt = 0
    else:
        green_cnt += 1

    if (cur_open < cur_close) and red_cnt >= 3:
        prev_close = cvs_data['Close'][x-1]
        prev_open = cvs_data['Open'][x-1]

        if abs(cur_close - cur_open) > abs(prev_close - prev_open):
            bullish_dates.append(cvs_data['Date'][x])
            red_cnt = 0
        else:
            # not engulfing
            red_cnt = 0
    elif (cur_close > cur_open):
        red_cnt = 0
    else:
        red_cnt += 1

print(bearish_dates)
print(bullish_dates)


# In[13]:


bear = go.Figure(data=[go.Candlestick(x=cvs_data['Date'],
                open=cvs_data['Open'],
                high=cvs_data['High'],
                low=cvs_data['Low'],
                close=cvs_data['Close'])])

bear.update_layout(
    shapes = [dict(
        x0=date, x1=date, y0=0, y1=1, xref='x', yref='paper',
        line_width=2, fillcolor = 'violet') for date in bearish_dates]
)
bear.show()


# In[14]:


bull = go.Figure(data=[go.Candlestick(x=cvs_data['Date'],
                open=cvs_data['Open'],
                high=cvs_data['High'],
                low=cvs_data['Low'],
                close=cvs_data['Close'])])

bull.update_layout(
    shapes = [dict(
        x0=date, x1=date, y0=0, y1=1, xref='x', yref='paper',
        line_width=2, fillcolor = 'violet') for date in bullish_dates]
)
bull.show()


# In[15]:


combined_bull = []
combined_bear = []
for date in indicator_dates:
    if date in bullish_dates:
        combined_bull.append(date)
    if date in bearish_dates:
        combined_bear.append(date)
print(combined_bull)
print(combined_bear)


# In[60]:


current_balance = 1000.0
owned = 0
for nums in indicator_nums:
    flagPos = True
    flagNeg = True
    for check in range(nums-1, nums-3, -1):
        if ha_close[check] < ha_open[check]:
            flagPos = False
    for check in range(nums-1, nums-3, -1):
        if ha_close[check] > ha_open[check]:
            flagNeg = False
    if flagNeg == True:
        print("Buying on: " + cvs_data['Date'][nums])
        owned += 1
        current_balance -= ha_open[check+1]
    if flagPos == True and owned != 0:
        print("Selling on: " + cvs_data['Date'][nums])
        current_balance += ha_open[check+1] * owned
        owned = 0
print(current_balance)
print(owned * ha_close[249])
print("Total worth: " + str(current_balance + owned * ha_close[249]))


# In[ ]:
