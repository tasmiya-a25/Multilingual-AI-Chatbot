"""
Flask API Routes for the Multilingual Chatbot.
"""

from flask import Blueprint, request, jsonify, render_template
from api.middleware import rate_limit
import uuid

def create_routes(chatbot_instance):
    routes = Blueprint('routes', __name__)
    
    @routes.route('/')
    def index():
        """Render the main chat UI."""
        return render_template('index.html')
        
    @routes.route('/api/session/new', methods=['GET'])
    @rate_limit(limit=30, per=60)
    def new_session():
        """Create a new session ID for a user."""
        session_id = str(uuid.uuid4())
        return jsonify({
            "session_id": session_id,
            "message": "New session created successfully."
        })
        
    @routes.route('/api/chat', methods=['POST'])
    @rate_limit(limit=60, per=60)
    def chat():
        """Process a message and return the chatbot's response."""
        data = request.get_json()
        
        if not data or 'message' not in data:
            return jsonify({"error": "Missing 'message' in request body"}), 400
            
        message = data['message']
        session_id = data.get('session_id', str(uuid.uuid4()))
        forced_language = data.get('language')
        
        try:
            result = chatbot_instance.process_message(
                message=message,
                session_id=session_id,
                forced_language=forced_language
            )
            return jsonify(result)
        except Exception as e:
            return jsonify({"error": f"Internal server error: {str(e)}"}), 500
            
    @routes.route('/api/language/detect', methods=['POST'])
    def detect_language():
        """Detect the language of the provided text."""
        data = request.get_json()
        if not data or 'text' not in data:
            return jsonify({"error": "Missing 'text' in request body"}), 400
            
        lang = chatbot_instance.language_detector.detect_language(data['text'])
        from config.languages import SUPPORTED_LANGUAGES
        
        return jsonify({
            "detected_language": lang,
            "language_name": SUPPORTED_LANGUAGES.get(lang, {}).get('name', 'Unknown')
        })
        
    @routes.route('/api/session/<session_id>/history', methods=['GET'])
    def get_history(session_id):
        """Retrieve conversation history for a session."""
        session = chatbot_instance.context_manager.get_session(session_id)
        return jsonify({
            "session_id": session_id,
            "history": session['history']
        })
        
    @routes.route('/api/session/<session_id>/clear', methods=['POST'])
    def clear_session(session_id):
        """Clear conversation history for a session."""
        chatbot_instance.context_manager.clear_session(session_id)
        return jsonify({"status": "success", "message": "Session history cleared."})
        
    @routes.route('/api/model/info', methods=['GET'])
    def get_model_info():
        """Get information about loaded models."""
        from config.languages import SUPPORTED_LANGUAGES
        
        info = []
        for lang, model in chatbot_instance.models.items():
            artifacts = chatbot_instance.artifacts[lang]
            info.append({
                "language_code": lang,
                "language_name": SUPPORTED_LANGUAGES[lang]['name'],
                "intents_count": len(artifacts['label_encoder'].classes_),
                "vocab_size": len(artifacts['tokenizer'].word_index) + 1,
                "max_sequence_length": artifacts['max_sequence_length']
            })
            
        return jsonify({"models_loaded": len(info), "details": info})
        
    @routes.route('/api/health', methods=['GET'])
    def health_check():
        """Health check endpoint."""
        return jsonify({
            "status": "healthy",
            "models_loaded": list(chatbot_instance.models.keys())
        })
        
    return routes
