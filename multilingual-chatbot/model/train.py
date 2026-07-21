"""
Training script for intent classification models (English, Hindi, Kannada).
"""

import os
import sys
import json
import pickle
import numpy as np
import random
import argparse
from datetime import datetime

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.config import Config
from config.languages import SUPPORTED_LANGUAGES, get_intent_file
from model.chatbot_model import ChatbotModel
from chatbot.preprocessor import TextPreprocessor

from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau, ModelCheckpoint
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

def load_data(lang_code):
    """Load intent JSON data for a specific language."""
    filename = get_intent_file(lang_code)
    filepath = os.path.join(Config.DATA_DIR, filename)
    
    if not os.path.exists(filepath):
        print(f"Error: Intent file not found: {filepath}")
        return None
        
    with open(filepath, 'r', encoding='utf-8') as f:
        data = json.load(f)
        
    return data

def prepare_data(data, lang_code):
    """Process intent JSON into training arrays."""
    preprocessor = TextPreprocessor(lang_code)
    
    texts = []
    labels = []
    
    for intent in data['intents']:
        tag = intent['tag']
        # Skip fallback intent for training (or give it very few samples if needed)
        if tag == 'fallback':
            continue
            
        for pattern in intent['patterns']:
            # Apply language-specific preprocessing
            clean_text = preprocessor.clean_text(pattern)
            texts.append(clean_text)
            labels.append(tag)
            
    return texts, labels

def plot_training_history(history, lang_code, save_dir):
    """Plot and save training metrics."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 4))
    
    # Accuracy plot
    ax1.plot(history.history['accuracy'], label='Train')
    ax1.plot(history.history['val_accuracy'], label='Validation')
    ax1.set_title(f'Model Accuracy ({lang_code})')
    ax1.set_xlabel('Epoch')
    ax1.set_ylabel('Accuracy')
    ax1.legend()
    
    # Loss plot
    ax2.plot(history.history['loss'], label='Train')
    ax2.plot(history.history['val_loss'], label='Validation')
    ax2.set_title(f'Model Loss ({lang_code})')
    ax2.set_xlabel('Epoch')
    ax2.set_ylabel('Loss')
    ax2.legend()
    
    plt.tight_layout()
    os.makedirs(os.path.join(save_dir, "plots"), exist_ok=True)
    plt.savefig(os.path.join(save_dir, "plots", f"history_{lang_code}.png"))
    print(f"Saved training plot for {lang_code}.")

def train_language_model(lang_code):
    """Train an intent classification model for a specific language."""
    print(f"\n{'='*50}")
    print(f"Starting training for: {SUPPORTED_LANGUAGES[lang_code]['name']} ({lang_code})")
    print(f"{'='*50}")
    
    # 1. Load Data
    data = load_data(lang_code)
    if not data:
        return
        
    texts, labels = prepare_data(data, lang_code)
    print(f"Loaded {len(texts)} samples across {len(set(labels))} intents.")
    
    # 2. Encode Labels
    label_encoder = LabelEncoder()
    y_encoded = label_encoder.fit_transform(labels)
    # One-hot encode
    num_classes = len(label_encoder.classes_)
    y_categorical = np.zeros((len(y_encoded), num_classes))
    for i, label in enumerate(y_encoded):
        y_categorical[i, label] = 1
        
    # 3. Tokenize Text
    tokenizer = Tokenizer(oov_token="<OOV>")
    tokenizer.fit_on_texts(texts)
    vocab_size = len(tokenizer.word_index) + 1
    
    sequences = tokenizer.texts_to_sequences(texts)
    X_padded = pad_sequences(sequences, maxlen=Config.MAX_SEQUENCE_LENGTH, padding='post')
    
    # 4. Train/Test Split
    X_train, X_val, y_train, y_val = train_test_split(X_padded, y_categorical, test_size=0.15, random_state=42)
    
    print(f"Vocab size: {vocab_size}")
    print(f"Training shape: X={X_train.shape}, y={y_train.shape}")
    print(f"Validation shape: X={X_val.shape}, y={y_val.shape}")
    
    # 5. Build Model
    model_builder = ChatbotModel(
        vocab_size=vocab_size,
        num_classes=num_classes,
        max_sequence_length=Config.MAX_SEQUENCE_LENGTH
    )
    model = model_builder.build(
        embedding_dim=Config.EMBEDDING_DIM,
        lstm_units=Config.LSTM_UNITS,
        dropout_rate=Config.DROPOUT_RATE
    )
    model.summary()
    
    # 6. Callbacks
    os.makedirs(Config.MODEL_DIR, exist_ok=True)
    model_path = os.path.join(Config.MODEL_DIR, f"{lang_code}_model.h5")
    
    callbacks = [
        EarlyStopping(monitor='val_loss', patience=15, restore_best_weights=True),
        ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=5, min_lr=1e-5),
        ModelCheckpoint(model_path, monitor='val_accuracy', save_best_only=True, verbose=1)
    ]
    
    # 7. Train
    history = model.fit(
        X_train, y_train,
        validation_data=(X_val, y_val),
        epochs=Config.EPOCHS,
        batch_size=Config.BATCH_SIZE,
        callbacks=callbacks,
        verbose=1
    )
    
    # 8. Save Artifacts (Tokenizer, LabelEncoder, intents metadata)
    artifacts = {
        'tokenizer': tokenizer,
        'label_encoder': label_encoder,
        'intents_metadata': data['intents'],
        'max_sequence_length': Config.MAX_SEQUENCE_LENGTH,
        'lang_code': lang_code
    }
    
    artifacts_path = os.path.join(Config.MODEL_DIR, f"{lang_code}_artifacts.pkl")
    with open(artifacts_path, 'wb') as f:
        pickle.dump(artifacts, f)
        
    print(f"Saved artifacts to {artifacts_path}")
    plot_training_history(history, lang_code, Config.MODEL_DIR)
    
    # Evaluate
    loss, accuracy = model.evaluate(X_val, y_val, verbose=0)
    print(f"Validation Accuracy: {accuracy*100:.2f}%")
    print(f"Training for {lang_code} complete!\n")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train Chatbot Models")
    parser.add_argument("--lang", type=str, default="all", choices=["en", "hi", "kn", "all"], help="Language to train")
    args = parser.parse_args()
    
    if args.lang == "all":
        for lang in SUPPORTED_LANGUAGES.keys():
            train_language_model(lang)
    else:
        train_language_model(args.lang)
