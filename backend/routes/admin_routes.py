from flask import Blueprint, jsonify

admin_bp = Blueprint('admin', __name__)

@admin_bp.route('/users', methods=['GET'])
def list_users(tenant):
    return jsonify([])

@admin_bp.route('/settings', methods=['PUT'])
def update_settings(tenant):
    return jsonify({"message": "Settings updated"})
