import numpy as np
import pandas as pd
from pandas_datareader import data as wb
from openpyxl import Workbook
import matplotlib.pyplot as plt

####        READ.ME         ####
# CHANGE EXCEL PATH ON LINE 148 & 20
# excel te gebruiken voor ander optimaal punt op de Markowitz Graph

############################        INPUT           ############################

### Geef bij tickers de symbols van alle stock in het portfolio (te vinden op Yahoo Finance)
assets = ["SPY", "AAPL","MSFT"]
#left IITU.L out
### Geef aantal simulaties voor Weights
simulations = 20000

################################################################################

mydata = pd.DataFrame()
for a in assets:
    mydata[a] = wb.DataReader(a, data_source='yahoo', start='2015-7-1')['Adj Close']

# mydata.to_excel('/Users/andres/Documents/Beleggen/Stock_Data2.xlsx',sheet_name= 'Stocks')
# print(mydata.info())
# print(mydata.head())
# print(mydata.tail())

# Growth since 2014-4-1
(mydata / mydata.iloc[0] * 100).plot(figsize = (15, 6));
plt.xlabel('Time')
plt.ylabel('Growth (Index 100 = 2014-4-1)')
plt.title('Simple Growth')
plt.legend(loc = 2)
plt.show()
print('Growth plot printed')

### Stock Prices since 2014-4-1
# mystocks = pd.DataFrame()
# for a in assets:
#     mystocks[a] = wb.DataReader(a, data_source='yahoo', start='2014-4-1')['Close']
# mystocks.info()
# mystocks.head()
# mystocks.tail()
#
# mystocks.plot(figsize=(15, 6))
# plt.xlabel('Time')
# plt.ylabel('StockPrices')
# #plt.show()
# print('Stock Price Plot printed')

#### Daily Returns
print("Daily Returns: \n")

print('Simple Return')
returns = mydata/mydata.shift(1) - 1
print(returns.tail())

print('\n Log Return')
log_returns = np.log(mydata/mydata.shift(1))
print(log_returns.tail())
print("\n")

### Annual Returns
print("Annual Returns: \n")

print('Simple Annual Return')
annual_returns = returns.mean() * 250
print(str(annual_returns*100) + '%')

print('\n Log Annual Return')
annual_log_returns = log_returns.mean() * 250
print(str(annual_log_returns*100) + '%')
print("\n")

### Covariance, Correlation & Number of Assets
# print("Covariance, Correlation & Number of Assets: \n")
covariance = log_returns.cov() * 250
# print('Covariance :\n' + str(covariance) + '\n')
correlation = log_returns.corr()
# print('Correlation :\n ' + str(correlation) + '\n')
num_assets = len(assets)
# print('Number of Assets: ' + str(num_assets))

# ## Test Weights
# weights = np.random.random(num_assets)
# weights /= np.sum(weights)
# weights
# for w in weights:
#     print(w)
# print(sum(weights))
#
# print('\nExpected Portfolio Return: ')
# expected_return = np.sum(weights * returns.mean()) * 250
# print(expected_return)
# print('\nExpected Portfolio Variance: ')
# expected_variance = np.dot(weights.T, np.dot(returns.cov() * 250, weights))
# print(expected_variance)
# print('\nExpected Portfolio Volatility: ')
# expected_volatility = np.sqrt(expected_variance)
# print(expected_volatility)

### 1000 weights simmulations (return and volatility)
pfolio_returns = []
pfolio_volatilities = []
pfolio_weights = []

for x in range (simulations):
    weights = np.random.random(num_assets)
    weights /= np.sum(weights)
    pfolio_returns.append(np.sum(weights * log_returns.mean()) * 250)
    pfolio_volatilities.append(np.sqrt(np.dot(weights.T,np.dot(log_returns.cov() * 250, weights))))
    pfolio_weights.append(weights)


pfolio_returns = np.array(np.round(pfolio_returns,3))
pfolio_volatilities = np.array(np.round(pfolio_volatilities,3))
pfolio_weights = np.array(pfolio_weights)


### Create DataFrame of weights

weights_df = pd.DataFrame(data=pfolio_weights)
sum_weights = weights_df.sum(axis = 1)
print(sum_weights)
weights_df['Sum'] = sum_weights
print('\n DataFrame of Weights')

## Rename Columns
index = 0
for a in assets:
    weights_df.rename(columns={index: a}, inplace= True)
    index += 1
weights_df.info()
print(weights_df.head())


### Dataframe with all resp. returns and volatility
print('\n All portfolios with different weights:')
portfolios = pd.DataFrame({'Return': pfolio_returns, 'Volatility': pfolio_volatilities, 'Weights': range(simulations)})
print(portfolios.head() ,'\n', portfolios.tail())
portfolios.plot(x='Volatility', y='Return', kind='scatter', figsize=(10, 6));
plt.xlabel('Expected Volatility')
plt.ylabel('Expected Return')
plt.title('Return - Volatility')
plt.show()
#print("Plot printed")

### Sort the portpolios by lowest volatility and highest expected return
print('\n Portfolios sorted by Volatility & Return')
portfolios_sorted = portfolios.sort_values(by=['Volatility','Return'], ascending= [1,0])
print('Info: \n', portfolios_sorted.info)
print('Head: \n',portfolios_sorted.head)
print('Tail: \n',portfolios_sorted.tail)


### Get optimal weights for minimal risk
index_weights = portfolios_sorted['Weights'].iloc[0]
weights_df = weights_df.drop('Sum', axis = 1)
print(index_weights)
print('--->     Minimum Risk Fractions:')
print(weights_df.loc[[index_weights]]*100)
print('\n',' --->     With resp. Return:')
print(str(round(float(np.dot(weights_df.loc[[index_weights]],annual_log_returns)*100),6)) + ' %')
print(type(float(np.dot(weights_df.loc[[index_weights]],annual_log_returns)*100)))
print('\n','\n','See Excel for higher Returns')

#plt.show()
print("Plot printed")

## Extract optimal weights for total portfolios
optimal_weights = pd.DataFrame()
x = portfolios_sorted['Volatility'].min()
while x < portfolios_sorted['Volatility'].max():
    loop_df = portfolios_sorted.loc[portfolios_sorted['Volatility'] == x]
    # print('All with same volatility: \n',loop_df)
    max = loop_df['Return'].max()
    # print('Max return for this Volatility: ', x, '\n',max)
    #print(loop_df.loc[loop_df['Return'] == max])
    optimal_weights = optimal_weights.append(loop_df.loc[loop_df['Return'] == max])
    x = np.round(x + 0.001, 3)

# print(optimal_weights)
optimal_weights.plot(x='Volatility', y='Return', kind='scatter', figsize=(10, 6));
plt.title('Highest Returns for Volatility')
plt.show()

## Get optimal weights:

### Write to Excel
writer = pd.ExcelWriter('/Users/andres/Documents/Beleggen/Markowitz_Optimalization2.xlsx', engine='xlsxwriter')
portfolios_sorted.to_excel(writer, sheet_name='Returns')
optimal_weights.to_excel(writer, sheet_name='Optimal Returns')
weights_df.to_excel(writer, sheet_name='Weights')
# weights_spread.to_excel(writer, sheet_name='Opitmal Weights Spread')
annual_log_returns.to_excel(writer, sheet_name= 'Average Returns')
covariance.to_excel(writer, sheet_name= 'Covariance')
correlation.to_excel(writer, sheet_name= 'Correlation')
writer.save()
print('Written to Excel \n')