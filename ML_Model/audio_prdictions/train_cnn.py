import numpy as np
from sklearn.model_selection import train_test_split
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Conv2D, MaxPooling2D, Flatten, Dropout, Reshape
from tensorflow.keras.utils import to_categorical
import matplotlib.pyplot as plt

# Load features
X = np.load("../features/X.npy")
y = np.load("../features/y.npy")

print("Data loaded successfully!")
print("X shape:", X.shape)
print("y shape:", y.shape)

# Reshape X for CNN input: (samples, height, width, channels)
# Our MFCCs are 1D vectors, so reshape to (n_samples, n_mfcc, 1, 1)
X = X.reshape(X.shape[0], X.shape[1], 1, 1)

# One-hot encode labels
y_cat = to_categorical(y)

# Split into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y_cat, test_size=0.2, random_state=42, stratify=y_cat)

# Build CNN model
model = Sequential([
    Conv2D(32, (3, 1), activation='relu', input_shape=(X.shape[1], 1, 1)),
    MaxPooling2D((2, 1)),
    Dropout(0.3),

    Conv2D(64, (3, 1), activation='relu'),
    MaxPooling2D((2, 1)),
    Dropout(0.3),

    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.3),
    Dense(2, activation='softmax')  # 2 classes: Normal / Abnormal
])

# Compile
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

# Train
history = model.fit(
    X_train, y_train,
    epochs=30,
    batch_size=8,
    validation_data=(X_test, y_test)
)

# Evaluate
test_loss, test_acc = model.evaluate(X_test, y_test)
print(f"\nTest Accuracy: {test_acc * 100:.2f}%")

# Save model
model.save("cow_sound_cnn_model.h5")
print("Model saved as cow_sound_cnn_model.h5")