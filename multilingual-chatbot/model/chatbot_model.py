"""
Model architecture for the intent classification model.
"""

import tensorflow as tf
from tensorflow.keras.models import Sequential, Model
from tensorflow.keras.layers import Dense, Embedding, LSTM, Bidirectional, Dropout, BatchNormalization, Input

def build_lstm_model(vocab_size, num_classes, max_sequence_length, embedding_dim=128, lstm_units=128, dropout_rate=0.5):
    """
    Builds a bidirectional LSTM model for intent classification.
    
    Args:
        vocab_size: Size of the vocabulary
        num_classes: Number of intent classes
        max_sequence_length: Maximum length of input sequences
        embedding_dim: Dimension of embedding vectors
        lstm_units: Number of units in LSTM layers
        dropout_rate: Dropout probability
        
    Returns:
        Compiled Keras model
    """
    inputs = Input(shape=(max_sequence_length,))
    
    x = Embedding(input_dim=vocab_size, output_dim=embedding_dim, input_length=max_sequence_length)(inputs)
    
    # Spatial dropout for embeddings
    x = Dropout(dropout_rate / 2)(x)
    
    x = Bidirectional(LSTM(lstm_units, return_sequences=True))(x)
    x = Dropout(dropout_rate)(x)
    x = Bidirectional(LSTM(lstm_units // 2))(x)
    
    x = Dense(128, activation='relu')(x)
    x = BatchNormalization()(x)
    x = Dropout(dropout_rate)(x)
    
    x = Dense(64, activation='relu')(x)
    x = Dropout(dropout_rate / 2)(x)
    
    outputs = Dense(num_classes, activation='softmax')(x)
    
    model = Model(inputs=inputs, outputs=outputs, name="IntentClassifier_BiLSTM")
    
    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.001),
        loss='categorical_crossentropy',
        metrics=['accuracy']
    )
    
    return model

class ChatbotModel:
    def __init__(self, vocab_size, num_classes, max_sequence_length):
        self.vocab_size = vocab_size
        self.num_classes = num_classes
        self.max_sequence_length = max_sequence_length
        self.model = None
        
    def build(self, embedding_dim=128, lstm_units=128, dropout_rate=0.5):
        self.model = build_lstm_model(
            self.vocab_size,
            self.num_classes,
            self.max_sequence_length,
            embedding_dim,
            lstm_units,
            dropout_rate
        )
        return self.model
    
    def summary(self):
        if self.model:
            return self.model.summary()
        return "Model not built yet."
