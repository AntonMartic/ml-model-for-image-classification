import os
import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score, classification_report

# Folder where HOG feature files are saved
hog_folder = "hog_features"  # Change this if needed

# Lists to store combined data
X_combined = []
y_combined = []

# Load all .pkl files
for file in os.listdir(hog_folder):
    if file.endswith(".pkl"):  # Ensure we only process .pkl files
        file_path = os.path.join(hog_folder, file)
        with open(file_path, "rb") as f:
            X_part, y_part = pickle.load(f)  # Load the features and labels
            X_combined.append(X_part)
            y_combined.append(y_part)

# Convert to NumPy arrays
X_combined = np.vstack(X_combined)  # Stack feature arrays vertically
y_combined = np.hstack(y_combined)  # Stack labels horizontally

# Print dataset shape
print(f"Combined Feature matrix shape: {X_combined.shape}")  # (num_samples, num_features)
print(f"Combined Labels shape: {y_combined.shape}")          # (num_samples,)




# Split dataset into 80% training and 20% testing
X_train, X_test, y_train, y_test = train_test_split(X_combined, y_combined, test_size=0.2, random_state=42, stratify=y_combined)

# Print dataset shapes
print(f"Training data shape: {X_train.shape}, Training labels shape: {y_train.shape}")
print(f"Testing data shape: {X_test.shape}, Testing labels shape: {y_test.shape}")

"""

# Initialize SVM classifier
svm_model = SVC(kernel='linear', random_state=42)

# Train the model on the training data
svm_model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = svm_model.predict(X_test)

# Evaluate performance
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy:.4f}")

# Print detailed classification report
print("Classification Report:\n", classification_report(y_test, y_pred))

"""
