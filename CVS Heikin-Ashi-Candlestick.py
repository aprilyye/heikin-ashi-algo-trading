#!/usr/bin/env python
# coding: utf-8

# In[2]:


import numpy as np
import pandas as pd


# In[3]:


cvs_data = pd.read_csv("CVS.csv")
cvs_data.head(3)


# In[4]:


cvs_data['Open'][0]


# In[5]:


ha_close = np.zeros(len(cvs_data['Date']))
ha_open = np.zeros(len(cvs_data['Date']))
ha_high = np.zeros(len(cvs_data['Date']))
ha_low = np.zeros(len(cvs_data['Date']))

ha_upper = np.zeros(len(cvs_data['Date']))
ha_lower = np.zeros(len(cvs_data['Date']))
ha_candle = np.zeros(len(cvs_data['Date']))
indicator_dates = []


# In[6]:


for x in range(0, len(ha_close)):
    ha_close[x] = (cvs_data["Open"][x] + cvs_data["High"][x] + cvs_data["Low"][x] + cvs_data["Close"][x]) / 4
    if x == 0:
        ha_open[0] = (cvs_data["Open"][0] + cvs_data["Close"][0]) / 2
    else:
        ha_open[x] = (ha_open[x-1] + ha_close[x-1]) / 2
    ha_high[x] = max(cvs_data["High"][x], ha_open[x], ha_close[x])
    ha_low[x] = min(cvs_data["Low"][x], ha_open[x], ha_close[x])
    ha_upper[x] = ha_high[x] - max(ha_open[x], ha_close[x])
    ha_lower[x] = min(ha_open[x], ha_close[x]) - ha_low[x]
    ha_candle[x] = abs(ha_open[x] - ha_close[x])
    if ha_upper[x] > 0 and ha_lower[x] > 0:
        if ha_upper[x] > 2 * ha_candle[x] and ha_lower[x] > 2 * ha_candle[x]:
            indicator_dates.append(cvs_data["Date"][x])


# In[7]:


print(indicator_dates)


# In[8]:


import plotly.graph_objects as go
from datetime import datetime

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

dates = {}
print(indicator_dates)
for x in indicator_dates:
    dates.update(dict(x0=x, x1=x, y0=0, y1=1, xref='x', yref='paper', line_width=2))
    print(x)
    fig.update_layout(
         shapes = [dates]
    )
print(dates)
original.show()
fig.show()


# In[9]:


trimmed_cvs_data = cvs_data[cvs_data['Date'] < "2019-03-28"]
trim_cvs_data = trimmed_cvs_data[trimmed_cvs_data['Date'] > "2019-02-20"]


# In[10]:


# trim_cvs_data.head(100)


# In[11]:


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


# In[12]:


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


# In[ ]:





# In[ ]:




