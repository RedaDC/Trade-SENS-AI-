from datetime import datetime, timedelta
import random

class AIAnalyst:
    def __init__(self, tenant_id):
        self.tenant_id = tenant_id

    def classify_news(self, news_items):
        # Mock logic: In a real app, this would use NLP or specific keywords
        # For now, we simulate classification based on keywords in mock data
        impact_score = 0
        sentiment = "NEUTRAL"
        
        for item in news_items:
            if item.impact == 'HIGH':
                impact_score += 2
            elif item.impact == 'MEDIUM':
                impact_score += 1
                
        if impact_score > 3:
            sentiment = "HIGH_VOLATILITY"
        
        return sentiment

    def detect_regime(self):
        # Mock Regime Detection
        regimes = [
            "Risk-On / Trending",
            "Risk-Off / High-Volatility",
            "Range-bound / Low-Volatility",
            "Neutral / Consolidation"
        ]
        return random.choice(regimes)

    def generate_trade_idea(self, symbol="EURUSD"):
        # 1. Analyze Market Regime
        regime = self.detect_regime()
        
        # 2. Simulate Technical Analysis (Mock)
        bias = random.choice(["LONG", "SHORT"])
        current_price = 1.0850 if symbol == "EURUSD" else 150.00
        
        # 3. Construct Trade Setup
        if bias == "LONG":
            entry = current_price
            stop_loss = current_price - 0.0030 # 30 pips SL
            take_profit_1 = current_price + 0.0040 # 40 pips
            take_profit_2 = current_price + 0.0080 # 80 pips
            explanation = "Price rejected key support level with strong volume confirmation. Momentum indicators crossing upward."
        else:
            entry = current_price
            stop_loss = current_price + 0.0030
            take_profit_1 = current_price - 0.0040
            take_profit_2 = current_price - 0.0080
            explanation = "Failed to break resistance at key level. Bearish divergence observed on RSI."

        return {
            "market_summary": f"Market is currently in a {regime} mode. Focus on {bias} setups.",
            "regime": regime,
            "news_driver": "Upcoming Central Bank decision causing pre-event positioning.",
            "trade_setup": {
                "asset": symbol,
                "bias": bias,
                "entry": entry,
                "stop_loss": stop_loss,
                "take_profit": [take_profit_1, take_profit_2],
                "rr_ratio": 1.5,
                "confidence": "85%", # Just a string for display
                "duration": "Intraday"
            },
            "risk_assessment": "Moderate risk. Volatility expected to increase during NY session. Stick to 1% risk per trade.",
            "entry_logic": explanation
        }

    def get_latest_analysis(self):
        # In a real scenario, this would aggregate data from DB price_data and news_events
        return self.generate_trade_idea()
