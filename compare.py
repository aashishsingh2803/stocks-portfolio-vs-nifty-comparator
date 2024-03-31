from parser import get_nifty_data, get_zerodha_data
import pandas as pd
import numpy as np
from datetime import datetime
from pyxirr import xirr

# https://in.investing.com/indices/s-p-cnx-nifty-historical-data?end_date=1710009000&st_date=1577817000
# Update this to fetch updated data using NSE API - https://www.nseindia.com/api/historical/indicesHistory?indexType=NIFTY%2050&from=01-01-2019&to=25-12-2019
nifty_data = get_nifty_data()

# Add input params for getting user input.
user = 'sample_user'
zerodha_data = get_zerodha_data(user)

curr_quantity = 0 # 12
curr_avg_price = 0   # 1212.12

total_sell_amount = 0
total_buy_amount = 0

cash_flows = []
cash_flow_dates = []

nifty_sell_amount = 0
# Handle case where nifty quantity can go in negative as we are not checking for < 0 quantity of nifty.
for trade in zerodha_data:
  trade_amount = trade['total_amount']
  trade_date = trade['trade_date']
  cash_flow_dates.append(trade_date)
  print(f"trade_date - {trade_date}, trade_amount - {trade_amount}, trade_type - {trade['trade_type']}, curr_nifty_quantity - {curr_quantity}, curr_nifty_avg_price - {curr_avg_price}")
  if 'buy' == trade['trade_type']:
    cash_flows.append(-trade_amount)

    new_quantity = trade_amount / nifty_data[trade_date]
    curr_avg_price = ((curr_quantity * curr_avg_price) + (trade_amount)) / (curr_quantity+ new_quantity)
    curr_quantity += new_quantity
    total_buy_amount += trade_amount
  elif 'sell' == trade['trade_type']:
    cash_flows.append(trade_amount)
    new_quantity = trade_amount / nifty_data[trade_date]
    total_sell_amount += trade_amount
    curr_avg_price = ((curr_quantity * curr_avg_price) - (trade_amount)) / (curr_quantity - new_quantity)
    curr_quantity -= new_quantity


curr_nifty_value = curr_quantity * nifty_data[max(nifty_data.keys())]

cash_flow_dates.append(max(nifty_data.keys()))
cash_flows.append(curr_nifty_value)
xirr_perc = xirr(cash_flow_dates, cash_flows)*100

print("\n\n=======================================")
print(f"Total buy amount - {total_buy_amount:.2f}")
print("=======================================")
print(f"Total sell amount - {total_sell_amount:.2f}")
print("=======================================")
print(f"curr nifty quantity - {curr_quantity:.2f}, curr_avg_price - {curr_avg_price:.2f}")
print("================================================================")
print(f"If nifty is sold today then we get this much amount - {curr_nifty_value:.2f}")
print("================================================================")
print(f"XIRR if you invested in NIFTY: {xirr_perc:.2f}%")
print("================================================================")
