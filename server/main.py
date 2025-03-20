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
    img = imread(image) if isinstance(image, str) else imread(image, plugin="matplotlib")  # Läser antingen från sökväg eller bytes
    img_resized = resize(img, (128, 128), anti_aliasing=True)
    img_gray = rgb2gray(img_resized)

    features = hog(img_gray, pixels_per_cell=(8, 8), cells_per_block=(2, 2), orientations=9)
    return features.reshape(1, -1), img_resized  # Returnerar feature-vektor

def occlusion_sensitivity(image_file, model, preprocess_func, patch_size=16, stride=8):
    """
    Generate an occlusion sensitivity heatmap to visualize which parts of the image
    are most important for classification.
    
    Args:
        image_file: Image file object or path
        model: Trained classifier model
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
    
    img = imread(image_file) if isinstance(image_file, str) else imread(image_file, plugin="matplotlib")
    img_resized = resize(img, (128, 128), anti_aliasing=True)
    
    # Get the original prediction
    original_pred = model.predict(original_features)[0]
    
    # Create a heatmap of the same size as the resized image
    heatmap = np.zeros((128, 128))
    
    # Calculate the decision function (confidence score) for the original image
    original_confidence = model.decision_function(original_features)[0]
    
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
            
            # Get the prediction for the occluded image
            occluded_confidence = model.decision_function(occluded_features.reshape(1, -1))[0]
            
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
    img = imread(image_file) if isinstance(image_file, str) else imread(image_file, plugin="matplotlib")
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
    plt.imshow(hog_image_rescaled, cmap='viridis')
    plt.axis('off')
    
    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)
    plt.close()
    
    # Convert to base64
    hog_viz_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
    
    return hog_viz_base64