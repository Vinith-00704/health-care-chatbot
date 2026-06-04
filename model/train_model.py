"""
train_model.py — Train an MLP (Multi-Layer Perceptron) Neural Network for disease prediction.
Replaces the old LogisticRegression model.
"""

import os
import pandas as pd
from sklearn.neural_network import MLPClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import Pipeline
import joblib

import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

print("=" * 50)
print("  NLP Healthcare -- MLP Neural Network Trainer")
print("=" * 50)

# Resolve paths relative to this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, "..", "data", "dataset.csv")
MODEL_PATH = os.path.join(BASE_DIR, "model.pkl")

# Load dataset
df = pd.read_csv(DATA_PATH)
print(f"\n[OK] Dataset loaded: {len(df)} samples, {len(df.columns)-1} features")
print(f"     Diseases: {sorted(df['disease'].unique())}\n")

# Split features and labels
X = df.drop("disease", axis=1)
y = df["disease"]

# Train / test split (no stratify — dataset too small per class)
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.15, random_state=42
)

# Build a Pipeline: StandardScaler → MLP Neural Network
model = Pipeline([
    ("scaler", StandardScaler()),
    ("mlp", MLPClassifier(
        hidden_layer_sizes=(128, 64, 32),   # 3 hidden layers
        activation="relu",                   # ReLU activation
        solver="adam",                       # Adam optimiser
        alpha=0.001,                         # L2 regularisation
        max_iter=2000,
        random_state=42,
        early_stopping=True,
        validation_fraction=0.15,
        n_iter_no_change=30,
        verbose=False
    ))
])

print("[TRAINING] MLP Neural Network (128 -> 64 -> 32 hidden layers)...")
model.fit(X_train, y_train)
print("[DONE] Training complete!\n")

# Evaluation
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)
print(f"[ACCURACY] Test Accuracy: {acc * 100:.1f}%\n")
print("[REPORT] Classification Report:")
print(classification_report(y_test, y_pred, zero_division=0))

# Save model
joblib.dump(model, MODEL_PATH)
print(f"[SAVED] Model saved to: {MODEL_PATH}")
print("=" * 50)