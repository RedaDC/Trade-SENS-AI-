"""
AI Chat Service - Elite Trading Mentor
Provides conversational AI assistance and market analysis
"""
from services.ai_analysis_service import AIAnalysisService
import random

class AIChatService:
    def __init__(self):
        self.analysis_service = AIAnalysisService()

    def get_response(self, message: str, context: dict = None) -> dict:
        symbol = context.get('symbol', 'EURUSD') if context else 'EURUSD'
        message_lower = message.lower().strip()
        
        # === GREETINGS & CASUAL CONVERSATION ===
        greetings = ['hello', 'hi', 'hey', 'greetings', 'good morning', 'good afternoon', 'good evening', 'sup', 'yo']
        if any(greeting in message_lower for greeting in greetings):
            responses = [
                f"👋 **Hello, Trader!** I'm your Elite AI Mentor. Currently tracking **{symbol}**. How can I assist you today?",
                f"🎯 **Hey there!** Ready to dominate the markets? I'm monitoring **{symbol}** for you. What would you like to know?",
                f"💎 **Greetings!** Your institutional-grade analysis is ready. Watching **{symbol}** closely. Ask me anything!",
                f"⚡ **Welcome back!** Let's make some smart moves. I'm analyzing **{symbol}** right now. What's on your mind?"
            ]
            return {"type": "text", "message": random.choice(responses)}
        
        # === FAREWELLS ===
        farewells = ['bye', 'goodbye', 'see you', 'later', 'thanks', 'thank you']
        if any(farewell in message_lower for farewell in farewells):
            responses = [
                "📈 **Trade smart, trade safe!** I'll be here when you need me. Good luck out there!",
                "💰 **May the pips be with you!** Come back anytime for more insights.",
                "🚀 **Happy trading!** Remember: discipline beats emotion every time.",
                "✨ **Until next time!** Keep those stop losses tight and profits running!"
            ]
            return {"type": "text", "message": random.choice(responses)}
        
        # === HOW ARE YOU / ABOUT YOU ===
        if any(phrase in message_lower for phrase in ['how are you', 'how do you do', 'what are you', 'who are you', 'tell me about yourself']):
            return {
                "type": "text",
                "message": "🤖 I'm your **Elite Trading Mentor** — powered by institutional-grade algorithms and real-time market intelligence.\n\n"
                           "I analyze **technical indicators**, **market structure**, and **sentiment** to give you high-probability trade setups.\n\n"
                           f"Right now, I'm laser-focused on **{symbol}**. Ask me for analysis, trends, or my opinion on any asset!"
            }
        
        # === HELP / CAPABILITIES ===
        if any(word in message_lower for word in ['help', 'what can you do', 'capabilities', 'commands']):
            return {
                "type": "text",
                "message": "💡 **Here's what I can do for you:**\n\n"
                           "### 📊 Market Analysis\n"
                           "- *\"Analyze AAPL\"* — Full technical breakdown\n"
                           "- *\"What's the trend for EURUSD?\"* — Trend analysis\n"
                           "- *\"Give me your opinion on TSLA\"* — AI recommendation\n\n"
                           "### 🎯 Trade Signals\n"
                           "- *\"Should I buy BTCUSD?\"* — Entry/exit zones with risk management\n"
                           "- *\"What do you think about GOLD?\"* — Market sentiment\n\n"
                           "### 💬 Casual Chat\n"
                           "- Just say hi, ask how I'm doing, or chat about the markets!\n\n"
                           f"Currently monitoring: **{symbol}** 🔍"
            }
        
        # === TECHNICAL ANALYSIS REQUEST ===
        analysis_keywords = ['analyze', 'analysis', 'opinion', 'think', 'trend', 'signal', 'recommendation', 
                             'should i buy', 'should i sell', 'what should i do', 'trade', 'entry', 'exit']
        if any(keyword in message_lower for keyword in analysis_keywords):
            # Get full analysis data
            full_analysis = self.analysis_service.analyze_symbol(symbol)
            analysis_data = full_analysis.get('analysis', {})
            
            # Construct meaningful text summary
            decision = analysis_data.get('decision', {})
            rec = decision.get('recommendation', 'WAIT')
            conf = decision.get('confidence', 0)
            reasoning = decision.get('reasoning', 'No clear signal at the moment.')
            
            summary_text = f"### 🎯 Elite Analysis: **{symbol}**\n\n**Signal:** {rec} ({conf}% confidence)\n\n{reasoning}"

            return {
                "type": "analysis",
                "message": summary_text,
                "data": analysis_data
            }
        
        # === GENERAL STOCK/MARKET QUESTIONS ===
        if any(word in message_lower for word in ['stock', 'market', 'forex', 'crypto', 'trading', 'price']):
            return {
                "type": "text",
                "message": f"📈 **Great question!** I specialize in technical analysis and trade signals.\n\n"
                           f"I'm currently tracking **{symbol}**, but I can analyze any asset you're interested in.\n\n"
                           "Try asking:\n"
                           "- *\"What's your opinion on AAPL?\"*\n"
                           "- *\"Analyze BTCUSD\"*\n"
                           "- *\"Should I buy EURUSD?\"*"
            }
        
        # === FALLBACK: FRIENDLY REDIRECT ===
        return {
            "type": "text",
            "message": f"🤔 I'm not quite sure what you mean, but I'm here to help!\n\n"
                       f"I'm currently monitoring **{symbol}**. You can ask me:\n"
                       "- For a **technical analysis**\n"
                       "- My **opinion** on a stock or forex pair\n"
                       "- About market **trends** and **signals**\n\n"
                       "Or just say **'help'** to see what I can do! 💡"
        }
