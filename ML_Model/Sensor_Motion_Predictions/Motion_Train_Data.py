import os
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, LSTM, Dropout, BatchNormalization, Input
from tensorflow.keras.callbacks import EarlyStopping
import joblib

# ---------------------------------------------------
# STEP 1: Load Dataset
# ---------------------------------------------------

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
file_path = os.path.join(BASE_DIR, "Sensor_Data", "motion_data.csv")

data = pd.read_csv(file_path)

print("Dataset Loaded Successfully!")
print("Total Samples:", len(data))

# ---------------------------------------------------
# STEP 2: Clean Dataset
# ---------------------------------------------------

data = data.dropna()
data = data[np.isfinite(data['classification'])]
data['classification'] = data['classification'].astype(int)

# Reduce dataset size for stable training
data = data.sample(n=300000, random_state=42)

print("\nClass Distribution:")
print(data['classification'].value_counts())

# ---------------------------------------------------
# STEP 3: Extract Motion Features
# ---------------------------------------------------

X_raw = data[['x', 'y', 'z']].values
y_raw = data['classification'].values

# ---------------------------------------------------
# STEP 4: Create Sliding Windows
# ---------------------------------------------------

window_size = 40   # Larger window for better pattern capture

X_windows = []
y_windows = []

for i in range(len(X_raw) - window_size):
    X_windows.append(X_raw[i:i + window_size])
    labels = y_raw[i:i + window_size]
    y_windows.append(np.bincount(labels).argmax())

X_windows = np.array(X_windows)
y_windows = np.array(y_windows)

print("Sliding windows created:", X_windows.shape)

# ---------------------------------------------------
# STEP 5: Normalize Data
# ---------------------------------------------------

X_reshaped = X_windows.reshape(-1, 3)

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X_reshaped)

X_scaled = X_scaled.reshape(X_windows.shape)

# ---------------------------------------------------
# STEP 6: Train-Test Split
# ---------------------------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X_scaled,
    y_windows,
    test_size=0.2,
    random_state=42
)

# ---------------------------------------------------
# STEP 7: Build Advanced LSTM Model
# ---------------------------------------------------

model = Sequential([
    Input(shape=(window_size, 3)),

    LSTM(128, return_sequences=True),
    Dropout(0.3),

    LSTM(64),
    Dropout(0.3),

    BatchNormalization(),

    Dense(32, activation='relu'),
    Dense(3, activation='softmax')
])

model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

model.summary()

# ---------------------------------------------------
# STEP 8: Train Model
# ---------------------------------------------------

early_stop = EarlyStopping(
    monitor='val_loss',
    patience=5,
    restore_best_weights=True
)

model.fit(
    X_train,
    y_train,
    validation_data=(X_test, y_test),
    epochs=40,
    batch_size=64,
    callbacks=[early_stop]
)

# ---------------------------------------------------
# STEP 9: Evaluate
# ---------------------------------------------------

loss, acc = model.evaluate(X_test, y_test)
print(f"\nFinal Accuracy: {acc:.3f}")

# ---------------------------------------------------
# STEP 10: Save Model & Scaler
# ---------------------------------------------------

model.save(os.path.join(BASE_DIR, "motion_lstm_optimized_model.keras"))
joblib.dump(scaler, os.path.join(BASE_DIR, "motion_lstm_optimized_scaler.pkl"))

print("\nOptimized LSTM Model and Scaler saved successfully!")