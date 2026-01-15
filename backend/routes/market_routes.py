from flask import Blueprint, request, jsonify
from backend.services.market_data_service import MarketDataFactory
from backend.models import TenantSettings

market_bp = Blueprint('market', __name__)

@market_bp.route('/last', methods=['GET'])
def get_last_price(tenant):
    symbol = request.args.get('symbol')
    
    # Get tenant provider settings
    # For now assuming defaults or fetching from DB
    provider = MarketDataFactory.get_provider()
    price = provider.get_last_price(symbol)
    
    return jsonify({"symbol": symbol, "price": price})

@market_bp.route('/ohlcv', methods=['GET'])
def get_ohlcv(tenant):
    symbol = request.args.get('symbol')
    timeframe = request.args.get('timeframe', '1d')
    limit = int(request.args.get('limit', 100))
    
    provider = MarketDataFactory.get_provider()
    data = provider.get_ohlcv(symbol, timeframe, limit)
    return jsonify(data)
