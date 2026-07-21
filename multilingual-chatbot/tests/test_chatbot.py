import unittest
from unittest.mock import MagicMock, patch
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chatbot.language_detector import LanguageDetector
from chatbot.context_manager import ContextManager

class TestChatbotCore(unittest.TestCase):
    
    def setUp(self):
        self.detector = LanguageDetector()
        self.context = ContextManager(session_timeout_minutes=10)
        
    def test_language_detection_english(self):
        # Test basic English detection
        lang = self.detector.detect_language("Hello, how are you today?")
        self.assertEqual(lang, "en")
        
    def test_language_detection_hindi_script(self):
        # Test Hindi Devanagari detection
        lang = self.detector.detect_language("नमस्ते, आप कैसे हैं?")
        self.assertEqual(lang, "hi")
        
    def test_language_detection_kannada_script(self):
        # Test Kannada script detection
        lang = self.detector.detect_language("ನಮಸ್ಕಾರ, ಹೇಗಿದ್ದೀರಾ?")
        self.assertEqual(lang, "kn")
        
    def test_context_manager_session_creation(self):
        # Test session creation
        session_id = "test_user_123"
        session = self.context.get_session(session_id)
        
        self.assertIn('history', session)
        self.assertIn('context', session)
        self.assertEqual(len(session['history']), 0)
        
    def test_context_manager_interaction_add(self):
        session_id = "test_user_456"
        self.context.add_interaction(
            session_id=session_id,
            user_message="Hello",
            intent="greeting",
            response="Hi there!",
            language="en"
        )
        
        session = self.context.get_session(session_id)
        self.assertEqual(len(session['history']), 1)
        self.assertEqual(session['history'][0]['intent'], "greeting")
        self.assertEqual(session['preferred_language'], "en")

if __name__ == '__main__':
    unittest.main()
