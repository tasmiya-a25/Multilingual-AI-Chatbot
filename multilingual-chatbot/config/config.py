import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Flask Settings
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-super-secure")
    DEBUG = os.getenv("DEBUG", "True") == "True"
    PORT = int(os.getenv("PORT", 5000))
    HOST = os.getenv("HOST", "0.0.0.0")

    # API Settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max upload
    API_RATE_LIMIT = int(os.getenv("API_RATE_LIMIT", 60)) # requests per minute

    # Project Paths
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DATA_DIR = os.path.join(BASE_DIR, "data")
    MODEL_DIR = os.path.join(BASE_DIR, "model", "saved_models")
    
    # Model Configuration
    MAX_SEQUENCE_LENGTH = 50
    EMBEDDING_DIM = 128
    LSTM_UNITS = 128
    DROPOUT_RATE = 0.5
    BATCH_SIZE = 32
    EPOCHS = 100
    
    # Confidence threshold for fallback
    CONFIDENCE_THRESHOLD = 0.65
