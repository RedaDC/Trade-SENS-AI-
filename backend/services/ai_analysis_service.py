"""
AI Analysis Service
Supports:
1. DEMO Mode: Simulated analysis using random indicators (Default)
2. REAL Mode: Uses OpenAI GPT-4o to analyze data (Requires OPENAI_API_KEY)
"""
import random
import os
import json
from datetime import datetime
from typing import Dict, List, Any

try:
    from openai import OpenAI
except ImportError:
    OpenAI = None

class AIAnalysisService:
    """AI-powered trading analysis engine"""
    
    def __init__(self):
        self.api_key = os.environ.get('OPENAI_API_KEY')
        if self.api_key and OpenAI:
            self.client = OpenAI(api_key=self.api_key)
            self.mode = "REAL"
            print("AI Service initialized in REAL mode (GPT-4o).")
        else:
            self.client = None
            self.mode = "DEMO"
            print("AI Service initialized in DEMO mode.")
    
    def analyze_symbol(self, symbol: str, timeframe: str = "1D") -> Dict[str, Any]:
        """
        Perform comprehensive AI analysis on a symbol
        """
        # Simulate current price (Step 0: Data Gathering)
        # In a full production version, this would call MarketDataService
        price = self._get_simulated_price(symbol)
        
        # Gather basic technical/news data to feed the AI (or use in Demo)
        news_analysis = self._analyze_news(symbol)
        technical = self._analyze_technical_indicators(symbol, price)
        
        if self.mode == "REAL":
            try:
                return self._call_llm_analysis(symbol, timeframe, price, technical, news_analysis)
            except Exception as e:
                print(f"LLM Analysis failed: {e}. Falling back to DEMO.")
                # Fallback to demo logic if API fails
        
        return self._get_simulated_analysis(symbol, timeframe, price, news_analysis, technical)

    def _call_llm_analysis(self, symbol, timeframe, price, technical, news) -> Dict[str, Any]:
        """Call OpenAI GPT-4o to generate analysis"""
        
        system_prompt = "You are an expert institutional trading AI. You provide data-driven trading analysis, strict risk management, and clear execution signals."
        
        user_prompt = f"""
        Analyze {symbol} (Price: {price}) on {timeframe} timeframe.
        
        Technical Data:
        {json.dumps(technical, indent=2)}
        
        News Context:
        {json.dumps(news, indent=2)}
        
        Task:
        1. Determine the Market Structure (Trend, S/R levels).
        2. Analyze Sentiment.
        3. Evaluate Trade Scenarios (Bullish/Bearish/Wait).
        4. Make a DECISION (BUY, SELL, or WAIT) with a confidence score.
        5. Provide strict Risk Management (Entry, SL, TP) if actionable.
        
        Output strictly valid JSON with this structure:
        {{
            "analysis": {{
                "news_macro": {{ "impact": "...", "key_events": [], "description": "...", "overreaction_risk": "..." }},
                "market_structure": {{ "trend": "...", "trend_strength": "...", "support_level": 0.0, "resistance_level": 0.0 }},
                "technical": {{ 
                    "rsi": {{ "value": 0, "signal": "..." }},
                    "macd": {{ "signal": "..." }},
                    "ema": {{ "alignment": "..." }},
                    "volume": {{ "trend": "..." }}
                }},
                "sentiment": {{ "environment": "...", "fear_greed_index": 0, "sentiment_label": "...", "positioning": "..." }},
                "scenarios": {{
                    "bullish": {{ "probability": 0, "case": "...", "target": 0.0 }},
                    "bearish": {{ "probability": 0, "case": "...", "target": 0.0 }},
                    "wait": {{ "probability": 0, "case": "...", "reason": "..." }}
                }},
                "decision": {{ "recommendation": "BUY/SELL/WAIT", "confidence": 0, "reasoning": "..." }},
                "risk_management": {{ "entry_zone": "...", "stop_loss": 0.0, "take_profit": 0.0, "risk_reward_ratio": 0.0, "position_size": "...", "risk_level": "..." }}
            }}
        }}
        """
        
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt}
            ],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        
        content = response.choices[0].message.content
        data = json.loads(content)
        
        # Ensure the response structure wraps correctly
        analysis_data = data.get("analysis", data)
        
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "current_price": price,
            "timestamp": datetime.now().isoformat(),
            "mode": "REAL (GPT-4o)",
            "analysis": analysis_data
        }

    def _get_simulated_analysis(self, symbol, timeframe, price, news_analysis, technical):
        """
        Smart Demo Logic: Generates coherent, correlated data.
        Unlike the random version, this ensures indicators match the trend.
        """
        
        # 1. Determine Major Trend (Randomly, but then enforces consistency)
        trend_direction = random.choices(["Bullish", "Bearish", "Range"], weights=[40, 40, 20])[0]
        
        # 2. Generate Correlated Technicals based on Trend
        technical = self._generate_coherent_technicals(trend_direction, price)
        
        # 3. Generate Correlated Market Structure
        market_structure = self._generate_coherent_structure(trend_direction, price)
        
        # 4. Generate Correlated Sentiment
        sentiment = self._generate_coherent_sentiment(trend_direction)
        
        # 5. Generate Correlated Scenarios
        scenarios = self._evaluate_coherent_scenarios(trend_direction, price)
        
        # 6. Make Decision (Obvious based on the trend)
        decision = self._make_coherent_decision(trend_direction, scenarios)
        
        # 7. Risk Management
        risk_management = self._calculate_risk_management(decision, price)
        
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "current_price": price,
            "timestamp": datetime.now().isoformat(),
            "mode": "Simulated Professional (Demo)",
            "analysis": {
                "news_macro": self._generate_coherent_news(trend_direction, symbol),
                "market_structure": market_structure,
                "technical": technical,
                "sentiment": sentiment,
                "scenarios": scenarios,
                "decision": decision,
                "risk_management": risk_management
            }
        }
    
    # --- Coherent Generators ---

    def _generate_coherent_technicals(self, trend, price):
        """Generate indicators that actually match the price action"""
        if trend == "Bullish":
            rsi = random.randint(55, 75)
            rsi_signal = "Bullish Momentum" if rsi < 70 else "Overbought"
            macd_val = round(random.uniform(0.1, 0.5), 3)
            macd_sig = "Bullish"
            ema_align = "Bullish" # 20 > 50 > 200
            ema_20 = price * 0.995
            ema_50 = price * 0.985
            ema_200 = price * 0.95
        elif trend == "Bearish":
            rsi = random.randint(25, 45)
            rsi_signal = "Bearish Momentum" if rsi > 30 else "Oversold"
            macd_val = round(random.uniform(-0.5, -0.1), 3)
            macd_sig = "Bearish"
            ema_align = "Bearish" # 20 < 50 < 200
            ema_20 = price * 1.005
            ema_50 = price * 1.015
            ema_200 = price * 1.05
        else: # Range
            rsi = random.randint(45, 55)
            rsi_signal = "Neutral"
            macd_val = round(random.uniform(-0.05, 0.05), 3)
            macd_sig = "Neutral"
            ema_align = "Mixed"
            ema_20 = price * 1.001
            ema_50 = price * 0.999
            ema_200 = price * 1.01
            
        return {
            "rsi": {"value": rsi, "signal": rsi_signal, "period": 14},
            "macd": {"value": macd_val, "signal": macd_sig, "histogram": "Positive" if macd_val > 0 else "Negative"},
            "ema": {"ema_20": round(ema_20, 2), "ema_50": round(ema_50, 2), "ema_200": round(ema_200, 2), "alignment": ema_align},
            "volume": {"trend": "Increasing" if trend != "Range" else "Stable"}
        }

    def _generate_coherent_structure(self, trend, price):
        if trend == "Bullish":
            support = round(price * 0.98, 2)
            resistance = round(price * 1.05, 2) # Far away
            trend_str = "Strong Uptrend"
        elif trend == "Bearish":
            support = round(price * 0.95, 2) # Far away
            resistance = round(price * 1.02, 2)
            trend_str = "Strong Downtrend"
        else:
            support = round(price * 0.99, 2)
            resistance = round(price * 1.01, 2)
            trend_str = "Consolidation"
            
        return {
            "trend": trend_str,
            "trend_strength": "High" if trend != "Range" else "Low",
            "support_level": support,
            "resistance_level": resistance
        }

    def _generate_coherent_sentiment(self, trend):
        if trend == "Bullish":
            score = random.randint(60, 85)
            label = "Greed"
            env = "Risk-On"
        elif trend == "Bearish":
            score = random.randint(15, 40)
            label = "Fear"
            env = "Risk-Off"
        else:
            score = random.randint(45, 55)
            label = "Neutral"
            env = "Mixed"
            
        return {
            "environment": env,
            "fear_greed_index": score,
            "sentiment_label": label,
            "positioning": f"Biased {trend}"
        }

    def _generate_coherent_news(self, trend, symbol):
        impact = trend if trend != "Range" else "Neutral"
        headlines = {
            "Bullish": ["Strong Earnings Beat Expectations", "Analyst Upgrades to Outperform", "Positive Macro Data Release"],
            "Bearish": ["Inflation Concerns Rise", "Missed Earnings & Weak Guidance", "Regulatory Headwinds Intensify"],
            "Neutral": ["Market Awaits Fed Decision", "Consolidation Continues on Low Vol", "Mixed Economic Data"]
        }
        return {
            "impact": impact,
            "key_events": random.sample(headlines.get(trend, headlines["Neutral"]), 2),
            "description": f"News flow is supporting a {trend.lower()} outlook.",
            "overreaction_risk": "Medium"
        }

    def _evaluate_coherent_scenarios(self, trend, price):
        if trend == "Bullish":
            return {
                "bullish": {"probability": 75, "case": f"Breakout above {round(price*1.005, 2)} confirms continuation.", "target": round(price*1.04, 2)},
                "bearish": {"probability": 15, "case": f"Unexpected drop below {round(price*0.99, 2)} invalidates.", "target": round(price*0.97, 2)},
                "wait": {"probability": 10, "case": "Consolidation at highs.", "reason": "Overbought temporarily."}
            }
        elif trend == "Bearish":
            return {
                "bullish": {"probability": 15, "case": f"Reversal above {round(price*1.02, 2)}.", "target": round(price*1.05, 2)},
                "bearish": {"probability": 75, "case": f"breakdown below {round(price*0.995, 2)} targets lows.", "target": round(price*0.95, 2)},
                "wait": {"probability": 10, "case": "Oversold bounce likely.", "reason": "Taking profits."}
            }
        else: # Range
            return {
                "bullish": {"probability": 30, "case": f"Break resistance at {round(price*1.01, 2)}.", "target": round(price*1.03, 2)},
                "bearish": {"probability": 30, "case": f"Break support at {round(price*0.99, 2)}.", "target": round(price*0.97, 2)},
                "wait": {"probability": 40, "case": "Chop city.", "reason": "No clear direction."}
            }

    def _make_coherent_decision(self, trend, scenarios):
        if trend == "Bullish":
            return {
                "recommendation": "BUY",
                "confidence": scenarios["bullish"]["probability"],
                "reasoning": "Strong bullish structure with confirmed EMA alignment and positive momentum."
            }
        elif trend == "Bearish":
            return {
                "recommendation": "SELL",
                "confidence": scenarios["bearish"]["probability"],
                "reasoning": "Bearish market structure, negative MACD, and price rejected at EMA resistance."
            }
        else:
            return {
                "recommendation": "WAIT",
                "confidence": scenarios["wait"]["probability"],
                "reasoning": "Market is consolidating. Wait for a breakout of key levels before entering."
            }
    
    def _get_simulated_price(self, symbol: str) -> float:
        """Generate realistic simulated price"""
        base_prices = {
            "EURUSD": 1.0950, "GBPUSD": 1.2750, "USDJPY": 148.50,
            "BTCUSD": 45000.00, "TSLA": 245.00, "AAPL": 185.00, "GOLD": 2030.00,
        }
        if symbol.endswith('.MA'):
            base = 100.0 + (sum(ord(c) for c in symbol) % 500)
        else:
            base = base_prices.get(symbol, 100.0)
        variation = (random.random() - 0.5) * (base * 0.02)
        return round(base + variation, 2)
    
    def _analyze_news(self, symbol: str) -> Dict[str, Any]:
        """Placeholder for Real Mode pre-analysis"""
        return {}
    
    def _analyze_technical_indicators(self, symbol: str, price: float) -> Dict[str, Any]:
        """Placeholder for Real Mode pre-analysis"""
        return {}
    
    def _analyze_market_structure(self, symbol: str, price: float) -> Dict[str, Any]:
        """Placeholder for Real Mode pre-analysis"""
        return {}
    
    def _analyze_sentiment(self, symbol: str) -> Dict[str, Any]:
        """Placeholder for Real Mode pre-analysis"""
        return {}
        
    def _evaluate_scenarios(self, symbol: str, price: float, technical: Dict, sentiment: Dict) -> Dict[str, Any]:
        """Placeholder for Real Mode pre-analysis"""
        return {}
        
    def _make_decision(self, scenarios: Dict, technical: Dict, market_structure: Dict) -> Dict[str, Any]:
        """Placeholder for Real Mode pre-analysis"""
        return {}
        
    def _calculate_risk_management(self, decision: Dict, price: float) -> Dict[str, Any]:
        """Calculate risk management parameters"""
        rec = decision['recommendation']
        if rec == "BUY":
            entry = price
            sl = round(price * 0.99, 2) # Tight SL
            tp = round(price * 1.03, 2) # 1:3 RR roughly
            return {
                "entry_zone": f"{round(entry*0.999, 2)} - {round(entry*1.001, 2)}",
                "stop_loss": sl,
                "take_profit": tp,
                "risk_reward_ratio": 3.0, "position_size": "2%", "risk_level": "Medium"
            }
        elif rec == "SELL":
            entry = price
            sl = round(price * 1.01, 2)
            tp = round(price * 0.97, 2)
            return {
                "entry_zone": f"{round(entry*0.999, 2)} - {round(entry*1.001, 2)}",
                "stop_loss": sl,
                "take_profit": tp,
                "risk_reward_ratio": 3.0, "position_size": "2%", "risk_level": "Medium"
            }
        return {"entry_zone": "N/A", "stop_loss": None, "take_profit": None, "risk_reward_ratio": None, "position_size": "0%", "risk_level": "N/A"}
