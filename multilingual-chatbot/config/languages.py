"""
Language configurations and utilities for Multilingual Chatbot.
"""

SUPPORTED_LANGUAGES = {
    'en': {
        'code': 'en',
        'name': 'English',
        'intent_file': 'intents_english.json',
        'model_name': 'chatbot_model_en'
    },
    'hi': {
        'code': 'hi',
        'name': 'Hindi',
        'intent_file': 'intents_hindi.json',
        'model_name': 'chatbot_model_hi'
    },
    'kn': {
        'code': 'kn',
        'name': 'Kannada',
        'intent_file': 'intents_kannada.json',
        'model_name': 'chatbot_model_kn'
    }
}

# Regex patterns for script detection
SCRIPT_PATTERNS = {
    # Devanagari Unicode range
    'hi': r'[\u0900-\u097F]',
    # Kannada Unicode range
    'kn': r'[\u0C80-\u0CFF]',
    # Latin/Basic English (used as fallback or for romanized scripts)
    'en': r'[a-zA-Z]'
}

def get_language_config(lang_code):
    return SUPPORTED_LANGUAGES.get(lang_code, SUPPORTED_LANGUAGES['en'])

def get_intent_file(lang_code):
    return get_language_config(lang_code)['intent_file']
