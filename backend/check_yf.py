import yfinance as yf
import pandas as pd

def check_gold():
    symbol = 'GC=F'
    print(f"Checking yfinance for {symbol}...")
    ticker = yf.Ticker(symbol)
    hist = ticker.history(period="3mo", interval="1d")
    print(f"History rows: {len(hist)}")
    if not hist.empty:
        print("Last 5 rows:")
        print(hist.tail())
    else:
        print("No data found.")

if __name__ == "__main__":
    check_gold()
