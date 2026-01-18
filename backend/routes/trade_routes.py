from flask import Blueprint, request, jsonify
from services.challenge_service import ChallengeService
from models import Trade, UserChallenge
from extensions import db

trade_bp = Blueprint('trade', __name__)

@trade_bp.route('/', methods=['POST'])
def place_trade(tenant):
    data = request.json
    # data: challenge_id, symbol, side, volume
    
    # Mock execution
    # 1. Get Price
    # 2. Create Trade
    trade = Trade(
        tenant_id=1, # Mock
        challenge_id=data['challenge_id'],
        symbol=data['symbol'],
        side=data['side'],
        volume=data['volume'],
        entry_price=100.0, # Mock
        stop_loss=data.get('stop_loss'),
        take_profit=data.get('take_profit'),
        pnl=0.0 # Open trade
    )
    db.session.add(trade)
    db.session.commit()
    
    return jsonify({"message": "Trade executed", "trade_id": trade.id}), 201
