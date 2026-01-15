from flask import Blueprint, request, jsonify
from backend.services.challenge_service import ChallengeService
from backend.models import UserChallenge

challenge_bp = Blueprint('challenge', __name__)

@challenge_bp.route('/', methods=['POST'])
def create_challenge_endpoint(tenant):
    # Triggered after payment
    data = request.json
    # Mock user fetching
    # challenge = ChallengeService.create_challenge(user, data['plan'])
    return jsonify({"message": "Challenge created", "id": 1}), 201

@challenge_bp.route('/<int:id>', methods=['GET'])
def get_challenge(tenant, id):
    challenge = UserChallenge.query.get(id)
    if not challenge:
        return jsonify({"error": "Not found"}), 404
        
    return jsonify({
        "id": challenge.id,
        "balance": challenge.current_equity,
        "status": challenge.status,
        "target": challenge.profit_target,
        "drawdown": challenge.max_drawdown
    })
