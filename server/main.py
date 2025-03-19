import pickle
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from skimage.color import rgb2gray
from skimage.feature import hog

# Load the trained SVM model
with open("PythonProject1/svm_model.pkl", "rb") as model_file:
    svm_model = pickle.load(model_file)

print("SVM model loaded successfully!")

# Function to preprocess and extract HOG features from a single image
def preprocess_single_image(image):
    img = imread(image) if isinstance(image, str) else imread(image, plugin="matplotlib")  # Läser antingen från sökväg eller bytes
    img_resized = resize(img, (128, 128), anti_aliasing=True)
    img_gray = rgb2gray(img_resized)

    features = hog(img_gray, pixels_per_cell=(8, 8), cells_per_block=(2, 2), orientations=9)
    return features.reshape(1, -1), img_resized  # Returnerar feature-vektor
