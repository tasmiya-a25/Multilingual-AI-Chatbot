"""
Response generator that selects appropriate responses based on intent and context.
"""

import random

class ResponseGenerator:
    def __init__(self):
        pass
        
    def get_response(self, intent_tag, intents_metadata, context=None):
        """
        Select a response for the given intent.
        
        Args:
            intent_tag: The classified intent
            intents_metadata: The loaded JSON intents data for the language
            context: Dictionary of contextual variables
            
        Returns:
            A string response.
        """
        # Find the matching intent
        matched_intent = None
        for intent in intents_metadata:
            if intent['tag'] == intent_tag:
                matched_intent = intent
                break
                
        if not matched_intent:
            return self._get_fallback_response(intents_metadata)
            
        # Select a random response from the available options
        responses = matched_intent.get('responses', [])
        if not responses:
            return self._get_fallback_response(intents_metadata)
            
        response = random.choice(responses)
        
        # Replace context variables if any (e.g., {name})
        if context:
            try:
                response = response.format(**context)
            except KeyError:
                # If a placeholder in the response isn't in context, leave it or replace with generic
                pass
                
        return response
        
    def _get_fallback_response(self, intents_metadata):
        """Get a fallback response if the intent isn't found."""
        for intent in intents_metadata:
            if intent['tag'] == 'fallback':
                responses = intent.get('responses', [])
                if responses:
                    return random.choice(responses)
        return "I'm not sure how to respond to that."
