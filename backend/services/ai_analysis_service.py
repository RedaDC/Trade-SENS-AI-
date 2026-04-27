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
        price = self._get_simulated_price(symbol)
        news_analysis = self._analyze_news(symbol)
        technical = self._analyze_technical_indicators(symbol, price)
        
        if self.mode == "REAL":
            try:
                return self._call_llm_analysis(symbol, timeframe, price, technical, news_analysis)
            except Exception as e:
                print(f"LLM Analysis failed: {e}. Falling back to DEMO.")
        
        return self._get_simulated_analysis(symbol, timeframe, price, news_analysis, technical)

    def _call_llm_analysis(self, symbol, timeframe, price, technical, news) -> Dict[str, Any]:
        """Call OpenAI GPT-4o to generate analysis"""
        system_prompt = "You are an expert institutional trading AI. You provide data-driven trading analysis, strict risk management, and clear execution signals."
        user_prompt = f"""
        Analyze {symbol} (Price: {price}) on {timeframe} timeframe.
        Technical Data: {json.dumps(technical, indent=2)}
        News Context: {json.dumps(news, indent=2)}
        Task: 1. Determine Market Structure. 2. Analyze Sentiment. 3. Evaluate Scenarios. 4. Make DECISION. 5. Provide Risk Management.
        Output strictly valid JSON.
        """
        response = self.client.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "system", "content": system_prompt}, {"role": "user", "content": user_prompt}],
            response_format={"type": "json_object"},
            temperature=0.3
        )
        data = json.loads(response.choices[0].message.content)
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
        # 1. Check for real data from our OPCVM scripts
        opcvm_data = None
        if symbol.startswith('OPCVM_'):
            try:
                import pandas as pd
                if os.path.exists('opcvm_enriched.csv'):
                    df = pd.read_csv('opcvm_enriched.csv')
                    # Search for symbol name or part of it in the CSV
                    # Note: Our CSV uses 'nom_fonds', let's assume symbol 'OPCVM_CDG_MONETAIRE' maps to 'CDG MONETAIRE'
                    search_name = symbol.replace('OPCVM_', '').replace('_', ' ')
                    match = df[df['nom_fonds'].str.contains(search_name, case=False, na=False)]
                    if not match.empty:
                        opcvm_data = match.iloc[0].to_dict()
                        print(f"Using REAL sentiment data for {symbol} from opcvm_enriched.csv")
            except Exception as e:
                print(f"Error loading OPCVM data: {e}")

        # 2. Determine Trend (Use sentiment if available)
        if opcvm_data:
            sent_score = opcvm_data.get('score_sentiment_moyen_jour', 0)
            if sent_score > 0.2: trend_direction = "Bullish"
            elif sent_score < -0.2: trend_direction = "Bearish"
            else: trend_direction = "Range"
        else:
            trend_direction = random.choices(["Bullish", "Bearish", "Range"], weights=[40, 40, 20])[0]
        
        # 3. Generate Coherent Analysis
        technical = self._generate_coherent_technicals(trend_direction, price)
        market_structure = self._generate_coherent_structure(trend_direction, price)
        sentiment = self._generate_coherent_sentiment(trend_direction)
        
        # Override sentiment if we have real data
        if opcvm_data:
            sentiment['fear_greed_index'] = int(50 + (opcvm_data['score_sentiment_moyen_jour'] * 40))
            sentiment['sentiment_label'] = "Bullish" if sent_score > 0 else "Bearish"
            sentiment['environment'] = "Macro Positive (Morocco)" if sent_score > 0 else "Macro Cautious (Morocco)"

        scenarios = self._evaluate_coherent_scenarios(trend_direction, price)
        decision = self._make_coherent_decision(trend_direction, scenarios, symbol=symbol)
        
        # Integrate news from the CSV if available
        news_data = self._generate_coherent_news(trend_direction, symbol)
        if opcvm_data and opcvm_data.get('nb_actus_jour', 0) > 0:
            news_data['key_events'] = [f"Sentiment Presse: {opcvm_data['score_sentiment_moyen_jour']:.2f}", f"Volume Actu: {int(opcvm_data['nb_actus_jour'])} articles"]
            news_data['description'] = f"Analyse basée sur les flux récents (Flux Net: {opcvm_data.get('flux_net', 0):.2f} MDH) et l'actualité marocaine."

        risk_management = self._calculate_risk_management(decision, price)
        
        return {
            "symbol": symbol,
            "timeframe": timeframe,
            "current_price": price,
            "timestamp": datetime.now().isoformat(),
            "mode": "Hybrid IA (Real Sentiment + Sim)" if opcvm_data else "Simulated Professional (Demo)",
            "analysis": {
                "news_macro": news_data,
                "market_structure": market_structure,
                "technical": technical,
                "sentiment": sentiment,
                "scenarios": scenarios,
                "decision": decision,
                "risk_management": risk_management
            }
        }

    def _generate_coherent_technicals(self, trend, price):
        if trend == "Bullish":
            rsi = random.randint(55, 75)
            macd_val = round(random.uniform(0.1, 0.5), 3)
            ema_align = "Bullish"
        elif trend == "Bearish":
            rsi = random.randint(25, 45)
            macd_val = round(random.uniform(-0.5, -0.1), 3)
            ema_align = "Bearish"
        else:
            rsi = random.randint(45, 55)
            macd_val = round(random.uniform(-0.05, 0.05), 3)
            ema_align = "Mixed"
        return {
            "rsi": {"value": rsi, "signal": "Normal", "period": 14},
            "macd": {"value": macd_val, "signal": trend, "histogram": "Positive" if macd_val > 0 else "Negative"},
            "ema": {"alignment": ema_align},
            "volume": {"trend": "Stable"}
        }

    def _generate_coherent_structure(self, trend, price):
        return {
            "trend": trend,
            "trend_strength": "High" if trend != "Range" else "Low",
            "support_level": round(price * 0.98, 2),
            "resistance_level": round(price * 1.02, 2)
        }

    def _generate_coherent_sentiment(self, trend):
        return {
            "environment": "Risk-On" if trend == "Bullish" else "Risk-Off",
            "fear_greed_index": random.randint(40, 80) if trend == "Bullish" else random.randint(20, 50),
            "sentiment_label": trend,
            "positioning": f"Biased {trend}"
        }

    def _get_simulated_price(self, symbol: str) -> float:
        base_prices = {"EURUSD": 1.0950, "GBPUSD": 1.2750, "USDJPY": 148.50, "BTCUSD": 45000.00}
        if symbol.startswith('OPCVM_'):
            base = 1000.0 + (sum(ord(c) for c in symbol) % 500) * 10
            return round(base + (random.random() - 0.5) * (base * 0.005), 2)
        base = base_prices.get(symbol, 100.0)
        return round(base + (random.random() - 0.5) * (base * 0.02), 2)

    def _evaluate_coherent_scenarios(self, trend, price) -> Dict[str, Any]:
        p_bull = 70 if trend == "Bullish" else 15 if trend == "Bearish" else 40
        p_bear = 15 if trend == "Bullish" else 70 if trend == "Bearish" else 40
        return {
            "bullish": {"probability": p_bull, "case": "Trend continuation", "target": round(price * 1.05, 2)},
            "bearish": {"probability": p_bear, "case": "Reversal", "target": round(price * 0.95, 2)},
            "wait": {"probability": 100 - p_bull - p_bear, "case": "Range", "reason": "No catalyst"}
        }

    def _generate_coherent_news(self, trend, symbol):
        is_opcvm = symbol.startswith('OPCVM_')
        if is_opcvm:
            headlines = ["BAM Taux directeur inchangé", "Flux positifs sur les fonds monétaires", "Croissance du PIB marocain"]
        else:
            headlines = ["Fed meeting news", "Earnings report beat", "Market sentiment positive"]
        return {
            "impact": trend,
            "key_events": random.sample(headlines, 2),
            "description": f"Perspectives {trend} basées sur les news.",
            "overreaction_risk": "Low"
        }

    def _make_coherent_decision(self, trend, scenarios, symbol=None):
        is_opcvm = symbol and symbol.startswith('OPCVM_')
        rec = "BUY" if trend == "Bullish" else "SELL" if trend == "Bearish" else "WAIT"
        conf = scenarios["bullish"]["probability"] if rec == "BUY" else scenarios["bearish"]["probability"] if rec == "SELL" else scenarios["wait"]["probability"]
        reason = "Structure haussière détectée sur les OPCVM." if is_opcvm and rec == "BUY" else "Attente de signaux clairs."
        return {"recommendation": rec, "confidence": conf, "reasoning": reason}

    def _analyze_news(self, symbol): return {}
    def _analyze_technical_indicators(self, symbol, price): return {}
    def _calculate_risk_management(self, decision, price):
        rec = decision['recommendation']
        if rec == "BUY":
            return {"entry_zone": str(price), "stop_loss": round(price * 0.98, 2), "take_profit": round(price * 1.05, 2), "risk_level": "Low"}
        return {"entry_zone": "N/A", "stop_loss": None, "take_profit": None, "risk_level": "N/A"}
