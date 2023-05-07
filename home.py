import pandas as pd
import yfinance as yf
import matplotlib.pyplot as plt
import time

# Define the trading strategy parameters
symbol = "HAL"
lookback = 15
overbought = 70
oversold = 30
capital = 10000

# Define the trading function
def trade(symbol, lookback, overbought, oversold, capital):
    # Download the historical data
    data = yf.download(symbol, interval='1m', period='1d')
    
    # Calculate the RSI indicator
    delta = data['Close'].diff()
    gain = delta.mask(delta<0, 0)
    loss = -delta.mask(delta>0, 0)
    avg_gain = gain.rolling(lookback).mean()
    avg_loss = loss.rolling(lookback).mean()
    rs = avg_gain / avg_loss
    rsi = 100.0 - (100.0 / (1.0 + rs))
    
    # Determine the trading signals
    signal = pd.Series(0, index=data.index)
    signal[rsi > overbought] = -1
    signal[rsi < oversold] = 1
    
    # Calculate the position and P&L
    position = signal.shift(1).fillna(0)
    position_value = position * data['Close'] * capital / data['Close'][0]
    pnl = position_value.diff().fillna(0)
    
    # Plot the RSI and trading signals
    fig, ax = plt.subplots(2, 1, figsize=(12, 8))
    ax[0].plot(data.index, data['Close'], label='Close')
    ax[1].plot(data.index, rsi, label='RSI')
    ax[1].axhline(overbought, color='r', linestyle='--')
    ax[1].axhline(oversold, color='r', linestyle='--')
    ax[1].fill_between(data.index, overbought, 100, alpha=0.1, color='r')
    ax[1].fill_between(data.index, oversold, 0, alpha=0.1, color='g')
    ax[1].plot(data.index, signal * 100, label='Signal', linestyle='None', marker='o')
    ax[0].legend()
    ax[1].legend()
    plt.show()
    
    # Print the P&L statistics
    print('Total P&L: {:.2f}'.format(pnl.sum()))
    print('Average P&L per trade: {:.2f}'.format(pnl.mean()))
    print('Win rate: {:.2%}'.format((pnl > 0).sum() / len(pnl)))
    
# Run the trading function every hour
while True:
    trade(symbol, lookback, overbought, oversold, capital)
    time.sleep(60*60) # wait for 1 hour

