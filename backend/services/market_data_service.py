import yfinance as yf
from abc import ABC, abstractmethod
from datetime import datetime, timedelta
import random
import os

try:
    from polygon import RESTClient
except ImportError:
    RESTClient = None

class IMarketDataProvider(ABC):
    @abstractmethod
    def get_last_price(self, symbol: str) -> float:
        pass

    @abstractmethod
    def get_ohlcv(self, symbol: str, timeframe: str, limit: int):
        pass

class PolygonProvider(IMarketDataProvider):
    def __init__(self, api_key):
        self.api_key = api_key
        self.client = RESTClient(api_key=api_key)
        print("Market Data initialized with PolygonProvider (REAL DATA).")

    def get_last_price(self, symbol: str) -> float:
        try:
            # Polygon uses 'C' for crypto (e.g. X:BTCUSD) and stock ticker for stocks
            # Logic to detecting asset type can be improved. 
            # For now assuming straightforward tickers. 
            # Forex in Polygon is C:EURUSD, Crypto X:BTCUSD.
            ticker = self._format_symbol(symbol)
            
            # Simple Previous Close or Real-time Trade
            # previous_close_agg = self.client.get_previous_close_agg(ticker)
            # if previous_close_agg:
            #     return previous_close_agg[0].close
            
            # Let's try last trade (requires realtime sub) or last quote.
            # Fallback to prev close if free tier.
            aggs = self.client.get_aggs(ticker, 1, "day", datetime.now() - timedelta(days=4), datetime.now())
            # Convert generator to list to access last item
            aggs_list = list(aggs)
            if aggs_list:
               return aggs_list[-1].close
               
            return 0.0
        except Exception as e:
            print(f"Polygon Price Error for {symbol}: {e}")
            raise e

    def get_ohlcv(self, symbol: str, timeframe: str, limit: int):
        try:
            ticker = self._format_symbol(symbol)
            # basic mapping
            multiplier = 1
            timespan = "day"
            if timeframe == '1h': timespan = "hour"
            
            # Date range
            end = datetime.now()
            start = end - timedelta(days=limit * 2) # Buffer
            
            aggs = self.client.get_aggs(ticker, multiplier, timespan, start, end)
            data = []
            for agg in aggs:
                # Polygon timestamp is ms
                dt = datetime.fromtimestamp(agg.timestamp / 1000)
                data.append({
                    'time': dt.strftime('%Y-%m-%d'),
                    'open': agg.open,
                    'high': agg.high,
                    'low': agg.low,
                    'close': agg.close,
                    'volume': agg.volume
                })
            return data[-limit:] # Return requested limit
        except Exception as e:
             print(f"Polygon OHLCV Error for {symbol}: {e}")
             raise e

    def _format_symbol(self, symbol):
        # Helper to format for Polygon
        s = symbol.upper()
        if s == 'EURUSD': return 'C:EURUSD'
        if s == 'GBPUSD': return 'C:GBPUSD'
        if s == 'USDJPY': return 'C:USDJPY'
        if s == 'BTCUSD': return 'X:BTCUSD'
        if s == 'ETHUSD': return 'X:ETHUSD'
        if s == 'GOLD': return 'C:XAUUSD'
        if s == 'SILVER': return 'C:XAGUSD'
        
        # If it's a Moroccan stock, Polygon won't have it, so let it fail and fallback
        return s

