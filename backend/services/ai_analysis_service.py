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
        """Original Demo Logic"""
        
        # Step 2: Market Structure & Trend
        market_structure = self._analyze_market_structure(symbol, price)
        
        # Step 4: Sentiment Check
        sentiment = self._analyze_sentiment(symbol)
        
        # Step 5: Trade Scenario Evaluation
        scenarios = self._evaluate_scenarios(symbol, price, technical, sentiment)
        
        # Step 6: Final Decision
        decision = self._make_decision(scenarios, technical, market_structure)
        
        # Step 7: Risk Management
        risk_management = self._calculate_risk_management(decision, price)
        
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "current_price": price,
            "timestamp": datetime.now().isoformat(),
            "mode": "DEMO",
            "analysis": {
                "news_macro": news_analysis,
                "market_structure": market_structure,
                "technical": technical,
                "sentiment": sentiment,
                "scenarios": scenarios,
                "decision": decision,
                "risk_management": risk_management
            }
        }
    
    # --- Helper Data Generators (Used for inputs in Real Mode, logic in Demo) ---
    
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
        """Analyze news and macro events"""
        news_impacts = ["Bullish", "Bearish", "Neutral"]
        impact = random.choice(news_impacts)
        events = {
            "EURUSD": ["ECB Rate Decision", "US CPI Data", "EUR GDP Report"],
            "GBPUSD": ["BoE Meeting", "UK Employment Data", "Brexit Updates"],
            "TSLA": ["Earnings Report", "Production Numbers", "EV Market News"],
            "GOLD": ["Fed Policy Shift", "Geopolitical Tension", "Inflation Hedge Demand"],
        }
        if symbol.endswith('.MA'):
            events[symbol] = ["Morocco GDP", "Bank Al-Maghrib Decision", "CSE Index Update"]
        relevant_events = events.get(symbol, ["Market Update", "Economic Data"])
        
        return {
            "impact": impact,
            "key_events": random.sample(relevant_events, min(2, len(relevant_events))),
            "description": f"Recent {impact.lower()} news flow detected",
            "overreaction_risk": random.choice(["Low", "Medium", "High"])
        }
    
    def _analyze_technical_indicators(self, symbol: str, price: float) -> Dict[str, Any]:
        """Analyze technical indicators"""
        rsi = random.randint(30, 70)
        rsi_signal = "Oversold" if rsi < 35 else "Overbought" if rsi > 65 else "Neutral"
        macd_value = round(random.uniform(-0.5, 0.5), 3)
        macd_signal = "Bullish" if macd_value > 0 else "Bearish"
        
        ema_20 = round(price * random.uniform(0.99, 1.01), 2)
        ema_50 = round(price * random.uniform(0.98, 1.02), 2)
        ema_200 = round(price * random.uniform(0.95, 1.05), 2)
        ema_alignment = "Bullish" if ema_20 > ema_50 > ema_200 else "Bearish" if ema_20 < ema_50 < ema_200 else "Mixed"
        
        return {
            "rsi": {"value": rsi, "signal": rsi_signal, "period": 14},
            "macd": {"value": macd_value, "signal": macd_signal, "histogram": "Positive" if macd_value > 0 else "Negative"},
            "ema": {"ema_20": ema_20, "ema_50": ema_50, "ema_200": ema_200, "alignment": ema_alignment},
            "volume": {"trend": random.choice(["Increasing", "Decreasing", "Stable"])}
        }

    # --- Demo Logic Helpers ---

    def _analyze_market_structure(self, symbol: str, price: float) -> Dict[str, Any]:
        """Analyze market structure and trend"""
        trends = ["Bullish", "Bearish", "Range-bound"]
        trend = random.choice(trends)
        support = round(price * 0.98, 2)
        resistance = round(price * 1.02, 2)
        return {
            "trend": trend,
            "trend_strength": random.choice(["Strong", "Moderate", "Weak"]),
            "support_level": support,
            "resistance_level": resistance,
            "key_levels": [{"type": "Support", "price": support, "strength": "Strong"}, {"type": "Resistance", "price": resistance, "strength": "Moderate"}],
            "liquidity_zones": f"Major liquidity around {support} and {resistance}"
        }
    
    def _analyze_sentiment(self, symbol: str) -> Dict[str, Any]:
        """Analyze market sentiment"""
        fear_greed = random.randint(20, 80)
        sentiment_label = "Fear" if fear_greed < 40 else "Greed" if fear_greed > 60 else "Neutral"
        return {
            "environment": random.choice(["Risk-On", "Risk-Off", "Mixed"]),
            "fear_greed_index": fear_greed,
            "sentiment_label": sentiment_label,
            "positioning": random.choice(["Crowded Long", "Crowded Short", "Balanced"])
        }
    
    def _evaluate_scenarios(self, symbol: str, price: float, technical: Dict, sentiment: Dict) -> Dict[str, Any]:
        """Evaluate bullish, bearish, and no-trade scenarios"""
        bullish_factors = 0
        bearish_factors = 0
        
        if technical['rsi']['signal'] == "Oversold": bullish_factors += 1
        elif technical['rsi']['signal'] == "Overbought": bearish_factors += 1
        if technical['macd']['signal'] == "Bullish": bullish_factors += 1
        elif technical['macd']['signal'] == "Bearish": bearish_factors += 1
        if technical['ema']['alignment'] == "Bullish": bullish_factors += 1
        elif technical['ema']['alignment'] == "Bearish": bearish_factors += 1
        
        total = bullish_factors + bearish_factors
        if total == 0:
            bull = 33; bear = 33; wait = 34
        else:
            bull = int((bullish_factors/total)*60)+20
            bear = int((bearish_factors/total)*60)+20
            wait = 100 - bull - bear
            
        return {
            "bullish": {"probability": bull, "case": f"Price breaks above {round(price * 1.01, 2)}", "target": round(price * 1.03, 2)},
            "bearish": {"probability": bear, "case": f"Price breaks below {round(price * 0.99, 2)}", "target": round(price * 0.97, 2)},
            "wait": {"probability": wait, "case": "Conflicting signals", "reason": "Wait for confirmation"}
        }
    
    def _make_decision(self, scenarios: Dict, technical: Dict, market_structure: Dict) -> Dict[str, Any]:
        """Make final trading decision"""
        probs = {"BUY": scenarios['bullish']['probability'], "SELL": scenarios['bearish']['probability'], "WAIT": scenarios['wait']['probability']}
        rec = max(probs, key=probs.get)
        
        reasoning = ""
        if rec == "BUY":
            reasoning = f"{market_structure['trend']} trend with {technical['ema']['alignment']} EMA alignment."
        elif rec == "SELL":
            reasoning = f"{market_structure['trend']} trend with {technical['macd']['signal']} MACD signal."
        else:
            reasoning = "Mixed signals across multiple timeframes."
            
        return {"recommendation": rec, "confidence": probs[rec], "reasoning": reasoning}
    
    def _calculate_risk_management(self, decision: Dict, price: float) -> Dict[str, Any]:
        """Calculate risk management parameters"""
        rec = decision['recommendation']
        if rec == "BUY":
            return {
                "entry_zone": f"{round(price * 0.998, 2)} - {round(price * 1.002, 2)}",
                "stop_loss": round(price * 0.98, 2),
                "take_profit": round(price * 1.04, 2),
                "risk_reward_ratio": 2.0, "position_size": "1-2%", "risk_level": "Medium"
            }
        elif rec == "SELL":
            return {
                "entry_zone": f"{round(price * 0.998, 2)} - {round(price * 1.002, 2)}",
                "stop_loss": round(price * 1.02, 2),
                "take_profit": round(price * 0.96, 2),
                "risk_reward_ratio": 2.0, "position_size": "1-2%", "risk_level": "Medium"
            }
        return {"entry_zone": "N/A", "stop_loss": None, "take_profit": None, "risk_reward_ratio": None, "position_size": "0%", "risk_level": "N/A"}
