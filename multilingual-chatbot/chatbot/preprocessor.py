"""
Text preprocessing and tokenization for different languages.
"""

import re
import string
import nltk
from nltk.stem import WordNetLemmatizer
from indic_transliteration import sanscript
from indic_transliteration.sanscript import transliterate

class TextPreprocessor:
    def __init__(self, lang_code='en'):
        self.lang_code = lang_code
        
        if self.lang_code == 'en':
            try:
                nltk.data.find('corpora/wordnet')
            except LookupError:
                nltk.download('wordnet', quiet=True)
                nltk.download('omw-1.4', quiet=True)
            self.lemmatizer = WordNetLemmatizer()
            
    def clean_text(self, text):
        """Clean and normalize text based on language."""
        if not text:
            return ""
            
        text = text.lower()
        
        if self.lang_code == 'en':
            # Remove punctuation
            text = text.translate(str.maketrans('', '', string.punctuation))
            # Lemmatize
            words = text.split()
            words = [self.lemmatizer.lemmatize(word) for word in words]
            text = ' '.join(words)
            
        elif self.lang_code == 'hi':
            # Basic cleaning for Hindi
            # Transliterate romanized Hindi to Devanagari if needed
            if re.match(r'^[a-zA-Z\s]+$', text):
                text = transliterate(text, sanscript.ITRANS, sanscript.DEVANAGARI)
            # Remove basic punctuation
            text = re.sub(r'[!@#$%^&*(),.?":{}|<>]', '', text)
            
        elif self.lang_code == 'kn':
            # Basic cleaning for Kannada
            text = re.sub(r'[!@#$%^&*(),.?":{}|<>]', '', text)
            
        # Common cleanup
        text = re.sub(r'\s+', ' ', text).strip()
        return text