class YFinanceProvider(IMarketDataProvider):
    def __init__(self):
        print("Market Data initialized with YFinanceProvider (Free Tier).")
        self.symbol_map = {
            'EURUSD': 'EURUSD=X',
            'GBPUSD': 'GBPUSD=X',
            'USDJPY': 'USDJPY=X',
            'BTCUSD': 'BTC-USD',
            'ETHUSD': 'ETH-USD',
            'GOLD': 'GC=F',
            'SILVER': 'SI=F',
            'TSLA': 'TSLA',
            'AAPL': 'AAPL'
        }

    def _map_symbol(self, symbol: str) -> str:
        return self.symbol_map.get(symbol, symbol)

    def get_last_price(self, symbol: str) -> float:
        ticker_symbol = self._map_symbol(symbol)
        ticker = yf.Ticker(ticker_symbol)
        try:
            # history(period='1d') is usually reliable
            hist = ticker.history(period="1d")
            if not hist.empty:
                return hist['Close'].iloc[-1]
            # If empty, we want to fallback
            raise ValueError("Empty history")
        except Exception as e:
            print(f"Error fetching YF price for {symbol}: {e}")
            raise e
        
    def get_ohlcv(self, symbol: str, timeframe: str, limit: int):
        # map timeframe to yfinance intervals
        # 1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo
        interval = '1d'
        if timeframe in ['1m', '5m', '15m', '1h', '1d']:
            interval = timeframe
        
        ticker_symbol = self._map_symbol(symbol)
        ticker = yf.Ticker(ticker_symbol)
        try:
            # period depends on limit and timeframe, simplified here
            hist = ticker.history(period="1mo", interval=interval)
            # transform to list of dicts
            data = []
            for index, row in hist.tail(limit).iterrows():
                time_val = index.strftime('%Y-%m-%d')
                data.append({
                    'time': time_val,
                    'open': row['Open'],
                    'high': row['High'],
                    'low': row['Low'],
                    'close': row['Close'],
                    'volume': row['Volume']
                })
            
            if not data:
                raise ValueError("No data found")
                
            return data
        except Exception as e:
            print(f"Error fetching YF OHLCV for {symbol}: {e}")
            raise e

class MockProvider(IMarketDataProvider):
    """Fallback if everything fails, modified for Moroccan OPCVMs"""
    def __init__(self):
        print("Market Data initialized with MockProvider (Simulation).")

    def _is_opcvm(self, symbol: str) -> bool:
        return symbol.startswith('OPCVM_')

    def get_last_price(self, symbol: str) -> float:
        if self._is_opcvm(symbol):
            base = 1000.0 + (sum(ord(c) for c in symbol) % 500) * 10
            # OPCVM have lower daily volatility
            variation = (random.random() - 0.5) * (base * 0.005) 
            return round(base + variation, 2)
            
        base = 100.0 + (sum(ord(c) for c in symbol) % 500)
        variation = (random.random() - 0.5) * 2
        return round(base + variation, 2)

    def get_ohlcv(self, symbol: str, timeframe: str, limit: int):
        data = []
        import datetime as dt
        base_price = self.get_last_price(symbol)
        start_date = datetime.now() - dt.timedelta(days=limit)
        is_fond = self._is_opcvm(symbol)
        
        for i in range(limit):
            current_date = start_date + dt.timedelta(days=i)
            # Volatility is much smaller for funds
            volatility_factor = 0.002 if is_fond else 0.02
            move = (random.random() - 0.5) * (base_price * volatility_factor)
            
            # Add a slight upward drift over time for OPCVMs as they generally appreciate
            if is_fond:
                 move += (base_price * 0.0005)
                 
            close_p = base_price + move
            
            # Less intraday variation for funds
            spread = (close_p * 0.001) if is_fond else 1.0
            
            data.append({
                'time': current_date.strftime('%Y-%m-%d'),
                'open': round(base_price, 2),
                'high': round(max(base_price, close_p) + spread, 2),
                'low': round(min(base_price, close_p) - spread, 2),
                'close': round(close_p, 2),
                # Funds have lower, simulated block volumes
                'volume': int(random.random() * 5000) if is_fond else int(random.random() * 100000)
            })
            base_price = close_p
        return data

class MarketDataFactory:
    @staticmethod
    def get_provider() -> IMarketDataProvider:
        # Forcing MockProvider to ensure app is responsive on localhost
        return MockProvider()

    @staticmethod
    def get_fallback_provider():
        return MockProvider()
