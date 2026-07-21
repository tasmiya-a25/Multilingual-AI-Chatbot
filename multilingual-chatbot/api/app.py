"""
Main Flask and Socket.IO application entry point.
"""

import os
import sys
import eventlet
eventlet.monkey_patch()

from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO, emit

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import Config
from chatbot.chatbot import MultilingualChatbot
from api.routes import create_routes

def create_app():
    """Create and configure the Flask application."""
    app = Flask(__name__, 
                template_folder='../templates',
                static_folder='../static')
                
    app.config.from_object(Config)
    CORS(app, resources={r"/api/*": {"origins": "*"}})
    
    # Initialize chatbot
    chatbot = MultilingualChatbot()
    
    # Register REST routes
    routes = create_routes(chatbot)
    app.register_blueprint(routes)
    
    # Initialize Socket.IO
    socketio = SocketIO(app, cors_allowed_origins="*", async_mode='eventlet')
    
    # Socket.IO event handlers
    @socketio.on('connect')
    def handle_connect():
        print(f"Client connected: {request.sid}")
        emit('server_message', {'data': 'Connected to LinguaBot WebSocket'})
        
    @socketio.on('disconnect')
    def handle_disconnect():
        print(f"Client disconnected: {request.sid}")
        
    @socketio.on('chat_message')
    def handle_chat_message(data):
        """Handle real-time chat messages."""
        if not data or 'message' not in data:
            return
            
        message = data['message']
        session_id = data.get('session_id', request.sid)
        forced_language = data.get('language')
        
        try:
            # Show typing indicator
            emit('typing_status', {'is_typing': True})
            
            # Allow a tiny delay to show the typing indicator visually
            eventlet.sleep(0.5)
            
            # Process message
            result = chatbot.process_message(
                message=message,
                session_id=session_id,
                forced_language=forced_language
            )
            
            # Hide typing and send response
            emit('typing_status', {'is_typing': False})
            emit('bot_response', result)
            
        except Exception as e:
            print(f"WebSocket error: {e}")
            emit('typing_status', {'is_typing': False})
            emit('error', {'message': 'An error occurred while processing your message.'})
            
    return app, socketio

if __name__ == '__main__':
    app, socketio = create_app()
    print(f"Starting server on port {Config.PORT}...")
    socketio.run(app, host=Config.HOST, port=Config.PORT, debug=Config.DEBUG)
