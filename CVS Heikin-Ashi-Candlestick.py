#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd


# In[2]:


cvs_data = pd.read_csv("CVS.csv")
cvs_data.head(3)


# In[3]:


cvs_data['Open'][0]


# In[4]:


ha_close = np.zeros(len(cvs_data['Date']))
ha_open = np.zeros(len(cvs_data['Date']))
ha_high = np.zeros(len(cvs_data['Date']))
ha_low = np.zeros(len(cvs_data['Date']))


# In[5]:


for x in range(0, len(ha_close)):
    ha_close[x] = (cvs_data["Open"][x] + cvs_data["High"][x] + cvs_data["Low"][x] + cvs_data["Close"][x]) / 4
    if x == 0:
        ha_open[0] = (cvs_data["Open"][0] + cvs_data["Close"][0]) / 2
    else:
        ha_open[x] = (ha_open[x-1] + ha_close[x-1]) / 2
    ha_high[x] = max(cvs_data["High"][x], ha_open[x], ha_close[x])
    ha_low[x] = min(cvs_data["Low"][x], ha_open[x], ha_close[x])


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

original.show()
fig.show()


# In[ ]:




