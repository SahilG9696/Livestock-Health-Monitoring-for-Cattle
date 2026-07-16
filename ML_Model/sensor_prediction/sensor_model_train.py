import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.callbacks import EarlyStopping
import joblib

# ---------------------------------------------------
# STEP 1: Load dataset
# ---------------------------------------------------
data = pd.read_csv("../Sensor_Data/sensor_data.csv")   # your new dataset file

# ---------------------------------------------------
# STEP 2: Preprocess
# ---------------------------------------------------
# Convert label to numeric
data['label'] = data['label'].map({'normal': 0, 'abnormal': 1})

# Select ALL 9 features
X = data[[
    'temperature',
    'accel_x',
    'accel_y',
    'accel_z',
    'gyro_x',
    'gyro_y',
    'gyro_z',
    'motion_magnitude',
    'gyro_magnitude'
]]

y = data['label']

# ---------------------------------------------------
# STEP 3: Normalize features
# ---------------------------------------------------
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# ---------------------------------------------------
# STEP 4: Train-test split
# ---------------------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X_scaled, y, test_size=0.2, random_state=42
)

# ---------------------------------------------------
# STEP 5: Build MLP model
# ---------------------------------------------------
model = Sequential([
    Dense(64, activation='relu', input_shape=(9,)),   # 9 features now
    Dense(32, activation='relu'),
    Dense(16, activation='relu'),
    Dense(8, activation='relu'),
    Dense(1, activation='sigmoid')                     # binary classification
])

model.compile(optimizer='adam', loss='binary_crossentropy', metrics=['accuracy'])

# ---------------------------------------------------
# STEP 6: Train
# ---------------------------------------------------
early_stop = EarlyStopping(monitor='val_loss', patience=5, restore_best_weights=True)

model.fit(
    X_train, y_train,
    validation_data=(X_test, y_test),
    epochs=60,
    batch_size=16,
    callbacks=[early_stop]
)

# ---------------------------------------------------
# STEP 7: Evaluate
# ---------------------------------------------------
loss, acc = model.evaluate(X_test, y_test)
print(f"\nFinal Model Accuracy: {acc:.3f}")

# ---------------------------------------------------
# STEP 8: Save model & scaler
# ---------------------------------------------------
model.save("sensor_health_model_v2.h5")
joblib.dump(scaler, "sensor_scaler_v2.pkl")

print("\nModel and scaler saved successfully!")
