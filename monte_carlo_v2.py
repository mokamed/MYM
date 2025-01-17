# -*- coding: utf-8 -*-
"""

________  ___  ___  ________  ________  ___  ________  _______   ________  ___  _________  ________
|\   ____\|\  \|\  \|\   ____\|\   ____\|\  \|\   __  \|\  ___ \ |\   __  \|\  \|\___   ___\\   __  \
\ \  \___|\ \  \\\  \ \  \___|\ \  \___|\ \  \ \  \|\  \ \   __/|\ \  \|\  \ \  \|___ \  \_\ \  \|\  \
 \ \  \  __\ \  \\\  \ \  \    \ \  \    \ \  \ \   ____\ \  \_|/_\ \   ____\ \  \   \ \  \ \ \  \\\  \
  \ \  \|\  \ \  \\\  \ \  \____\ \  \____\ \  \ \  \___|\ \  \_|\ \ \  \___|\ \  \   \ \  \ \ \  \\\  \
   \ \_______\ \_______\ \_______\ \_______\ \__\ \__\    \ \_______\ \__\    \ \__\   \ \__\ \ \_______\
    \|_______|\|_______|\|_______|\|_______|\|__|\|__|     \|_______|\|__|     \|__|    \|__|  \|_______|


_  _ ____ _  _ ___ ____    ____ ____ ____ _    ____    ____ _ _  _ _  _ _    ____ ___ _ ____ _  _
|\/| |  | |\ |  |  |___    |    |__| |__/ |    |  |    [__  | |\/| |  | |    |__|  |  | |  | |\ |
|  | |__| | \|  |  |___    |___ |  | |  \ |___ |__|    ___] | |  | |__| |___ |  |  |  | |__| | \|

"""

# Installation of necessary libraries

import numpy as np
import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
from datetime import datetime

# Downloading historical stock data
def download_stock_data(ticker, start_date, end_date):
    """Download historical stock data from Yahoo Finance.

    Parameters:
    ticker (str): Ticker symbol of the stock.
    start_date (str): Start date of the historical data (YYYY-MM-DD).
    end_date (str): End date of the historical data (YYYY-MM-DD).

    Returns:
    pandas.Series: Close prices of the stock.
    str: Short name of the stock.
    """
    stock = yf.Ticker(ticker)
    data = stock.history(start=start_date, end=end_date)
    return data['Close'], stock.info['shortName']

# Monte Carlo simulation for theoretical future stock price
def monte_carlo_simulation(data, num_simulations, num_days, short_name):
    """Perform Monte Carlo simulation for predicting future stock prices.

    Parameters:
    data (pandas.Series): Historical stock price data.
    num_simulations (int): Number of simulations to run.
    num_days (int): Number of days to simulate into the future.
    short_name (str): Short name of the stock.

    Returns:
    pandas.Series: Last simulated prices.
    float: Average predicted price after all simulations.
    """
    returns = (data / data.shift(1) - 1).dropna()
    last_price = data[-1]
    simulation_df = pd.DataFrame()

    for x in range(num_simulations):
        count = 0
        daily_vol = returns.std()
        price_series = []
        price = last_price * (1 + np.random.normal(0, daily_vol))
        price_series.append(price)

        for y in range(num_days - 1):
            if count == 251:
                break
            price = price_series[count] * (1 + np.random.normal(0, daily_vol))
            price_series.append(price)
            count += 1

        simulation_df[x] = price_series

    plt.figure(figsize=(10, 6))
    plt.plot(simulation_df)
    plt.axhline(simulation_df.iloc[-1].mean(), color='green', linestyle='--', linewidth=1, label='Average Predicted Price: {:.2f}'.format(simulation_df.iloc[-1].mean()))
    plt.axhline(last_price, color='gray', linestyle='--', linewidth=1, label='Current Price: {:.2f}'.format(last_price))
    plt.xlabel('Days')
    plt.ylabel('Stock Price')
    plt.title('Monte Carlo Simulation for Theoretical Future Price of {}'.format(short_name))
    plt.legend()
    plt.show()

    average_predicted_price = simulation_df.iloc[-1].mean()

    return simulation_df.iloc[-1], average_predicted_price

# Parameters
ticker = 'BFH'  # Stock ticker symbol (Microsoft in this example)
start_date = '2023-01-01'  # Start date of historical data
end_date = datetime.now().strftime("%Y-%m-%d")  # End date of historical data (today's date)
num_simulations = 1000  # Number of Monte Carlo simulations
num_days = 252  # Number of days for the simulation

# Downloading historical data
stock_data, short_name = download_stock_data(ticker, start_date, end_date)

# Monte Carlo Simulation
monte_carlo_prices, average_predicted_price = monte_carlo_simulation(stock_data, num_simulations, num_days, short_name)

# Average predicted price after all simulations
print("\nAverage predicted price after all simulations with Monte Carlo:", average_predicted_price)
