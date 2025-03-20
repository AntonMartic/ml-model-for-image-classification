import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.transform import resize
from skimage.color import rgb2gray
from skimage.feature import hog
import pickle

# Load the trained SVM model
with open("svm_model.pkl", "rb") as f:
    svm_model = pickle.load(f)

# Function to extract HOG features
def extract_hog(image):
    image_resized = resize(image, (128, 128))
    image_gray = rgb2gray(image_resized)
    features, _ = hog(image_gray, pixels_per_cell=(8, 8), cells_per_block=(2, 2), orientations=9, visualize=True)
    return features

# Function to generate occlusion heatmap
def occlusion_sensitivity(image_path, patch_size=10):
    original_image = imread(image_path)
    original_image = resize(original_image, (128, 128))  # Resize for consistency

    # Get original prediction
    original_features = extract_hog(original_image).reshape(1, -1)
    original_prediction = svm_model.decision_function(original_features)

    # Correct heatmap dimensions
    heatmap_height = len(range(0, 128 - patch_size, patch_size))
    heatmap_width = len(range(0, 128 - patch_size, patch_size))
    heatmap = np.zeros((heatmap_height, heatmap_width))

    # Iterate with correct bounds
    for i_idx, i in enumerate(range(0, 128 - patch_size, patch_size)):
        for j_idx, j in enumerate(range(0, 128 - patch_size, patch_size)):
            occluded_image = original_image.copy()
            occluded_image[i:i+patch_size, j:j+patch_size] = 0  # Mask part of image

            occluded_features = extract_hog(occluded_image).reshape(1, -1)
            occluded_prediction = svm_model.decision_function(occluded_features)

            # Difference in prediction confidence
            importance = original_prediction - occluded_prediction
            heatmap[i_idx, j_idx] = importance.item()

    # Normalize heatmap
    heatmap = np.maximum(heatmap, 0)
    heatmap /= np.max(heatmap)

    # Display results
    plt.figure(figsize=(8, 4))
    plt.subplot(1, 2, 1)
    plt.imshow(original_image)
    plt.title("Original Image")
    plt.axis("off")

    plt.subplot(1, 2, 2)
    plt.imshow(heatmap, cmap="jet", alpha=0.75, extent=[0, 128, 128, 0])  # Match image size
    plt.title("Feature Importance Heatmap")
    plt.axis("off")

    plt.show()

# Run the visualization
image_path = ("test-images/marcus.jpg")
#training-data/PetImages/Dog/10.jpg
occlusion_sensitivity(image_path)
