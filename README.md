# 🐄 Livestock Health Monitoring for Cattle

> Iot and ML based livestock health monitoring system for early disease detection in cattle using Machine Learning and sensor data.

---

## 📌 Project Overview

Livestock Health Monitoring for Cattle is a Bachelor of Engineering (B.E.) final year project developed to assist farmers in monitoring the health of cattle.

The system collects health-related data such as temperature, motion, and cattle sounds. Using Machine Learning models, it predicts whether the cattle is in a normal or abnormal condition and helps farmers take timely action.

---

## ✨ Features

- 🐄 Real-time cattle health monitoring
- 🌡 Temperature monitoring
- 🚶 Motion analysis
- 🎤 Cow sound analysis using Machine Learning
- 🤖 Disease prediction
- 🔥 Firebase integration
- 📊 Interactive Web Dashboard
- 🚨 Early health alerts

---

# 🏗 Project Architecture

```
                  Sensors
        (Temperature, Motion, Sound)
                    │
                    ▼
            Data Collection
                    │
                    ▼
          Firebase Realtime Database
                    │
        ┌───────────┴───────────┐
        ▼                       ▼
 Machine Learning          Web Application
 (Python Models)        (React + Vite Dashboard)
        │                       │
        └───────────┬───────────┘
                    ▼
          Health Prediction
                    │
                    ▼
            Farmer Dashboard
```

---

# 📂 Repository Structure

```
Livestock-Health-Monitoring-for-Cattle

│
├── Web_Application/
│
├── ML_Model/
│
├── README.md
│
└── .gitignore
```

---

# 🤖 Machine Learning

The project uses Machine Learning models for:

- Audio Classification
- Motion Prediction
- Sensor-based Health Prediction

Audio features are extracted using MFCC before training the classification model.

---

# 💻 Technologies Used

## Frontend

- React
- Vite
- TypeScript
- Tailwind CSS

## Backend / Cloud

- Firebase

## Machine Learning

- Python
- TensorFlow / Keras
- NumPy
- Pandas
- Librosa
- Scikit-learn

---

# 🚀 How to Run

## Web Application

```bash
cd Web_Application
npm install
npm run dev
```

## Machine Learning

```bash
cd ML_Model

pip install -r requirements.txt

python train_cnn.py
```

---

# 📊 Future Enhancements

- Mobile Application
- Live IoT Sensor Integration
- GPS Tracking
- Cloud Deployment
- Improved AI Model Accuracy

---

# 📌 Note

The training dataset, trained models, and Firebase credentials are not included in this repository due to GitHub file size limits and security reasons.

---

# 👨‍💻 Authors
**Sahil Shekhar Gaikwad**
**Sanket Amar Dhayguide**
**Shritej Nanaso Phadatare**
**Abhijit Prakash Bhagat**

Bachelor of Engineering (Computer Engineering)

Savitribai Phule Pune University

GitHub:
https://github.com/SahilG9696

---

⭐ If you found this project useful, consider giving it a star.
