import pandas as pd
import numpy as np
from typing import List, Dict, Any

class TechnicalAnalysisUtils:
    @staticmethod
    def calculate_indicators(df: pd.DataFrame) -> Dict[str, Any]:
        """
        Calculate common technical indicators: RSI, MACD, and EMAs.
        Expects a DataFrame with 'close' column.
        """
        if df.empty or len(df) < 50: # Need enough data for calculations
            return {}

        # 1. RSI (14)
        delta = df['close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['rsi'] = 100 - (100 / (1 + rs))

        # 2. MACD (12, 26, 9)
        exp1 = df['close'].ewm(span=12, adjust=False).mean()
        exp2 = df['close'].ewm(span=26, adjust=False).mean()
        df['macd'] = exp1 - exp2
        df['macd_signal'] = df['macd'].ewm(span=9, adjust=False).mean()
        df['macd_hist'] = df['macd'] - df['macd_signal']

        # 3. EMAs (20, 50, 200)
        df['ema_20'] = df['close'].ewm(span=20, adjust=False).mean()
        df['ema_50'] = df['close'].ewm(span=50, adjust=False).mean()
        df['ema_200'] = df['close'].ewm(span=200, adjust=False).mean()

        last = df.iloc[-1]
        
        # Categorize RSI
        rsi_val = float(last['rsi'])
        rsi_signal = "Neutral"
        if rsi_val > 70: rsi_signal = "Overbought"
        elif rsi_val < 30: rsi_signal = "Oversold"

        # Categorize MACD
        macd_val = float(last['macd'])
        macd_sig = float(last['macd_signal'])
        macd_signal_cat = "Bullish" if macd_val > macd_sig else "Bearish"

        # EMA Alignment
        ema20 = float(last['ema_20'])
        ema50 = float(last['ema_50'])
        ema200 = float(last['ema_200'])
        
        alignment = "Mixed"
        if ema20 > ema50 > ema200: alignment = "Bullish"
        elif ema20 < ema50 < ema200: alignment = "Bearish"

        return {
            "rsi": {"value": round(rsi_val, 2), "signal": rsi_signal},
            "macd": {"value": round(macd_val, 4), "signal": macd_signal_cat, "histogram": round(float(last['macd_hist']), 4)},
            "ema": {"ema_20": round(ema20, 4), "ema_50": round(ema50, 4), "ema_200": round(ema200, 4), "alignment": alignment},
            "close": float(last['close'])
        }
