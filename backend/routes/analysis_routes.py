from flask import Blueprint, jsonify
from services.ai_analyst import AIAnalyst

market_bp_analysis = Blueprint('market_analysis', __name__)

@market_bp_analysis.route('/latest', methods=['GET'])
def get_latest_analysis(tenant):
    analyst = AIAnalyst(tenant_id=1) # Mock tenant
    report = analyst.get_latest_analysis()
    return jsonify(report)
