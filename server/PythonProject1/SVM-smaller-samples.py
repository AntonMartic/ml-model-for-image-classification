import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.ensemble import RandomForestClassifier

import random
import matplotlib.pyplot as plt

# Load two HOG feature files
with (open("hog_features/hog_features_part_1.pkl", "rb") as f1,
      open("hog_features/hog_features_part_24.pkl", "rb") as f2):
    X1, y1 = pickle.load(f1)
    X2, y2 = pickle.load(f2)

# Combine data
X = np.vstack((X1, X2))  # Stack feature matrices
y = np.hstack((y1, y2))  # Stack labels

print(f"Feature matrix shape after combining: {X.shape}")  # Should be (2000, feature_length)
print(f"Labels shape after combining: {y.shape}")          # Should be (2000,)

# Split data into training (80%) and testing (20%)
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train an SVM model
svm_model = SVC(kernel="rbf", C=5, gamma=0.01)  # Try kernel='rbf' later
svm_model.fit(X_train, y_train)

# Predict on test set
y_pred = svm_model.predict(X_test)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy:.4f}")

# Save trained SVM model to a file
"""with open("svm_model.pkl", "wb") as model_file:
    pickle.dump(svm_model, model_file)

print("SVM model saved as svm_model.pkl")"""
