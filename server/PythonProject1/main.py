import pickle
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score

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
svm_model = SVC(kernel="rbf", C=10, gamma=0.01)  # Try kernel='rbf' later
svm_model.fit(X_train, y_train)

# Predict on test set
y_pred = svm_model.predict(X_test)

# Evaluate accuracy
accuracy = accuracy_score(y_test, y_pred)
print(f"Test Accuracy: {accuracy:.4f}")



# Select a few random test images
num_samples = 10  # Choose how many to display
random_indices = random.sample(range(len(X_test)), num_samples)
test_images = X_test[random_indices]
true_labels = y_test[random_indices]
predicted_labels = svm_model.predict(test_images)

# Plot images with predicted vs actual labels
fig, axes = plt.subplots(2, 5, figsize=(12, 5))
for i, ax in enumerate(axes.ravel()):
    ax.imshow(X_test_original[random_indices[i]])  # Assuming X_test_original has original images
    ax.set_title(f"Pred: {predicted_labels[i]}, True: {true_labels[i]}")
    ax.axis("off")

plt.tight_layout()
plt.show()
