# 💬 Multi-Lingual Chatbot (ML)

A context-aware AI chatbot supporting **English**, **Hindi**, and **Kannada** with deep learning intent classification, a Flask REST API, and real-time Socket.IO chat interface.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python)
![TensorFlow](https://img.shields.io/badge/TensorFlow-2.13-orange?logo=tensorflow)
![Flask](https://img.shields.io/badge/Flask-2.3-lightgrey?logo=flask)
![NLTK](https://img.shields.io/badge/NLTK-3.8-green)
![Socket.IO](https://img.shields.io/badge/Socket.IO-5.3-black?logo=socket.io)
![Docker](https://img.shields.io/badge/Docker-Supported-blue?logo=docker)

---

## ✨ Features

- 🌐 **3 Language Support** – English, Hindi (हिन्दी), Kannada (ಕನ್ನಡ)
- 🔍 **Auto Language Detection** – Script-based + langdetect
- 🧠 **LSTM Deep Learning** – Bidirectional LSTM intent classifier
- 💬 **Context Awareness** – Conversation history and follow-up detection
- ⚡ **Real-time Chat** – Socket.IO WebSocket connection
- 🎤 **Voice Input** – Web Speech API integration
- 📡 **REST API** – Full REST endpoints + Socket.IO
- 🐳 **Docker Ready** – Single command deployment

---

## 🏗️ Project Structure

```
multilingual-chatbot/
├── api/
│   ├── app.py               # Flask + Socket.IO server
│   └── routes.py            # API route definitions
├── chatbot/
│   ├── chatbot.py           # Core MultilingualChatbot class
│   ├── language_detector.py # Language detection module
│   ├── preprocessor.py      # Text preprocessing per language
│   ├── context_manager.py   # Conversation context tracking
│   └── response_generator.py# Response selection engine
├── data/
│   ├── intents_english.json # English intents (25+ intents)
│   ├── intents_hindi.json   # Hindi intents (20+ intents)
│   └── intents_kannada.json # Kannada intents (15+ intents)
├── model/
│   ├── train.py             # LSTM training script
│   └── chatbot_model.py     # Model architecture
├── config/
│   ├── config.py            # Application config
│   └── languages.py         # Language-specific settings
├── utils/
│   ├── text_utils.py        # Text utility functions
│   └── metrics.py           # Model evaluation metrics
├── templates/
│   └── index.html           # Chat UI frontend
├── static/
│   ├── css/style.css        # Dark AI theme
│   └── js/chat.js           # Chat JavaScript
├── docs/
│   ├── api_documentation.md
│   └── model_architecture.md
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

---

## 🚀 Quick Start

```bash
git clone https://github.com/yourusername/multilingual-chatbot.git
cd multilingual-chatbot

python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt

# Download NLTK data
python -c "import nltk; nltk.download('punkt'); nltk.download('wordnet'); nltk.download('stopwords')"

# Train models for all languages
python model/train.py --lang all

# Start the server
python api/app.py
```

Open: [http://localhost:5000](http://localhost:5000)

---

## 📡 API Reference

### Send a Message
```http
POST /api/chat
Content-Type: application/json

{
  "message": "Hello, how are you?",
  "session_id": "user_123",
  "language": "en"
}
```

**Response:**
```json
{
  "response": "I'm doing great! How can I help you today?",
  "intent": "greeting",
  "language": "en",
  "language_name": "English",
  "confidence": 0.97,
  "session_id": "user_123"
}
```

### Detect Language
```http
POST /api/language/detect
{"text": "नमस्ते, आप कैसे हैं?"}
```

### Get Session History
```http
GET /api/session/user_123/history
```

---

## 🌐 Language Support

| Language | Script | Detection | Training Intents |
|----------|--------|-----------|-----------------|
| English | Latin | langdetect | 25+ intents |
| Hindi | Devanagari (0900–097F) | Script range | 20+ intents |
| Kannada | Kannada script (0C80–0CFF) | Script range | 15+ intents |

---

## 🧠 Model Architecture

```
Input Text
    │
    ▼
Tokenization + Lemmatization
    │
    ▼
Bag-of-Words Encoding
    │
    ▼
Embedding Layer (128 dims)
    │
    ▼
Bidirectional LSTM (128 units)
    │
    ▼
Dense(128) + BatchNorm + Dropout
    │
    ▼
Dense(64) + Dropout
    │
    ▼
Dense(num_intents) + Softmax
    │
    ▼
Intent Classification + Response
```

---

## 🛠️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Backend | Python, Flask |
| ML Framework | TensorFlow 2.13, Keras |
| NLP | NLTK, langdetect |
| Real-time | Flask-SocketIO, eventlet |
| Frontend | HTML5, CSS3, Vanilla JS |
| WebSocket | Socket.IO |
| Deployment | Docker, Gunicorn |

---

## 📄 License
MIT License – see LICENSE for details.
