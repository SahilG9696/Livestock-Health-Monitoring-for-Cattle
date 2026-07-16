import time
import numpy as np
import joblib     # used to save and load ml models
from tensorflow.keras.models import load_model
import firebase_admin
from firebase_admin import credentials, db

# -----------------------------------------------------
# CONFIGURATION
# -----------------------------------------------------
MODEL_PATH = "sensor_health_model_v2.h5"  # UPDATED
SCALER_PATH = "sensor_scaler_v2.pkl"  # UPDATED
FIREBASE_KEY = "firebase_key.json"
DATABASE_URL = "https://livestockhealthprediction-default-rtdb.firebaseio.com/"  # replace your URL

INPUT_NODE = "Incoming_Sensor_Data"
OUTPUT_NODE = "Sensor_Predictions"

# -----------------------------------------------------
# LOAD MODEL & SCALER
# -----------------------------------------------------
print("Loading model and scaler...")
model = load_model(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
print("Model & Scaler loaded successfully!")

# -----------------------------------------------------
# FIREBASE INITIALIZATION
# -----------------------------------------------------
cred = credentials.Certificate(FIREBASE_KEY)
firebase_admin.initialize_app(cred, {"databaseURL": DATABASE_URL})

input_ref = db.reference(INPUT_NODE)
output_ref = db.reference(OUTPUT_NODE)

# -----------------------------------------------------
# UTILITY FUNCTIONS TO COMPUTE MAGNITUDES
# -----------------------------------------------------
def compute_motion_magnitude(ax, ay, az):
    return (ax**2 + ay**2 + az**2) ** 0.5

def compute_gyro_magnitude(gx, gy, gz):
    return (gx**2 + gy**2 + gz**2) ** 0.5

# -----------------------------------------------------
# MAIN PREDICTION FUNCTION
# -----------------------------------------------------
def predict_sensor_health(data, record_id):

    # Raw input values
    temp = data["temperature"]
    ax = data["accel_x"]
    ay = data["accel_y"]
    az = data["accel_z"]
    gx = data["gyro_x"]
    gy = data["gyro_y"]
    gz = data["gyro_z"]

    # Compute derived features
    motion_magnitude = compute_motion_magnitude(ax, ay, az)
    gyro_magnitude = compute_gyro_magnitude(gx, gy, gz)

    # Prepare full 9-feature vector
    input_vector = np.array([
        temp,
        ax,
        ay,
        az,
        gx,
        gy,
        gz,
        motion_magnitude,
        gyro_magnitude
    ]).reshape(1, -1)

    # Scale the feature vector
    input_scaled = scaler.transform(input_vector)

    # Predict using MLP
    prob = model.predict(input_scaled)[0][0]
    prediction = "normal" if prob < 0.5 else "abnormal"

    # Save prediction to Firebase
    output_ref.child(record_id).set({
        "temperature": temp,
        "accel_x": ax,
        "accel_y": ay,
        "accel_z": az,
        "gyro_x": gx,
        "gyro_y": gy,
        "gyro_z": gz,
        "motion_magnitude": float(motion_magnitude),
        "gyro_magnitude": float(gyro_magnitude),
        "prediction": prediction,
        "confidence": float(prob),
        "timestamp": data["timestamp"]
    })

    print(f"✔ Prediction saved for ID {record_id}: {prediction} (confidence={prob:.3f})")


# -----------------------------------------------------
# MAIN LOOP → continuously read Firebase for new data
# -----------------------------------------------------
print("\n Prediction engine running... (Ctrl+C to stop)\n")

processed_ids = set()

while True:
    all_data = input_ref.get()

    if all_data:
        for record_id, record in all_data.items():
            if record_id not in processed_ids:
                print(f" New sensor data detected: ID = {record_id}")
                predict_sensor_health(record, record_id)
                processed_ids.add(record_id)

    time.sleep(2)   # Check every 2 seconds
