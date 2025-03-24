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

# Load the trained SVM model
with open("svm_model.pkl", "rb") as model_file_svm:
    svm_model = pickle.load(model_file_svm) 
print("SVM model loaded successfully!")

with open("rf_model.pkl", "rb") as model_file_rf:
    rf_model = pickle.load(model_file_rf)
print("RF model loaded successfully!")

# Function to preprocess and extract HOG features from a single image
def preprocess_single_image(image):
    img = imageio.imread(image) if isinstance(image, str) else imageio.imread(image)  # Load image
    img_resized = resize(img, (128, 128), anti_aliasing=True)  # Resize to 128x128
    img_gray = rgb2gray(img_resized)  # Convert to grayscale

    features, hog_image = hog(img_gray, pixels_per_cell=(8, 8), cells_per_block=(2, 2), orientations=9, visualize=True, block_norm='L2-Hys')
    hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))

    return create_overlay_image(img_resized, hog_image_rescaled), img_resized, features.reshape(1,-1)

def occlusion_sensitivity(model, original_features, original_pred, img_resized, class_type):
    """
    Generate an occlusion sensitivity heatmap for Random Forest or SVM models.
    Shows which parts of the image are most important for classification.
    
    Args:
        model: Trained classifier model (RF or SVM)
        original_features: Pre-extracted HOG features
        original_pred: Numeric prediction (0 for Cat, 1 for Dog)
        img_resized: Pre-resized image
        class_type: Type of classifier ("SVM" or "RF")
        
    Returns:
        Base64 encoded string of the heatmap image
    """
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

        # Calculate the difference in confidence
        diff = original_confidence - occluded_confidence
            
        return x, y, diff

    with ThreadPoolExecutor() as executor:
        results = list(executor.map(process_patch, coords))

    heatmap = np.zeros((128, 128))
    
    for x, y, diff in results:
        heatmap[y:y+patch_size, x:x+patch_size] += diff
    
    heatmap = (heatmap - np.min(heatmap)) / (np.max(heatmap) - np.min(heatmap) + 1e-10)

    return create_overlay_image(img_resized, heatmap)

def create_overlay_image(base_img, overlay):
    plt.figure(figsize=(5, 5))
    plt.imshow(base_img)
    plt.imshow(overlay, cmap='jet', alpha=0.5)
    plt.axis('off')
    
    # Save the figure to a buffer
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    plt.close()
    return base64.b64encode(buf.getvalue()).decode('utf-8')

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