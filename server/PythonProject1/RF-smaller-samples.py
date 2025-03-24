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

# Train a Random Forest model
rf_model = RandomForestClassifier(n_estimators=400, random_state=42)  # 100 trees
rf_model.fit(X_train, y_train)

# Predict on test set
y_pred = rf_model.predict(X_test)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy:.4f}")

"""
# Save trained RF model to a file
with open("rf_model.pkl", "wb") as model_file:
    pickle.dump(rf_model, model_file)

print("RF model saved as rf_model.pkl")

"""