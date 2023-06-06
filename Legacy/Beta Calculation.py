import numpy as np
import pandas as pd
from pandas_datareader import data as wb

#### GEEF ARRAY VAN STOCKS WAARVAN JE BETA WILT WETEN
stocks = ['GLPG.AS']

#### GEEF INDEX VAN MARKT WAARMEE JE WILT VERGELIJKEN (BV: BEL20)
market = '^AEX'
''
###  CALCULATIONS
stocks.append(market)
print(stocks)

data = pd.DataFrame()
for t in stocks:
    data[t] = wb.DataReader(t, data_source='yahoo', start='2015-1-1')['Adj Close']

sec_returns = np.log( data / data.shift(1) )
cov = sec_returns.cov() * 250
# print(cov)

index = 0
covariances = []

while(index < len(stocks) - 1):
    covariances.append(cov.iloc[index, len(stocks) - 1])
    index = index + 1

# print(covariances)

market_variance = sec_returns[market].var() * 250

beta = covariances / market_variance
stocks.remove(market)
betas = pd.DataFrame(columns = list(stocks))
betas.loc[0] = beta
print(betas)

