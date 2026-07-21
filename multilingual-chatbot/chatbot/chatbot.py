"""
Core chatbot logic orchestrating models, processing, and responses.
"""

import os
import sys
import pickle
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.config import Config
from config.languages import SUPPORTED_LANGUAGES
from chatbot.language_detector import LanguageDetector
from chatbot.preprocessor import TextPreprocessor
from chatbot.context_manager import ContextManager
from chatbot.response_generator import ResponseGenerator

class MultilingualChatbot:
    def __init__(self):
        self.language_detector = LanguageDetector()
        self.context_manager = ContextManager()
        self.response_generator = ResponseGenerator()
        
        # Cache for loaded models and artifacts per language
        self.models = {}
        self.artifacts = {}
        self.preprocessors = {}
        
        self._load_available_models()
        
    def _load_available_models(self):
        """Pre-load all available language models into memory."""
        print("Initializing Multilingual Chatbot...")
        for lang_code in SUPPORTED_LANGUAGES.keys():
            model_path = os.path.join(Config.MODEL_DIR, f"{lang_code}_model.h5")
            artifacts_path = os.path.join(Config.MODEL_DIR, f"{lang_code}_artifacts.pkl")
            
            if os.path.exists(model_path) and os.path.exists(artifacts_path):
                try:
                    # Load model
                    self.models[lang_code] = tf.keras.models.load_model(model_path)
                    
                    # Load artifacts
                    with open(artifacts_path, 'rb') as f:
                        self.artifacts[lang_code] = pickle.load(f)
                        
                    # Initialize preprocessor
                    self.preprocessors[lang_code] = TextPreprocessor(lang_code)
                    
                    print(f"✅ Loaded model for {SUPPORTED_LANGUAGES[lang_code]['name']} ({lang_code})")
                except Exception as e:
                    print(f"❌ Failed to load model for {lang_code}: {e}")
            else:
                print(f"⚠️ Model files missing for {lang_code}. Needs training.")
                
    def _predict_intent(self, text, lang_code):
        """Predict intent using the appropriate language model."""
        if lang_code not in self.models:
            return 'fallback', 0.0
            
        model = self.models[lang_code]
        artifacts = self.artifacts[lang_code]
        preprocessor = self.preprocessors[lang_code]
        
        tokenizer = artifacts['tokenizer']
        label_encoder = artifacts['label_encoder']
        max_len = artifacts['max_sequence_length']
        
        # Preprocess text
        clean_text = preprocessor.clean_text(text)
        
        # Tokenize and pad
        sequence = tokenizer.texts_to_sequences([clean_text])
        padded = pad_sequences(sequence, maxlen=max_len, padding='post')
        
        # Predict
        predictions = model.predict(padded, verbose=0)[0]
        
        # Get highest probability intent
        best_idx = np.argmax(predictions)
        confidence = float(predictions[best_idx])
        
        if confidence < Config.CONFIDENCE_THRESHOLD:
            return 'fallback', confidence
            
        intent = label_encoder.inverse_transform([best_idx])[0]
        return intent, confidence
        
    def process_message(self, message, session_id, forced_language=None):
        """
        Process a user message and return a response.
        """
        if not message or not message.strip():
            return {
                "response": "Please say something!",
                "intent": "unknown",
                "language": "en",
                "confidence": 0.0
            }
            
        session = self.context_manager.get_session(session_id)
        
        # 1. Detect Language
        if forced_language and forced_language in SUPPORTED_LANGUAGES:
            lang_code = forced_language
        else:
            # Check if user explicitly asked to switch language in English
            lower_msg = message.lower()
            if "switch to hindi" in lower_msg or "talk in hindi" in lower_msg:
                lang_code = 'hi'
            elif "switch to kannada" in lower_msg or "talk in kannada" in lower_msg:
                lang_code = 'kn'
            elif "switch to english" in lower_msg or "talk in english" in lower_msg:
                lang_code = 'en'
            else:
                # Auto-detect based on text
                detected_lang = self.language_detector.detect_language(message)
                # Fallback to session preferred language if detection fails or models missing
                if detected_lang in self.models:
                    lang_code = detected_lang
                else:
                    lang_code = session.get('preferred_language', 'en')
                    
        # Ensure we have a model for the language
        if lang_code not in self.models:
            return {
                "response": f"Sorry, the {SUPPORTED_LANGUAGES.get(lang_code, {}).get('name', lang_code)} model is not trained yet.",
                "intent": "error",
                "language": lang_code,
                "language_name": SUPPORTED_LANGUAGES.get(lang_code, {}).get('name', 'Unknown'),
                "confidence": 0.0
            }
            
        # 2. Predict Intent
        intent, confidence = self._predict_intent(message, lang_code)
        
        # Handle explicit language switch intents
        if intent.startswith('language_switch_'):
            new_lang = intent.split('_')[-1]
            if new_lang in ['hindi']: lang_code = 'hi'
            elif new_lang in ['kannada']: lang_code = 'kn'
            elif new_lang in ['english']: lang_code = 'en'
            
        # 3. Generate Response
        intents_metadata = self.artifacts[lang_code]['intents_metadata']
        response_text = self.response_generator.get_response(
            intent_tag=intent,
            intents_metadata=intents_metadata,
            context=session['context']
        )
        
        # 4. Update Context
        self.context_manager.add_interaction(
            session_id=session_id,
            user_message=message,
            intent=intent,
            response=response_text,
            language=lang_code
        )
        
        return {
            "response": response_text,
            "intent": intent,
            "language": lang_code,
            "language_name": SUPPORTED_LANGUAGES[lang_code]['name'],
            "confidence": confidence,
            "session_id": session_id
        }
