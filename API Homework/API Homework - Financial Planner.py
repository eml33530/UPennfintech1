#!/usr/bin/env python
# coding: utf-8

# # API Homework - Financial Planner

# In[39]:


# Initial imports
import os
import requests
import pandas as pd
from dotenv import load_dotenv
import alpaca_trade_api as tradeapi
from MCForecastTools import MCSimulation

get_ipython().run_line_magic('matplotlib', 'inline')


# In[40]:


# Load .env enviroment variables
load_dotenv()


# ## Part 1 - Personal Finance Planner

# ### Collect Crypto Prices Using the requests Library

# In[41]:


# Set current amount of crypto assets
# YOUR CODE HERE!

my_btc=1.2
my_eth=5.3


# In[42]:


# Crypto API URLs
btc_url = "https://api.alternative.me/v2/ticker/Bitcoin/?convert=CAD"
eth_url = "https://api.alternative.me/v2/ticker/Ethereum/?convert=CAD"


# In[47]:


# Requesting the data

request_btc_data= requests.get(btc_url)
btc_data=request_btc_data.json()
import json
print(json.dumps(btc_data, indent=4))

request_eth_data= requests.get(eth_url)
eth_data=request_eth_data.json()
import json
print(json.dumps(eth_data, indent=4))


# In[49]:


# Fetch current BTC price
# Fetch current ETH price
# Compute current value of my crpto

btc_price=btc_data["data"]["1"]["quotes"]["USD"]["price"]
my_btc_value=my_btc*btc_price
eth_price=eth_data["data"]["1027"]["quotes"]["USD"]["price"]
my_eth_value=my_eth*eth_price


# Print current crypto wallet balance
print(f"The current value of your {my_btc} BTC is ${my_btc_value:0.2f}")
print(f"The current value of your {my_eth} ETH is ${my_eth_value:0.2f}")


# ### Collect Investments Data Using Alpaca: SPY (stocks) and AGG (bonds)

# In[50]:


# Current amount of shares
my_agg = 200
my_spy = 50


# In[51]:


# Set Alpaca API key and secret
# Create the Alpaca API object

alpaca_api_key = os.getenv("ALPACA_API_KEY")
alpaca_secret_key = os.getenv("ALPACA_SECRET_KEY")

api = tradeapi.REST(
    alpaca_api_key,
    alpaca_secret_key,
    api_version = "v2")


# In[67]:


# Set the tickers
tickers = ["AGG", "SPY"]

# Set timeframe to '1D' for Alpaca API
timeframe = "1D"

# Format current date as ISO format

today = pd.Timestamp("2021-03-12", tz="America/New_York").isoformat()

# Get current closing prices for SPY and AGG

df_portfolio=api.get_barset(tickers,timeframe,start=today,end=today,limit=1000).df
df_portfolio.index=df_portfolio.index.date
df_portfolio.head()


# In[68]:


# Pick AGG and SPY close prices

agg_close_price=float(df_portfolio["AGG"]["close"])
spy_close_price=float(df_portfolio["SPY"]["close"])

# Print AGG and SPY close prices
print(f"Current AGG closing price: ${agg_close_price}")
print(f"Current SPY closing price: ${spy_close_price}")


# In[69]:


# Compute the current value of shares
my_agg_value=my_agg*agg_close_price
my_spy_value=my_spy*spy_close_price


# Print current value of share
print(f"The current value of your {my_spy} SPY shares is ${my_spy_value:0.2f}")
print(f"The current value of your {my_agg} AGG shares is ${my_agg_value:0.2f}")


# ### Savings Health Analysis

# In[83]:


# Set monthly household income
monthly_income=12000
total_crypto=my_btc_value+my_eth_value
total_stocks=my_agg_value+my_spy_value
data={'$':[crypto,stocks]}

# Create savings DataFrame

df_savings=pd.DataFrame(data, index=['Crypto','Stock Portfolio'])

# Display savings DataFrame
display(df_savings)


# In[84]:


# Plot savings pie chart

df_savings.plot.pie(y="$", title="Personal Savings Portfolio")


# In[85]:


# Set ideal emergency fund
emergency_fund = monthly_income * 3

# Calculate total amount of savings
total_savings=total_crypto+total_stocks

# Validate saving health

if total_savings>emergency_fund:
   print("Congratulations! You have enough money in your emergency fund.")
elif total_savings==emergency_fund:
   print("Congratulations! You have reached this financial goal.")
else:
   print(f"You are currently ${emergency_fund - total_savings} away from reaching the financial goal")


# # Part 2 - Retirement Planning

# ### Monte Carlo Simulation

# In[86]:


# Set start and end dates of five years back from today.
# Sample results may vary from the solution based on the time frame chosen
start_date = pd.Timestamp('2015-08-07', tz='America/New_York').isoformat()
end_date = pd.Timestamp('2020-08-07', tz='America/New_York').isoformat()


