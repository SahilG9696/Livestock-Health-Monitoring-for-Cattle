import numpy as np
import time
from tensorflow.keras.models import load_model
from firebase_admin import credentials, db, initialize_app

# ---------------- CONFIGURATION ----------------
MODEL_PATH = "cow_sound_cnn_model.h5"
FIREBASE_CRED = "firebase_key.json"  # your Firebase service account key
DATABASE_URL = "https://livestockhealthprediction-default-rtdb.firebaseio.com/"
# ------------------------------------------------

# Initialize Firebase
cred = credentials.Certificate(FIREBASE_CRED)
initialize_app(cred, {"databaseURL": DATABASE_URL})

# Load trained model
model = load_model(MODEL_PATH)
print("Model loaded successfully!")

# Firebase references
input_ref = db.reference("Incoming_MFCC")      # where ESP32 uploads features
output_ref = db.reference("Audio_Predictions") # where results will be saved

def predict_from_mfcc(mfcc_list):
    """Run CNN prediction on MFCC features (list of 40 values)."""
    mfcc_array = np.array(mfcc_list).reshape(1, 40, 1, 1)
    prediction = model.predict(mfcc_array)
    predicted_class = np.argmax(prediction)
    labels = {0: "Normal", 1: "Abnormal"}
    result = {
        "status": labels[predicted_class],
        "confidence": float(prediction[0][predicted_class])
    }
    return result

print("🚀 Waiting for new MFCC features...")

# Continuously listen for new inputs (you can run this as a background service)
while True:
    mfcc_data = input_ref.get()
    if mfcc_data:
        for key, data in mfcc_data.items():
            # Process only if not already predicted
            if "mfcc_features" in data and "prediction" not in data:
                features = data["mfcc_features"]
                print(f"Received new MFCC input: {features[:5]}...")

                result = predict_from_mfcc(features)
                print("Prediction:", result)

                # Update the same node with prediction (no deletion)
                input_ref.child(key).update({
                    "prediction": result["status"],
                    "confidence": result["confidence"],
                    "timestamp_predicted": time.strftime("%Y-%m-%d %H:%M:%S")
                })

                # Also push result to Audio_Predictions
                output_ref.push({
                    "mfcc_input_id": key,
                    "prediction": result["status"],
                    "confidence": result["confidence"],
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                })

    time.sleep(5)  # small delay to prevent repeated reads
