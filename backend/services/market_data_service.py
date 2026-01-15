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
        if symbol == 'EURUSD': return 'C:EURUSD'
        if symbol == 'GBPUSD': return 'C:GBPUSD'
        if symbol == 'USDJPY': return 'C:USDJPY'
        if symbol == 'BTCUSD': return 'X:BTCUSD'
        return symbol

class YFinanceProvider(IMarketDataProvider):
    def __init__(self):
        print("Market Data initialized with YFinanceProvider (Free Tier).")

    def get_last_price(self, symbol: str) -> float:
        ticker = yf.Ticker(symbol)
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
        
        ticker = yf.Ticker(symbol)
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
    """Fallback if everything fails"""
    def __init__(self):
        print("Market Data initialized with MockProvider (Simulation).")

    def get_last_price(self, symbol: str) -> float:
        base = 100.0 + (sum(ord(c) for c in symbol) % 500)
        variation = (random.random() - 0.5) * 2
        return round(base + variation, 2)

    def get_ohlcv(self, symbol: str, timeframe: str, limit: int):
        data = []
        import datetime as dt
        base_price = self.get_last_price(symbol)
        start_date = datetime.now() - dt.timedelta(days=limit)
        for i in range(limit):
            current_date = start_date + dt.timedelta(days=i)
            move = (random.random() - 0.5) * 2
            close_p = base_price + move
            data.append({
                'time': current_date.strftime('%Y-%m-%d'),
                'open': round(base_price, 2),
                'high': round(max(base_price, close_p) + 1, 2),
                'low': round(min(base_price, close_p) - 1, 2),
                'close': round(close_p, 2),
                'volume': int(random.random() * 100000)
            })
            base_price = close_p
        return data

class MarketDataFactory:
    @staticmethod
    def get_provider() -> IMarketDataProvider:
        api_key = os.environ.get('POLYGON_API_KEY')
        
        # Priority 1: Polygon (if key exists and library installed)
        if api_key and RESTClient:
            try:
                # Test connection (optional, or just return)
                return PolygonProvider(api_key)
            except:
                pass
        
        # Priority 2: YFinance (Free Tier)
        # Note: YFinance can be flaky, so we wrap in try/catch logic in consumption too,
        # but here we just return the provider.
        return YFinanceProvider()

    @staticmethod
    def get_fallback_provider():
        return MockProvider()
