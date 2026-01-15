from flask import Blueprint, jsonify

leaderboard_bp = Blueprint('leaderboard', __name__)

@leaderboard_bp.route('/', methods=['GET'])
def get_leaderboard(tenant):
    # logic to aggregate UserChallenges and sort by profit
    return jsonify([
        {"rank": 1, "user": "TraderX", "profit": "15%"},
        {"rank": 2, "user": "AlphaWolf", "profit": "12%"}
    ])
