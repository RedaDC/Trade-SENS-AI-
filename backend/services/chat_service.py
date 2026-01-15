"""
AI Chat Service - Demo Version
Provides simulated financial advice and market information
"""
from backend.services.ai_analysis_service import AIAnalysisService

class AIChatService:
    def __init__(self):
        self.analysis_service = AIAnalysisService()

    def get_response(self, message: str, context: dict = None) -> dict:
        symbol = context.get('symbol', 'EURUSD') if context else 'EURUSD'
        
        # Determine if the user is asking for an opinion or trend
        message_lower = message.lower()
        if any(word in message_lower for word in ['opinion', 'think', 'trend', 'analysis', 'signal', 'recommendation', 'what should i do']):
            # Get full analysis data
            full_analysis = self.analysis_service.analyze_symbol(symbol)
            analysis_data = full_analysis.get('analysis', {})
            
            # Construct meaningful text summary for fallbacks
            decision = analysis_data.get('decision', {})
            rec = decision.get('recommendation', 'WAIT')
            conf = decision.get('confidence', 0)
            
            summary_text = f"My technical opinion for **{symbol}** is a **{rec}** ({conf}% confidence)."

            return {
                "type": "analysis",
                "message": summary_text,
                "data": analysis_data
            }
            
        # Fallback to general interaction
        return {
            "type": "text",
            "message": f"I'm here to help! I'm currently monitoring **{symbol}**. You can ask for my technical opinion or the current trend. 🤖"
        }
