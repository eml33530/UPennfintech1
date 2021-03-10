#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import datetime as dt
from pathlib import Path

get_ipython().run_line_magic('matplotlib', 'inline')


# In[35]:


# set the path
algo_rts=Path('algo_returns.csv')
sp500_history=Path('sp500_history.csv')
whale_returns=Path('whale_returns.csv')

# Read the CSVs and set the `date` column as a datetime index to the DataFrame

algo_rts_df = pd.read_csv(algo_rts, index_col="Date", infer_datetime_format=True, parse_dates=True)
sp500_history_df = pd.read_csv(sp500_history, index_col="Date", infer_datetime_format=True, parse_dates=True)
whale_returns_df = pd.read_csv(whale_returns, index_col="Date", infer_datetime_format=True, parse_dates=True)

#sort data

algo_rts_df=algo_rts_df.sort_index()
sp500_history_df=sp500_history_df.sort_index()
whale_returns_df=whale_returns_df.sort_index()

# Display a few rows

whale_returns_df.head()


# In[36]:


# count the nulls - Whale returns

whale_returns_df.isnull().sum()


# In[37]:


# drop nulls - whale returns

whale_returns_df = whale_returns_df.dropna()


# In[38]:


# double check the nulls are dropped

whale_returns_df.isnull().sum()


# In[39]:


# count nulls for algo returns

algo_rts_df.isnull().sum()


# In[40]:


# drop the nulls for algo returns

algo_rts_df=algo_rts_df.dropna()


# In[41]:


# double check the nulls are dropped
algo_rts_df.isnull().sum()


# In[42]:


# check the data types

sp500_history_df.dtypes


# In[43]:


# fix the data type to float

sp500_history_df['Close']=sp500_history_df['Close'].str.replace('$', '')
sp500_history_df['Close']=sp500_history_df['Close'].str.replace(',', '')
sp500_history_df['Close'] = sp500_history_df['Close'].astype(float)
sp500_history_df.head()


# In[44]:


# double check you changed the datatype for Close to float

sp500_history_df.dtypes


# In[45]:


# calculate daily returns for sp500

daily_rts_sp500=sp500_history_df.pct_change()
daily_rts_sp500.head()


# In[46]:


# check for null values in sp500

daily_rts_sp500.isnull().sum()


# In[47]:


#drop nulls in sp500 daily returns
daily_rts_sp500=daily_rts_sp500.dropna()


# In[48]:


#double check those nulls are dropped in daily returns - sp500
daily_rts_sp500.isnull().sum()


# In[50]:


# change 'close' column to be 'SP500'

daily_rts_sp500=daily_rts_sp500.rename(columns={'Close':'SP500'})
daily_rts_sp500.head()


# In[51]:


# Combine all data into one

combined_df=pd.concat([whale_returns_df,algo_rts_df,daily_rts_sp500], axis=1, join='inner')
combined_df.head()


# In[ ]:


### Performance Analysis


# In[54]:


# Plot daily returns of all portfolios

combined_df.plot(figsize=(20,10),title='Performance Analysis')


# In[55]:


# Calculate cumulative returns of all portfolios

cumulative_rts=(1+combined_df).cumprod()
cumulative_rts.head()


# In[56]:


# Plot cumulative returns

cumulative_rts.plot(figsize=(20,10),title='Cumulative Returns')


# In[ ]:


### Risk Analysis


# In[61]:


# create a box plot for each portfolio

combined_df.plot.box(figsize=(20,10),title='Risk Analysis')


# In[63]:


# calculate the standard dev of all portfolios

std=combined_df.std()
std


# In[66]:


# Determine which portfolios are riskier than the S&P 500

## As you can see below Tiger Global and Berkshire are risker than the SP500

std_sp500=combined_df['SP500'].std()

std>std_sp500


# In[67]:


# Calculate the Annualized Standard Deviation

annualized_std=std*np.sqrt(252)
annualized_std


# In[ ]:


### Rolling Stats


# In[98]:


# Calculate the rolling standard deviation for all portfolios using a 21-day window
   
rolling_std=combined_df.rolling(window=21).std()
rolling_std


# In[72]:


# Plot the rolling standard deviation

rolling_std.plot(figsize=(20,10),title='21-DAY SMA')


# In[76]:


# Calculate the correlation

import seaborn as sn

correlation=combined_df.corr()
correlation


# In[174]:


# Display de correlation matrix

sn.heatmap(correlation, annot=True)


# In[102]:


# Calculate covariance of a single portfolio

covariance=combined_df['SOROS FUND MANAGEMENT LLC'].cov(combined_df['SP500'])
covariance


# In[103]:


# Calculate variance of S&P 500

variance=combined_df['SP500'].var()
variance


# In[104]:


# Computing beta

soros_beta=covariance/variance
soros_beta


# In[159]:


# Calculate rolling Cov and VAR for plotting beta

rolling_covariance=combined_df['SOROS FUND MANAGEMENT LLC'].rolling(window=21).cov(combined_df['SP500'])
rolling_variance=combined_df['SP500'].rolling(window=21).var()

# Plot rolling Beta

rolling_beta=rolling_covariance/rolling_variance
rolling_beta.plot(figsize=(20,10), title='Rolling 21-day Beat of Soros Fund Mgmt. LLC')


# In[119]:


# EWM

combined_df.ewm(halflife=21)


# In[118]:


# Use `ewm` to calculate the rolling window and plot - Try calculating the ewm with a 21-day half-life.

combined_df.ewm(halflife=21).mean().plot(figsize=(20,10))


# In[160]:


