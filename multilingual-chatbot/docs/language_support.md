# Language Support Guide

LinguaBot is designed to support multiple languages natively using separate deep learning models for optimal accuracy.

## Supported Languages

| Code | Language | Native Script | Unicode Block | Training Data |
|------|----------|---------------|---------------|---------------|
| `en` | English  | Latin         | `N/A`         | 25+ Intents   |
| `hi` | Hindi    | Devanagari    | `0900-097F`   | 20+ Intents   |
| `kn` | Kannada  | Kannada       | `0C80-0CFF`   | 15+ Intents   |

## How Language Processing Works

1. **Auto-Detection**
   When a user sends a message, the `LanguageDetector` class identifies the language.
   - It first looks for specific Unicode blocks (Devanagari for Hindi, Kannada for Kannada). This is extremely fast and 100% accurate for native scripts.
   - If no Indian script is found, it uses the `langdetect` library as a fallback.

2. **Romanized Text Support**
   If a user types Hindi using English letters (e.g., "kaise ho"), the preprocessor attempts to transliterate it to Devanagari using `indic-transliteration` before passing it to the neural network.

3. **Explicit Switching**
   Users can explicitly command the bot to switch languages (e.g., "Switch to Hindi"). This overrides the auto-detector for the current turn and sets a preferred language in the session context.

## Adding a New Language

To add support for a new language (e.g., Tamil):

1. **Update `config/languages.py`**:
   Add the language code, name, and script Unicode range.
   ```python
   'ta': {
       'code': 'ta',
       'name': 'Tamil',
       'intent_file': 'intents_tamil.json',
       'model_name': 'chatbot_model_ta'
   }
   ```
   Add the regex pattern for script detection (Tamil: `\u0B80-\u0BFF`).

2. **Create Intent Data**:
   Create `data/intents_tamil.json` following the same structure as existing files. Provide translated patterns and responses for all intents.

3. **Update Preprocessor**:
   If the language requires special tokenization (e.g., agglutinative languages), add rules in `chatbot/preprocessor.py`.

4. **Train Model**:
   Run `python model/train.py --lang ta`.

5. **Update UI**:
   Add the language option to the `<select>` dropdown in `templates/index.html` and add the flag mapping in `static/js/ui.js`.