# In[91]:


# Get 5 years' worth of historical data for SPY and AGG

df_stock_data=api.get_barset(tickers,timeframe,start=start_date,end=end_date,limit=1000).df
df_stock_data.index=df_stock_data.index.date

# Display sample data
df_stock_data.head()


# In[92]:


# Configuring a Monte Carlo simulation to forecast 30 years cumulative returns

MC_dist=MCSimulation(
   portfolio_data=df_stock_data,
   weights=[.40,.60],
   num_simulation=500,
   num_trading_days=252*30)

# Print the simulation input data
MC_dist.portfolio_data.head()
   
   


# In[93]:


# Running a Monte Carlo simulation to forecast 30 years cumulative returns

MC_dist.calc_cumulative_return()


# In[94]:


# Plot simulation outcomes


line_plot=MC_dist.plot_simulation()


# In[95]:


# Plot probability distribution and confidence intervals

dist_plot=MC_dist.plot_distribution()


# ### Retirement Analysis

# In[97]:


# Fetch summary statistics from the Monte Carlo simulation results

tbl=MC_dist.summarize_cumulative_return()

# Print summary statistics

print(tbl)


# ### Calculate the expected portfolio return at the 95% lower and upper confidence intervals based on a $20,000 initial investment.

# In[99]:


# Set initial investment
initial_investment = 20000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $20,000
ci_lower=round(tbl[8]*initial_investment,2)
ci_upper=round(tbl[9]*initial_investment,2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
     f" over the next 30 years will end within in the range of"
     f" ${ci_lower} and ${ci_upper}")


# ### Calculate the expected portfolio return at the 95% lower and upper confidence intervals based on a 50% increase in the initial investment.

# In[100]:


# Set initial investment
initial_investment = 20000 * 1.5

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $30,000

ci_lower=round(tbl[8]*initial_investment,2)
ci_upper=round(tbl[9]*initial_investment,2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 30 years will end within in the range of"
      f" ${ci_lower} and ${ci_upper}")


# ## Optional Challenge - Early Retirement

# ### Five Years Retirement Option

# In[112]:


# Configuring a Monte Carlo simulation to forecast 5 years cumulative returns

MC_5yr_dist=MCSimulation(
    portfolio_data=df_stock_data,
    weights=[.40,.60],
    num_simulation=500,
    num_trading_days=252*5)

# Print the simulation input data
MC_5yr_dist.portfolio_data.head()


# In[113]:


# Running a Monte Carlo simulation to forecast 5 years cumulative returns
# YOUR CODE HERE!

MC_5yr_dist.calc_cumulative_return()


# In[118]:


# Plot simulation outcomes

line_plot_5yr=MC_5yr_dist.plot_simulation()


# In[119]:


# Plot probability distribution and confidence intervals
dist_plot_5yr=MC_5yr_dist.plot_distribution()


# In[120]:


# Fetch summary statistics from the Monte Carlo simulation results

tbl_5yr=MC_5yr_dist.summarize_cumulative_return()

# Print summary statistics

print(tbl_5yr)


# In[121]:


# Set initial investment

initial_investment = 60000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $30,000

ci_lower_five=round(tbl_5yr[8]*initial_investment,2)
ci_upper_five=round(tbl_5yr[9]*initial_investment,2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 5 years will end within in the range of"
      f" ${ci_lower_five} and ${ci_upper_five}")


# ### Ten Years Retirement Option

# In[106]:


# Configuring a Monte Carlo simulation to forecast 10 years cumulative returns
MC_10yr_dist=MCSimulation(
    portfolio_data=df_stock_data,
    weights=[.40,.60],
    num_simulation=500,
    num_trading_days=252*10)

# Print the simulation input data
MC_10yr_dist.portfolio_data.head()


# In[107]:


# Running a Monte Carlo simulation to forecast 10 years cumulative returns
MC_10yr_dist.calc_cumulative_return()


# In[122]:


# Plot simulation outcomes
line_plot_10yr=MC_10yr_dist.plot_simulation()


# In[123]:


# Plot probability distribution and confidence intervals
dist_plot_10yr=MC_10yr_dist.plot_distribution()


# In[124]:


# Fetch summary statistics from the Monte Carlo simulation results
tbl_10yr=MC_10yr_dist.summarize_cumulative_return()

# Print summary statistics

print(tbl_10yr)


# In[125]:


# Set initial investment
initial_investment = 60000

# Use the lower and upper `95%` confidence intervals to calculate the range of the possible outcomes of our $60,000

ci_lower_ten=round(tbl_10yr[8]*initial_investment,2)
ci_upper_ten=round(tbl_10yr[9]*initial_investment,2)

# Print results
print(f"There is a 95% chance that an initial investment of ${initial_investment} in the portfolio"
      f" over the next 10 years will end within in the range of"
      f" ${ci_lower_ten} and ${ci_upper_ten}")


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




