"""
AI Analysis Routes - Trading Analysis API
"""
from flask import Blueprint, jsonify, request
from services.ai_analysis_service import AIAnalysisService

ai_analysis_bp = Blueprint('ai_analysis', __name__)
analysis_service = AIAnalysisService()


@ai_analysis_bp.route('/analyze', methods=['POST'])
def analyze_symbol(tenant):
    """
    Analyze a trading symbol and provide AI-powered recommendation
    
    Request Body:
        {
            "symbol": "EURUSD",
            "timeframe": "1D"  # optional: scalp, day, swing
        }
    
    Returns:
        Complete AI analysis with BUY/SELL/WAIT recommendation
    """
    data = request.get_json() or {}
    symbol = data.get('symbol', 'EURUSD')
    timeframe = data.get('timeframe', '1D')
    
    try:
        analysis = analysis_service.analyze_symbol(symbol, timeframe)
        return jsonify(analysis), 200
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Failed to analyze symbol"
        }), 500


@ai_analysis_bp.route('/quick-signal/<symbol>', methods=['GET'])
def quick_signal(tenant, symbol):
    """
    Get quick trading signal for a symbol
    
    Returns:
        Simplified recommendation (BUY/SELL/WAIT) with confidence
    """
    try:
        analysis = analysis_service.analyze_symbol(symbol)
        decision = analysis['analysis']['decision']
        
        return jsonify({
            "symbol": symbol,
            "signal": decision['recommendation'],
            "confidence": decision['confidence'],
            "price": analysis['current_price'],
            "mode": "DEMO"
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "Failed to get signal"
        }), 500