# Annualized Sharpe Ratios

sharpe_ratios=(combined_df.mean()*252)/(combined_df.std()*np.sqrt(252))
sharpe_ratios


# In[161]:


# Visualize the sharpe ratios as a bar plot

sharpe_ratios.plot(kind='bar', title='Sharpe Ratios')


# In[186]:


# Determine whether the algorithmic strategies outperform both the market (S&P 500) and the whales portfolios. print function

print('Determine wheter the algorithmic strategies outerperform both the market(SP 500) and the whales portfolios.')
print()
print('The algo 1 portfolio performed better than the SP500, but had a higher risk premium where algo 2 performed slightly under the SP500 it had a much lower risk premium.')


# In[ ]:





# In[ ]:





# In[ ]:


### Create Custom Portfolio


# In[139]:


# set the path
aapl_historical=Path('aapl_historical.csv')
cost_historical=Path('cost_historical.csv')
goog_historical=Path('goog_historical.csv')

# Read the CSVs and set the `date` column as a datetime index to the DataFrame

aapl_df = pd.read_csv(aapl_historical, index_col="Trade DATE", infer_datetime_format=True, parse_dates=True)
cost_df = pd.read_csv(cost_historical, index_col="Trade DATE", infer_datetime_format=True, parse_dates=True)
goog_df = pd.read_csv(goog_historical, index_col="Trade DATE", infer_datetime_format=True, parse_dates=True)

#sort data

aapl_df=aapl_df.sort_index()
cost_df=cost_df.sort_index()
goog_df=goog_df.sort_index()

# Display a few rows

goog_df.head()


# In[140]:


# Drop symbol column

aapl_df=aapl_df.drop('Symbol', axis=1)
cost_df=cost_df.drop('Symbol', axis=1)
goog_df=goog_df.drop('Symbol', axis=1)
aapl_df.head()


# In[142]:


#combine all three files and reset the index

#Reorganize portfolio data by having a column per symbol

stocks_combined_df=pd.concat([aapl_df,cost_df,goog_df], axis=1, join='inner')
stocks_combined_df.reset_index()
stocks_combined_df.columns=['AAPL','COST','GOOG']
stocks_combined_df.head()


# In[151]:


# Calculate daily returns

daily_returns2=stocks_combined_df.pct_change()
daily_returns2.head()


# In[148]:


# check for N/A

daily_returns2.isnull().sum()


# In[152]:


# drop N/a

daily_returns2=daily_returns2.dropna()


# In[154]:


# double check yourself that n/a have been dropped

daily_returns2.isnull().sum()


# In[155]:


# display a sample

daily_returns2.head()


# In[158]:


#### Calculate the weighted returns for the portfolio assuming an equal number of shares for each stock

# Set weights
# weights = [1/3, 1/3, 1/3]

aapl_weight = 1/3
cost_weight= 1/3
goog_weight= 1/3

# Calculate portfolio return
# Display sample data

portfolio_returns = aapl_weight * daily_returns2["AAPL"] +cost_weight * daily_returns2["COST"]+goog_weight * daily_returns2["GOOG"]
portfolio_returns.head()


# In[187]:


### Join your portfolio returns to the DataFrame that contains all of the portfolio returns

# Join your returns DataFrame to the original returns DataFrame
# Only compare dates where return data exists for all the stocks (drop NaNs)

stocks_combined2=pd.concat([portfolio_returns, combined_df], axis='columns', join='inner')
stocks_combined2.rename(columns={0:"Custom1"},inplace=True)
stocks_combined2.dropna(inplace=True)
stocks_combined2.sort_index()
stocks_combined2.head()


# In[188]:


### Re-run the risk analysis with your portfolio to see how it compares to the others

# Calculate the annualized `std`

stocks_combined2.std()


# In[189]:


### Calculate and plot rolling std with 21-day window

# Calculate rolling standard deviation

annualized_variance2 = (stocks_combined2.var()*252)
annualized_std2 = np.sqrt(annualized_variance2)
annualized_std2


# In[190]:


# Plot rolling standard deviation

stocks_combined2.rolling(window=21).std().plot(figsize=(20,10))


# In[191]:


### Calculate and plot the correlation

coorelation2=stocks_combined2.corr()
coorelation2


# In[192]:


# Plot new coorelation

sn.heatmap(coorelation2, vmin=-1, vmax=1)


# In[193]:


### Calculate and Plot Rolling 60-day Beta for Your Portfolio compared to the S&P 500

# Calculate new variance

rolling_variance2 = stocks_combined2['Custom1'].rolling(window=21).var()

# Calculate new covariance

rolling_covariance2 = stocks_combined2['Custom1'].rolling(window=21).cov(stocks_combined2['SP500'])

# Calculate new beta

rolling_beta2 = rolling_covariance2 / rolling_variance2

# Plot new Beta

rolling_beta2.plot(figsize=(20, 10), title='Portfolio Returns Beta')


# In[194]:


### Using the daily returns, calculate and visualize the Sharpe ratios using a bar plot

# Calculate Annualzied Sharpe Ratios

sharpe_ratios2=(stocks_combined2.mean()*252)/(stocks_combined2.std()*np.sqrt(252))
sharpe_ratios2


# In[195]:


# Visualize the sharpe ratios as a bar plot

sharpe_ratios2.plot(kind='bar', title="Sharpe Ratios 2")


# In[196]:


### How does your portfolio do?

print('How did your portfolio do?')
print()
print('Our portfolio outerperformed its whale investors and the SP500, but failed to beet algo 1.')


# In[ ]:





# In[ ]:




