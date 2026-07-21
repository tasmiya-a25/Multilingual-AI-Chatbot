"""
Metrics and evaluation utilities for chatbot models.
"""

import numpy as np
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt
import seaborn as sns
import os

def calculate_metrics(y_true, y_pred, label_encoder):
    """
    Calculate and print classification metrics.
    
    Args:
        y_true: True categorical labels
        y_pred: Predicted probabilities
        label_encoder: Fitted LabelEncoder instance
    """
    # Convert one-hot / probs back to indices
    y_true_idx = np.argmax(y_true, axis=1)
    y_pred_idx = np.argmax(y_pred, axis=1)
    
    # Get class names
    class_names = label_encoder.classes_
    
    # Generate report
    report = classification_report(y_true_idx, y_pred_idx, target_names=class_names)
    print("\nClassification Report:\n")
    print(report)
    
    return report

def plot_confusion_matrix(y_true, y_pred, label_encoder, save_path=None):
    """
    Plot and optionally save a confusion matrix.
    """
    y_true_idx = np.argmax(y_true, axis=1)
    y_pred_idx = np.argmax(y_pred, axis=1)
    
    cm = confusion_matrix(y_true_idx, y_pred_idx)
    class_names = label_encoder.classes_
    
    plt.figure(figsize=(12, 10))
    sns.heatmap(cm, annot=False, fmt='d', cmap='Blues', 
                xticklabels=class_names, yticklabels=class_names)
    
    plt.title('Intent Classification Confusion Matrix')
    plt.ylabel('True Intent')
    plt.xlabel('Predicted Intent')
    plt.xticks(rotation=90)
    plt.yticks(rotation=0)
    plt.tight_layout()
    
    if save_path:
        os.makedirs(os.path.dirname(save_path), exist_ok=True)
        plt.savefig(save_path)
        print(f"Confusion matrix saved to {save_path}")
    else:
        plt.show()
        
    plt.close()
