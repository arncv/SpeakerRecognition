# -*- coding: utf-8 -*-
"""Speaker V2.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1JXBebF5z13I-pjp_0irBgsGzuayKU91Z
"""

!pip install librosa soundfile numpy scikit-learn matplotlib seaborn

from google.colab import drive
drive.mount('/content/drive')

!unzip /content/drive/MyDrive/speech-emotion-recognition-ravdess-data.zip -d /content/ravdess

import librosa
import numpy as np

def augment_audio(file_name):
    y, sr = librosa.load(file_name)
    # Time Stretching
    y_stretch = librosa.effects.time_stretch(y, rate=1.2)
    # Pitch Shifting
    y_shift = librosa.effects.pitch_shift(y, sr, n_steps=4)
    # Adding Noise
    noise = np.random.randn(len(y))
    y_noise = y + 0.005 * noise
    return [y_stretch, y_shift, y_noise]

import soundfile

def extract_feature(file_name, mfcc=True, chroma=True, mel=True, zcr=True, contrast=True, tonnetz=True):
    with soundfile.SoundFile(file_name) as sound_file:
        X = sound_file.read(dtype="float32")
        sample_rate = sound_file.samplerate
        if chroma or contrast:
            stft = np.abs(librosa.stft(X))
        result = np.array([])
        if mfcc:
            mfccs = np.mean(librosa.feature.mfcc(y=X, sr=sample_rate, n_mfcc=40).T, axis=0)
            result = np.hstack((result, mfccs))
        if chroma:
            chroma = np.mean(librosa.feature.chroma_stft(S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, chroma))
        if mel:
            mel = np.mean(librosa.feature.melspectrogram(y=X, sr=sample_rate).T, axis=0)
            result = np.hstack((result, mel))
        if zcr:
            zcr = np.mean(librosa.feature.zero_crossing_rate(y=X).T, axis=0)
            result = np.hstack((result, zcr))
        if contrast:
            contrast = np.mean(librosa.feature.spectral_contrast(S=stft, sr=sample_rate).T, axis=0)
            result = np.hstack((result, contrast))
        if tonnetz:
            tonnetz = np.mean(librosa.feature.tonnetz(y=librosa.effects.harmonic(X), sr=sample_rate).T, axis=0)
            result = np.hstack((result, tonnetz))
    return result

import glob
import os
from sklearn.model_selection import train_test_split

# Function to extract speaker ID from file name
def get_speaker_id(file_name):
    return file_name.split("-")[-1].split(".")[0]

# List of speakers to observe (all speakers in the dataset)
observed_speakers = [f'speaker{i}' for i in range(1, 25)]

# Load the data and extract features for each sound file
def load_data(test_size=0.2):
    x, y = [], []
    for file in glob.glob("/content/ravdess/Actor_*/*.wav"):
        file_name = os.path.basename(file)
        speaker = f'speaker{int(file_name.split("-")[-1].split(".")[0]):02d}'
        feature = extract_feature(file, mfcc=True, chroma=True, mel=True, zcr=True, contrast=True, tonnetz=True)
        x.append(feature)
        y.append(speaker)
    return train_test_split(np.array(x), y, test_size=test_size, random_state=9)

x_train, x_test, y_train, y_test = load_data(test_size=0.25)

from sklearn.neural_network import MLPClassifier
from sklearn.metrics import accuracy_score, confusion_matrix, classification_report
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize the Multi Layer Perceptron Classifier
model = MLPClassifier(alpha=0.01, batch_size=256, epsilon=1e-08, hidden_layer_sizes=(300,), learning_rate='adaptive', max_iter=500)

# Train the model
model.fit(x_train, y_train)

# Predict for the test set
y_pred = model.predict(x_test)

# Calculate the accuracy of our model
accuracy = accuracy_score(y_true=y_test, y_pred=y_pred)

# Print the accuracy
print("Accuracy: {:.5f}%".format(accuracy*100))

# Confusion Matrix
conf_matrix = confusion_matrix(y_test, y_pred)
plt.figure(figsize=(10, 7))
sns.heatmap(conf_matrix, annot=True, fmt='d', cmap='Blues', xticklabels=observed_speakers, yticklabels=observed_speakers)
plt.xlabel('Predicted')
plt.ylabel('Actual')
plt.title('Confusion Matrix')
plt.show()

# Classification Report
print("Classification Report:")
print(classification_report(y_test, y_pred, target_names=observed_speakers))

from sklearn.model_selection import GridSearchCV

param_grid = {
    'alpha': [0.0001, 0.001, 0.01],
    'hidden_layer_sizes': [(100,), (200,), (300,)],
    'learning_rate': ['constant', 'adaptive'],
    'max_iter': [200, 300, 500]
}

grid = GridSearchCV(estimator=MLPClassifier(), param_grid=param_grid, n_jobs=-1, cv=3)
grid_result = grid.fit(x_train, y_train)

print(f"Best: {grid_result.best_score_} using {grid_result.best_params_}")

import librosa.display

def plot_features(y, sr):
    plt.figure(figsize=(10, 4))
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40)
    librosa.display.specshow(mfccs, x_axis='time')
    plt.colorbar()
    plt.title('MFCC')
    plt.tight_layout()
    plt.show()

y, sr = librosa.load('/content/ravdess/Actor_01/03-01-01-01-01-02-01.wav')
plot_features(y, sr)

!sudo apt-get install texlive-xetex texlive-fonts-recommended texlive-plain-generic pandoc

!jupyter nbconvert --to pdf /content/drive/MyDrive/Colab\ Notebooks/Untitled0.ipynb