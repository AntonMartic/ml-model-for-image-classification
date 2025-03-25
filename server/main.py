import pickle
import numpy as np
import imageio
from skimage.transform import resize
from skimage.color import rgb2gray
from skimage.feature import hog
from skimage import exposure
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from io import BytesIO
import base64
from concurrent.futures import ThreadPoolExecutor
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load the trained SVM model with memory optimization
def load_model(filepath):
    try:
        with open(filepath, "rb") as model_file:
            model = pickle.load(model_file)
        logger.info(f"Model loaded successfully from {filepath}")
        return model
    except Exception as e:
        logger.error(f"Error loading model from {filepath}: {e}")
        return None

svm_model = load_model("svm_model.pkl")
rf_model = load_model("rf_model.pkl")

# Function to preprocess and extract HOG features from a single image
def preprocess_single_image(image):
    try:
        img = imageio.imread(image)
        img_resized = resize(img, (128, 128), anti_aliasing=True)
        img_gray = rgb2gray(img_resized)

        features, hog_image = hog(img_gray, pixels_per_cell=(8, 8), cells_per_block=(2, 2), orientations=9, visualize=True, block_norm='L2-Hys')
        hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))

        overlay = create_overlay_image(img_resized, hog_image_rescaled)

        del img_gray, hog_image, img

        return overlay, img_resized, features.reshape(1, -1)
        
    except Exception as e:
        logger.error(f"Error in image preprocessing: {e}")
        raise

def occlusion_sensitivity(model, original_features, original_pred, img_resized, class_type):
    try:
        patch_size = 16
        stride = 8
    
        # Get the original confidence score
        # Different models have different methods for confidence scores
        if class_type == "SVM":
            # SVM has decision_function
            original_confidence = model.decision_function(original_features)[0]
        else:
            # Random Forest has predict_proba
            original_proba = model.predict_proba(original_features)[0]
            # Use probability of predicted class as confidence
            original_confidence = original_proba[original_pred]

        coords = [(x, y) 
              for y in range(0, 128 - patch_size + 1, stride)
              for x in range(0, 128 - patch_size + 1, stride)]
    
        def process_patch(coords):
            x, y = coords
        
            occluded_img = img_resized.copy()
            occluded_img[y:y+patch_size, x:x+patch_size] = 0.5
        
            occluded_gray = rgb2gray(occluded_img)
            occluded_features = hog(occluded_gray, pixels_per_cell=(8, 8), cells_per_block=(2, 2), orientations=9)
        
            if class_type == "SVM":
                occluded_confidence = model.decision_function(occluded_features.reshape(1, -1))[0]
                # Handle multi-class case
                if isinstance(occluded_confidence, np.ndarray) and len(occluded_confidence) > 1:
                    if original_pred == 1:  # If predicted class is positive (Dog)
                        occluded_confidence = occluded_confidence[1]
                    else:
                        occluded_confidence = -occluded_confidence[0]
            else:
                occluded_proba = model.predict_proba(occluded_features.reshape(1, -1))[0]
                occluded_confidence = occluded_proba[original_pred]

            # Cleanup memory
            del occluded_img, occluded_gray, occluded_features
            
            return x, y, original_confidence - occluded_confidence

        with ThreadPoolExecutor() as executor:
            results = list(executor.map(process_patch, coords))

        heatmap = np.zeros((128, 128))
        for x, y, diff in results:
            heatmap[y:y+patch_size, x:x+patch_size] += diff
    
        heatmap = (heatmap - np.min(heatmap)) / (np.max(heatmap) - np.min(heatmap) + 1e-10)

        heatmap_overlay = create_overlay_image(img_resized, heatmap)

        del coords, results, heatmap, patch_size, stride, original_confidence
        return heatmap_overlay
    
    except Exception as e:
        logger.error(f"Error in occlusion sensitivity: {e}")
        raise

def create_overlay_image(base_img, overlay):
    try:
        plt.figure(figsize=(5, 5))
        plt.imshow(base_img)
        plt.imshow(overlay, cmap='jet', alpha=0.5)
        plt.axis('off')
    
        # Save to buffer
        buf = BytesIO()
        plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
        buf.seek(0)

        # Encode and cleanup
        encoded = base64.b64encode(buf.getvalue()).decode('utf-8')

        plt.close()

        # Cleanup memory
        del buf, overlay
        return encoded
    
    except Exception as e:
        logger.error(f"Error creating overlay image: {e}")
        raise

def occlusion_sensitivity_old(model, original_features, original_pred, img_resized, class_type):
    patch_size = 16
    stride = 8
    
    # Create a heatmap of the same size as the resized image
    heatmap = np.zeros((128, 128))

    # Get the original confidence score
    # Different models have different methods for confidence scores
    if class_type == "SVM":
        # SVM has decision_function
        original_confidence = model.decision_function(original_features)[0]
    else:
        # Random Forest has predict_proba
        original_proba = model.predict_proba(original_features)[0]
        # Use probability of predicted class as confidence
        original_confidence = original_proba[original_pred]

    for y in range(0, 128 - patch_size + 1, stride):
        for x in range(0, 128 - patch_size + 1, stride):
            # Create a copy of the original image
            occluded_img = img_resized.copy()
            
            # Apply occlusion (gray patch)
            occluded_img[y:y+patch_size, x:x+patch_size] = 0.5
            
            # Convert to grayscale and extract HOG features
            occluded_gray = rgb2gray(occluded_img)
            occluded_features = hog(occluded_gray, pixels_per_cell=(8, 8), 
                                   cells_per_block=(2, 2), orientations=9)

            if class_type == "SVM":
                occluded_confidence = model.decision_function(occluded_features.reshape(1, -1))[0]
                # Handle multi-class case
                if isinstance(occluded_confidence, np.ndarray) and len(occluded_confidence) > 1:
                    if original_pred == 1:  # If predicted class is positive (Dog)
                        occluded_confidence = occluded_confidence[1]
                    else:
                        occluded_confidence = -occluded_confidence[0]
            else:
                occluded_proba = model.predict_proba(occluded_features.reshape(1, -1))[0]
                occluded_confidence = occluded_proba[original_pred]
            
            diff = original_confidence - occluded_confidence
            heatmap[y:y+patch_size, x:x+patch_size] += diff
    
    # Normalize the heatmap
    heatmap = (heatmap - np.min(heatmap)) / (np.max(heatmap) - np.min(heatmap) + 1e-10)
    
    return create_overlay_image(img_resized, heatmap)