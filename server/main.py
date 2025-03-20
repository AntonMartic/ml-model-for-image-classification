import pickle
import numpy as np
from skimage.io import imread
from skimage.transform import resize
from skimage.color import rgb2gray
from skimage.feature import hog
from skimage import exposure
import matplotlib.pyplot as plt
import io
import base64

# Load the trained SVM model
with open("PythonProject1/svm_model.pkl", "rb") as model_file:
    svm_model = pickle.load(model_file) 

print("SVM model loaded successfully!")

# Function to preprocess and extract HOG features from a single image
def preprocess_single_image(image):
    img = imread(image) if isinstance(image, str) else imread(image, plugin="matplotlib")  
    img_resized = resize(img, (128, 128), anti_aliasing=True)
    img_gray = rgb2gray(img_resized)

    features = hog(img_gray, pixels_per_cell=(8, 8), cells_per_block=(2, 2), orientations=9)
    return {"features": features.reshape(1, -1), "img_resized": img_resized}  # Returnera dictionary

def occlusion_sensitivity(model, preprocessed_data, patch_size=16, stride=8):
    img_resized = preprocessed_data["img_resized"]
    original_features = preprocessed_data["features"]

    original_confidence = model.decision_function(original_features)[0]
    heatmap = np.zeros((128, 128))

    for y in range(0, 128 - patch_size + 1, stride):
        for x in range(0, 128 - patch_size + 1, stride):
            occluded_img = img_resized.copy()
            occluded_img[y:y+patch_size, x:x+patch_size] = 0.5

            occluded_gray = rgb2gray(occluded_img)
            occluded_features = hog(occluded_gray, pixels_per_cell=(8, 8), 
                                    cells_per_block=(2, 2), orientations=9)

            occluded_confidence = model.decision_function(occluded_features.reshape(1, -1))[0]
            heatmap[y:y+patch_size, x:x+patch_size] += original_confidence - occluded_confidence

    heatmap = (heatmap - np.min(heatmap)) / (np.max(heatmap) - np.min(heatmap) + 1e-10)

    plt.figure(figsize=(5, 5))
    plt.imshow(img_resized)
    plt.imshow(heatmap, cmap='jet', alpha=0.5)
    plt.axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    plt.close()
    
    return base64.b64encode(buf.getvalue()).decode('utf-8')

def visualize_hog_features(preprocessed_data):
    img_resized = preprocessed_data["img_resized"]

    img_gray = rgb2gray(img_resized)
    _, hog_image = hog(img_gray, pixels_per_cell=(8, 8), cells_per_block=(2, 2), 
                       orientations=9, visualize=True, block_norm='L2-Hys')

    hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))

    plt.figure(figsize=(5, 5))
    plt.imshow(img_resized)
    plt.imshow(hog_image_rescaled, cmap='jet', alpha=0.5)
    plt.axis('off')

    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    plt.close()

    return base64.b64encode(buf.getvalue()).decode('utf-8')