from flask import Blueprint, request, jsonify
from services.market_data_service import MarketDataFactory
from models import TenantSettings

market_bp = Blueprint('market', __name__)

@market_bp.route('/last', methods=['GET'])
def get_last_price(tenant):
    symbol = request.args.get('symbol')
    
    # Get tenant provider settings
    try:
        provider = MarketDataFactory.get_provider()
        price = provider.get_last_price(symbol)
    except Exception as e:
        print(f"Primary provider failed for {symbol}: {e}. Falling back to mock.")
        provider = MarketDataFactory.get_fallback_provider()
        price = provider.get_last_price(symbol)
    
    return jsonify({"symbol": symbol, "price": price})

@market_bp.route('/ohlcv', methods=['GET'])
def get_ohlcv(tenant):
    symbol = request.args.get('symbol')
    timeframe = request.args.get('timeframe', '1d')
    limit = int(request.args.get('limit', 100))
    
    try:
        provider = MarketDataFactory.get_provider()
        data = provider.get_ohlcv(symbol, timeframe, limit)
    except Exception as e:
        print(f"Primary provider failed for {symbol} OHLCV: {e}. Falling back to mock.")
        provider = MarketDataFactory.get_fallback_provider()
        data = provider.get_ohlcv(symbol, timeframe, limit)
        
    return jsonify(data)
