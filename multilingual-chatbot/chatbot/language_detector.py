"""
Language detection module for classifying input language.
"""

import re
from langdetect import detect, DetectorFactory
from langdetect.lang_detect_exception import LangDetectException

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config.languages import SCRIPT_PATTERNS

# Ensure consistent results from langdetect
DetectorFactory.seed = 0

class LanguageDetector:
    def __init__(self):
        pass
        
    def detect_language(self, text):
        """
        Detect the language of the given text using script analysis and langdetect.
        
        Args:
            text: Input string
            
        Returns:
            Language code ('en', 'hi', 'kn') or 'en' as fallback.
        """
        if not text or not text.strip():
            return 'en'
            
        # 1. Script-based detection (fast and accurate for native scripts)
        for lang_code, pattern in SCRIPT_PATTERNS.items():
            if lang_code in ['hi', 'kn']:  # Only check non-Latin scripts first
                # If we find at least 2 characters in the script, classify it
                matches = re.findall(pattern, text)
                if len(matches) >= 2:
                    return lang_code
                    
        # 2. Fallback to langdetect (useful for romanized text or ambiguous cases)
        try:
            detected = detect(text)
            
            # Map langdetect output to our supported languages
            if detected == 'hi':
                return 'hi'
            elif detected == 'kn':
                return 'kn'
            elif detected in ['en', 'fr', 'de', 'es']: # Common latin scripts fallback to english
                return 'en'
        except LangDetectException:
            pass
            
        # Default fallback
        return 'en'
