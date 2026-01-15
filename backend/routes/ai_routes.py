"""
AI Chat Routes - Financial Chatbot API
"""
from flask import Blueprint, jsonify, request
from backend.services.chat_service import AIChatService

ai_bp = Blueprint('ai', __name__)
chat_service = AIChatService()

@ai_bp.route('/chat', methods=['POST'])
def chat(tenant):
    data = request.get_json() or {}
    message = data.get('message', '')
    context = data.get('context', {})
    
    if not message:
        return jsonify({"error": "No message provided"}), 400
        
    try:
        response = chat_service.get_response(message, context)
        return jsonify({
            "response": response,
            "status": "success"
        }), 200
    except Exception as e:
        return jsonify({
            "error": str(e),
            "message": "AI failed to respond"
        }), 500
