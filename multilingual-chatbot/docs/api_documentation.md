# LinguaBot REST & WebSocket API Documentation

## REST API Endpoints

### 1. New Session
Create a new chat session to maintain conversation context.

**Endpoint:** `GET /api/session/new`  
**Rate Limit:** 30 req/min

**Response (200 OK):**
```json
{
  "session_id": "4b6c3f30-5896-4a12-88d4-5390c37715f3",
  "message": "New session created successfully."
}
```

### 2. Send Message (Chat)
Process a message and get a response. Auto-detects language if not forced.

**Endpoint:** `POST /api/chat`  
**Rate Limit:** 60 req/min

**Request Body:**
```json
{
  "message": "What is AI?",
  "session_id": "optional-uuid-here",
  "language": "auto" // Optional: "en", "hi", "kn"
}
```

**Response (200 OK):**
```json
{
  "response": "AI (Artificial Intelligence) is the simulation of human intelligence in machines.",
  "intent": "technology",
  "language": "en",
  "language_name": "English",
  "confidence": 0.985,
  "session_id": "session-uuid-used"
}
```

### 3. Detect Language
Detect the language of text using script analysis and heuristics.

**Endpoint:** `POST /api/language/detect`

**Request Body:**
```json
{
  "text": "ನಮಸ್ಕಾರ"
}
```

**Response (200 OK):**
```json
{
  "detected_language": "kn",
  "language_name": "Kannada"
}
```

### 4. Get Session History
Retrieve the conversation history.

**Endpoint:** `GET /api/session/<session_id>/history`

**Response (200 OK):**
```json
{
  "session_id": "user_123",
  "history": [
    {
      "timestamp": "2024-03-12T10:30:00",
      "user_message": "Hello",
      "intent": "greeting",
      "response": "Hi there!",
      "language": "en"
    }
  ]
}
```

### 5. Clear Session History
Clear history for a given session.

**Endpoint:** `POST /api/session/<session_id>/clear`

**Response (200 OK):**
```json
{
  "status": "success",
  "message": "Session history cleared."
}
```

### 6. Model Info
Get metadata about loaded machine learning models.

**Endpoint:** `GET /api/model/info`

**Response (200 OK):**
```json
{
  "models_loaded": 3,
  "details": [
    {
      "language_code": "en",
      "language_name": "English",
      "intents_count": 25,
      "vocab_size": 1204,
      "max_sequence_length": 50
    }
  ]
}
```

---

## WebSocket (Socket.IO) API

Connect via standard Socket.IO client to `/` or `ws://localhost:5000`.

### Client Events (Emit to Server)

- **`chat_message`**: Send a message for processing.
  ```json
  {
    "message": "Tell me a joke",
    "session_id": "user_123",
    "language": "auto" 
  }
  ```

### Server Events (Listen from Server)

- **`server_message`**: Sent on successful connection.
- **`typing_status`**: Indicates if bot is processing.
  ```json
  { "is_typing": true }
  ```
- **`bot_response`**: The final response to `chat_message`. Matches REST API response structure.
- **`error`**: Emitted on failure.
  ```json
  { "message": "An error occurred..." }
  ```
