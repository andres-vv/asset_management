import numpy as np
import pandas as pd
from pandas_datareader import data as wb
from openpyxl import Workbook
import matplotlib.pyplot as plt

# Geef bij tickers de tickers van alle stock in het portfolio (te vinden op Yahoo Finance)
tickers = ['ABI.BR', 'VGP.BR', 'KBCA.BR']
start_date = '2019-9-1'


mydata = pd.DataFrame()
for t in tickers:
    mydata[t] = wb.DataReader(t, data_source='yahoo', start=start_date)['Adj Close']

(mydata / mydata.iloc[0] * 100).plot(figsize = (15, 6));
plt.title('Growth')
plt.xlabel('Time')
plt.ylabel('Growth (2019-9-1 = 100)')
plt.show()

mydata.plot(figsize = (15, 6))
plt.title('Stock Prices')
plt.xlabel('Time')
plt.ylabel('Stock Price')
plt.show()
