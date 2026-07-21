"""
Context manager for tracking conversation history and maintaining context.
"""

from datetime import datetime, timedelta

class ContextManager:
    def __init__(self, session_timeout_minutes=30):
        # Stores session data: {session_id: {'history': [...], 'last_active': datetime, 'context': {}}}
        self.sessions = {}
        self.session_timeout = timedelta(minutes=session_timeout_minutes)
        
    def _cleanup_old_sessions(self):
        """Remove sessions that have expired."""
        now = datetime.now()
        expired_sessions = [
            sid for sid, data in self.sessions.items()
            if now - data['last_active'] > self.session_timeout
        ]
        for sid in expired_sessions:
            del self.sessions[sid]
            
    def get_session(self, session_id):
        """Get or create a session."""
        self._cleanup_old_sessions()
        
        if session_id not in self.sessions:
            self.sessions[session_id] = {
                'history': [],
                'context': {},
                'last_active': datetime.now(),
                'preferred_language': 'en'
            }
        else:
            self.sessions[session_id]['last_active'] = datetime.now()
            
        return self.sessions[session_id]
        
    def add_interaction(self, session_id, user_message, intent, response, language):
        """Add a turn to the conversation history."""
        session = self.get_session(session_id)
        
        interaction = {
            'timestamp': datetime.now().isoformat(),
            'user_message': user_message,
            'intent': intent,
            'response': response,
            'language': language
        }
        
        session['history'].append(interaction)
        session['preferred_language'] = language
        
        # Limit history size to prevent memory issues
        if len(session['history']) > 50:
            session['history'] = session['history'][-50:]
            
    def set_context_variable(self, session_id, key, value):
        """Store a variable in the context (e.g., user name)."""
        session = self.get_session(session_id)
        session['context'][key] = value
        
    def get_context_variable(self, session_id, key, default=None):
        """Retrieve a variable from the context."""
        session = self.get_session(session_id)
        return session['context'].get(key, default)
        
    def clear_session(self, session_id):
        """Clear history for a specific session."""
        if session_id in self.sessions:
            self.sessions[session_id]['history'] = []
            self.sessions[session_id]['context'] = {}
