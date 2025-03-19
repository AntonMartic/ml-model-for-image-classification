import pickle
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from skimage.color import rgb2gray
from skimage.feature import hog
import matplotlib.pyplot as plt



# Function to preprocess and extract HOG features from a single image
def preprocess_single_image(image_path):
    img = imread(image_path)
    img_resized = resize(img, (128, 128), anti_aliasing=True)
    img_gray = rgb2gray(img_resized)

    # Extract HOG features
    features = hog(img_gray, pixels_per_cell=(8, 8),
                   cells_per_block=(2, 2), orientations=9)

    return features.reshape(1, -1), img_resized  # Return reshaped features and original image


# Load the trained SVM model
with open("svm_model.pkl", "rb") as model_file:
    svm_model = pickle.load(model_file)

print("SVM model loaded successfully!")

# Choose a test image from your dataset (Modify this path to test different images)
image_path = "training-data/PetImages/Cat/5.jpg"  # Example image

# Preprocess the image
hog_features, img_resized = preprocess_single_image(image_path)

# Make prediction
prediction = svm_model.predict(hog_features)

# Map label to class name
class_names = {0: "Cat", 1: "Dog"}
predicted_label = class_names[prediction[0]]

# Display the image with predicted label
plt.imshow(img_resized)
plt.title(f"Predicted: {predicted_label}")
plt.axis("off")
plt.show()
