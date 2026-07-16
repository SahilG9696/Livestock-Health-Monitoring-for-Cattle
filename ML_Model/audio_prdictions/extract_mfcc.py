import os
import numpy as np
import librosa
from tqdm import tqdm
import soundfile as sf

# ----------- CONFIGURATION -------------
DATASET_PATH = "../CowSoundDataset_2class"  # your dataset folder
OUTPUT_FEATURES = "features"
SAMPLE_RATE = 22050  # common for audio
N_MFCC = 40          # number of MFCCs to extract
# ---------------------------------------

# Create output folder
os.makedirs(OUTPUT_FEATURES, exist_ok=True)

# Prepare lists for features and labels
X = []
y = []

# Class mapping
class_mapping = {"Normal": 0, "Abnormal": 1}

print("Extracting MFCC features from dataset...\n")

# Loop through both folders
for label_name in class_mapping.keys():
    folder_path = os.path.join(DATASET_PATH, label_name)
    print(f"Processing folder: {label_name}")

    for file_name in tqdm(os.listdir(folder_path)):
        if file_name.endswith(".wav"):
            file_path = os.path.join(folder_path, file_name)
            try:
                # Load audio file
                signal, sr = librosa.load(file_path, sr=SAMPLE_RATE)

                # Ensure minimum length (to avoid short clips)
                if len(signal) < sr:
                    padding = sr - len(signal)
                    signal = np.pad(signal, (0, padding))

                # Extract MFCCs
                mfcc = librosa.feature.mfcc(y=signal, sr=sr, n_mfcc=N_MFCC)
                mfcc_mean = np.mean(mfcc.T, axis=0)  # average over time

                # Append
                X.append(mfcc_mean)
                y.append(class_mapping[label_name])

            except Exception as e:
                print(f"Error processing {file_name}: {e}")

# Convert to numpy arrays
X = np.array(X)
y = np.array(y)

# Save features
np.save(os.path.join(OUTPUT_FEATURES, "X.npy"), X)
np.save(os.path.join(OUTPUT_FEATURES, "y.npy"), y)

print("\nFeature extraction completed!")
print(f"Saved MFCC features to folder: {OUTPUT_FEATURES}")
print(f"Total samples processed: {len(X)}")