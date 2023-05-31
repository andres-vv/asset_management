import numpy as np
import pandas as pd
from pandas_datareader import data as wb
from scipy.optimize import Bounds
from scipy.optimize import minimize
from scipy.optimize import LinearConstraint


### Geef aandelen in
assets = ["BTC-USD", "ETH-USD"]

### r = risk aversion (r = 1: minimize variance, r = 0: maximize return)
r = 1









mydata = pd.DataFrame()
for a in assets:
    mydata[a] = wb.DataReader(a, data_source='yahoo', start='2018-7-1')['Adj Close']
print(mydata.head())
print(mydata.isna().sum())
mydata.fillna(method='ffill')
print(mydata.info())
print(mydata.head)


returns = mydata/mydata.shift(1) - 1
log_returns = np.log(mydata/mydata.shift(1))

#simple annual Return
annual_returns = returns.mean() * 250

#log annual Returns
annual_log_returns = log_returns.mean() * 250

#covariances
covariance = log_returns.cov() * 250

#defining objective function:
def objective_simple(x):
    annual_returns = returns.mean() * 250

    return -1*(r*(np.dot(annual_returns,x)) + (1-r)*(np.sqrt(np.dot(x.T,np.dot(log_returns.cov() * 250, x)))))

#defining bounds
lowerbound = []
upperbound = []
for i in range(len(assets)):
    lowerbound.append(0)
    upperbound.append(np.inf)
bounds = Bounds(lowerbound,upperbound)

#defining constraints
coefficients = []
for i in range(len(assets)):
    coefficients.append(1)

linear_constraint = LinearConstraint([coefficients],1,1)

#optimalization
x0 = []
startvalue = 1/len(assets)
for i in range(len(assets)):
    x0.append(startvalue)

result = minimize(objective_simple, x0, method='trust-constr',
            constraints=linear_constraint, bounds=bounds)
print('RETURNS:')
for r in annual_log_returns:
    print(np.round(r*100,2),'%')
print('RISK:')
print('PORTFOLIO RISK:')
print(np.round(np.sqrt(np.dot(result.x.T,np.dot(log_returns.cov() * 250, result.x)))*100,2),'%')
print('WEIGHTS:')
for w in result.x:
    print(np.round(w*100,2), '%')
print('SUM: ')
print(np.sum(result.x))
