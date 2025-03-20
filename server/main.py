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
import io
import base64

# Load the trained SVM model
with open("PythonProject1/svm_model.pkl", "rb") as model_file_svm:
    svm_model = pickle.load(model_file_svm) 
print("SVM model loaded successfully!")

with open("PythonProject1/rf_model.pkl", "rb") as model_file_rf:
    rf_model = pickle.load(model_file_rf)
print("RF model loaded successfully!")

# Function to preprocess and extract HOG features from a single image
def preprocess_single_image(image):
    img = imageio.imread(image) if isinstance(image, str) else imageio.imread(image)  # Läser antingen från sökväg eller bytes
    img_resized = resize(img, (128, 128), anti_aliasing=True)
    img_gray = rgb2gray(img_resized)

    features = hog(img_gray, pixels_per_cell=(8, 8), cells_per_block=(2, 2), orientations=9)
    return features.reshape(1, -1), img_resized  # Returnerar feature-vektor

def occlusion_sensitivity(image_file, model, preprocess_func, patch_size=16, stride=8):
    """
    Generate an occlusion sensitivity heatmap for Random Forest or SVM models.
    Shows which parts of the image are most important for classification.
    
    Args:
        image_file: Image file object or path
        model: Trained classifier model (RF or SVM)
        preprocess_func: Function to preprocess image and extract features
        patch_size: Size of the occlusion patch
        stride: Step size for sliding the occlusion patch
        
    Returns:
        Base64 encoded string of the heatmap image
    """
    # Read and preprocess the original image
    original_features, original_img = preprocess_func(image_file)
    if hasattr(image_file, 'seek'):
        image_file.seek(0)  # Reset file pointer for reuse
    
    img = imageio.imread(image_file) if isinstance(image_file, str) else imageio.imread(image_file)
    img_resized = resize(img, (128, 128), anti_aliasing=True)
    
    # Get the original prediction
    original_pred = model.predict(original_features)[0]
    
    # Create a heatmap of the same size as the resized image
    heatmap = np.zeros((128, 128))
    
    # Get the original confidence score
    # Different models have different methods for confidence scores
    if hasattr(model, 'decision_function'):
        # SVM has decision_function
        original_confidence = model.decision_function(original_features)[0]
        
        # For binary classification with SVM
        if isinstance(original_confidence, np.ndarray) and len(original_confidence) > 1:
            # Multi-class SVM returns an array of scores per class
            if original_pred == 1:  # If predicted class is positive (Dog)
                original_confidence = original_confidence[1]  # Use positive class score
            else:
                original_confidence = -original_confidence[0]  # Negative of negative class score
    else:
        # Random Forest has predict_proba
        original_proba = model.predict_proba(original_features)[0]
        # Use probability of predicted class as confidence
        original_confidence = original_proba[original_pred]
    
    # Slide the occlusion patch over the image
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
            
            # Get the confidence score for the occluded image
            if hasattr(model, 'decision_function'):
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
            
            # Update the heatmap
            heatmap[y:y+patch_size, x:x+patch_size] += diff
    
    # Normalize the heatmap
    heatmap = (heatmap - np.min(heatmap)) / (np.max(heatmap) - np.min(heatmap) + 1e-10)
    
    # Create a figure and plot the heatmap
    plt.figure(figsize=(5, 5))
    plt.imshow(img_resized)
    plt.imshow(heatmap, cmap='jet', alpha=0.5)
    plt.axis('off')
    
    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    plt.close()
    
    # Convert to base64
    heatmap_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return heatmap_base64

def visualize_hog_features(image_file):
    """
    Generate a visualization of HOG features for an image and return as base64 encoded string.
    
    Args:
        image_file: Image file object or path
        
    Returns:
        Base64 encoded string of the HOG visualization image
    """
    # Read the image
    img = imageio.imread(image_file) if isinstance(image_file, str) else imageio.imread(image_file)
    if hasattr(image_file, 'seek'):
        image_file.seek(0)  # Reset file pointer for reuse
    
    # Resize image to match classifier's input size
    img_resized = resize(img, (128, 128), anti_aliasing=True)
    
    # Convert to grayscale
    img_gray = rgb2gray(img_resized)
    
    # Extract HOG features with visualization
    features, hog_image = hog(
        img_gray, 
        pixels_per_cell=(8, 8),
        cells_per_block=(2, 2), 
        orientations=9,
        visualize=True,
        block_norm='L2-Hys'
    )
    
    # Rescale the HOG image for better visualization
    hog_image_rescaled = exposure.rescale_intensity(hog_image, in_range=(0, 10))
    
    # Create a figure for the HOG visualization
    plt.figure(figsize=(5, 5))
    plt.imshow(img_resized)
    plt.imshow(hog_image_rescaled, cmap='jet', alpha=0.5)
    plt.axis('off')
    
    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', pad_inches=0)
    buf.seek(0)
    plt.close()
    
    # Convert to base64
    hog_viz_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return hog_viz_base64