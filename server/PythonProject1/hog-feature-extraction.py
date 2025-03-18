import os
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
from skimage.feature import hog
from skimage.color import rgb2gray
from skimage.io import imread
from skimage.transform import resize
from skimage.util import img_as_float
import pickle

#### TEST ####
# test resize, grayscale and hog features for a single image

img_path_test = "training-data/PetImages/Cat/1.jpg"
img_test = imread(img_path_test)  # Load the image
img_resized_test = resize(img_test, (128, 128), anti_aliasing=True)  # Resize
img_gray_test = img_as_float(rgb2gray(img_resized_test))  # Convert to grayscale & normalize (ensuring pixel values are between 0 and 1)

# Extract HOG features and visualize
hog_features_test, hog_image_test = hog(img_gray_test, pixels_per_cell=(8, 8),
                              cells_per_block=(2, 2), orientations=9,
                              visualize=True)


fig, ax = plt.subplots(1, 3, figsize=(15, 5))

ax[0].imshow(img_test)
ax[0].set_title("Original Image")
ax[0].axis("off")

ax[1].imshow(img_gray_test, cmap="gray")
ax[1].set_title("Grayscale Image")
ax[1].axis("off")

ax[2].imshow(hog_image_test, cmap="gray")
ax[2].set_title("HOG Features")
ax[2].axis("off")

plt.show()




#### HOG feature extraction for all cats and dogs ####

# Create image directories
cat_dir ="training-data/PetImages/Cat"
dog_dir ="training-data/PetImages/Dog"

# Ensure the HOG feature directory exists
hog_dir = "hog_features"
os.makedirs(hog_dir, exist_ok=True)

# Image settings
img_size = (128, 128)  # Resize images to a fixed size
batch_size = 1000  # Number of images per file

# Lists to store features and labels
X = []
y = []
file_index = 1  # File counter

# Function to process images and extract HOG features
def process_images(directory, label):
    global X, y, file_index  # Use global to update lists across function calls
    for filename in os.listdir(directory):
        img_path = os.path.join(directory, filename)

        # Ignore non-image files
        if not filename.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        try:
            # Load, resize, convert to grayscale, normalize
            img = imread(img_path)
            img_resized = resize(img, img_size, anti_aliasing=True)
            img_gray = img_as_float(rgb2gray(img_resized))

            # Extract HOG features
            features = hog(img_gray, pixels_per_cell=(8, 8),
                           cells_per_block=(2, 2), orientations=9)

            # Append to dataset
            X.append(features)
            y.append(label)

            # Save in batches of batch_size
            if len(X) >= batch_size:
                save_features(X, y, file_index)
                file_index += 1
                X, y = [], []  # Reset lists

        except Exception as e:
            print(f"Skipping {img_path} due to error: {e}")

# Function to save features to a file
def save_features(X, y, index):
    filename = os.path.join(hog_dir, f"hog_features_part_{index}.pkl")
    with open(filename, "wb") as f:
        pickle.dump((np.array(X), np.array(y)), f)
    print(f"Saved {len(X)} samples to {filename}")

# Process images
process_images(cat_dir, 0)  # Cats → Label 0
process_images(dog_dir, 1)  # Dogs → Label 1

# Save remaining data if any
if X:
    save_features(X, y, file_index)

print("All HOG features and labels saved in multiple files.")

"""

# Convert to NumPy arrays
X = np.array(X)
y = np.array(y)

# Print dataset shape
print(f"Feature matrix shape: {X.shape}")  # Should be (num_samples, feature_length)
print(f"Labels shape: {y.shape}")          # Should be (num_samples,)

# Save to pickle file at the end
with open("hog_features.pkl", "wb") as f:
    pickle.dump((X, y), f)

print("HOG features and labels saved to hog_features.pkl")

"""
