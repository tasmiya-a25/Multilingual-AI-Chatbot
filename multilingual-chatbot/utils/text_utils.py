"""
Utility functions for text processing.
"""

import re
import json

def load_json_file(filepath):
    """Safely load a JSON file."""
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading {filepath}: {e}")
        return None

def is_valid_input(text):
    """Check if input text is valid (not empty, not just symbols)."""
    if not text or not text.strip():
        return False
        
    # Check if there's at least one alphanumeric character (handling unicode)
    if not re.search(r'[^\W_]', text):
        return False
        
    return True
