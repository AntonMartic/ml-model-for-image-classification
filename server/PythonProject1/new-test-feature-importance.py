import numpy as np
import matplotlib.pyplot as plt
from skimage.io import imread
from skimage.transform import resize
from skimage.color import rgb2gray
from skimage.feature import hog
import io
import base64


def extract_hog(img):
    """Extract HOG features from an image"""
    if len(img.shape) > 2 and img.shape[2] > 1:
        img = rgb2gray(img)
    features = hog(img, pixels_per_cell=(8, 8), cells_per_block=(2, 2), orientations=9)
    return features


def occlusion_sensitivity_test(image_path, model, patch_size=16, stride=8, display=True):
    """
    Generate and display an occlusion sensitivity heatmap for testing in PyCharm.

    Args:
        image_path: Path to the image file
        model: Trained classifier model
        patch_size: Size of the occlusion patch
        stride: Step size for sliding the occlusion patch
        display: Whether to display the plot (set to True for PyCharm testing)

    Returns:
        heatmap: The computed sensitivity heatmap
        base64_str: Base64 encoded string of the heatmap image
    """
    # Read and preprocess the original image
    img = imread(image_path)
    img_resized = resize(img, (128, 128), anti_aliasing=True)

    # Extract HOG features from original image
    original_gray = rgb2gray(img_resized) if len(img_resized.shape) > 2 else img_resized
    original_features = extract_hog(original_gray)

    # Get the original prediction and confidence
    original_features_reshaped = original_features.reshape(1, -1)
    original_pred = model.predict(original_features_reshaped)[0]
    original_confidence = model.decision_function(original_features_reshaped)[0]

    # Create a heatmap of the same size as the resized image
    heatmap = np.zeros((128, 128))

    # Slide the occlusion patch over the image
    for y in range(0, 128 - patch_size + 1, stride):
        for x in range(0, 128 - patch_size + 1, stride):
            # Create a copy of the original image
            occluded_img = img_resized.copy()

            # Apply occlusion (gray patch)
            occluded_img[y:y + patch_size, x:x + patch_size] = 0.5

            # Convert to grayscale and extract HOG features
            occluded_gray = rgb2gray(occluded_img) if len(occluded_img.shape) > 2 else occluded_img
            occluded_features = extract_hog(occluded_gray)

            # Get the prediction for the occluded image
            occluded_confidence = model.decision_function(occluded_features.reshape(1, -1))[0]

            # Calculate the difference in confidence
            diff = original_confidence - occluded_confidence

            # Update the heatmap
            heatmap[y:y + patch_size, x:x + patch_size] += diff

    # Normalize the heatmap
    heatmap = (heatmap - np.min(heatmap)) / (np.max(heatmap) - np.min(heatmap) + 1e-10)

    # Create a figure and plot the heatmap
    plt.figure(figsize=(10, 5))

    plt.subplot(1, 2, 1)
    plt.imshow(img_resized)
    plt.title("Original Image")
    plt.axis('off')

    plt.subplot(1, 2, 2)
    plt.imshow(img_resized)
    plt.imshow(heatmap, cmap='jet', alpha=0.5)
    plt.title('Classification Sensitivity Heatmap')
    plt.axis('off')

    # Save the figure to a buffer
    buf = io.BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight')
    buf.seek(0)

    # Convert to base64
    base64_str = base64.b64encode(buf.getvalue()).decode('utf-8')

    # Display the plot if requested
    if display:
        plt.tight_layout()
        plt.show()
    else:
        plt.close()

    return heatmap, base64_str


# Example usage:
if __name__ == "__main__":
    # Replace with your actual model and image path
    import pickle

    # Load SVM model
    #svm_model.pkl
    with open("svm_model.pkl", "rb") as model_file:
        svm_model = pickle.load(model_file)

    # Test the function with an image
    image_path = "test-images/dog1-test.jpg"
    heatmap, base64_str = occlusion_sensitivity_test(image_path, svm_model)

    print("Heatmap generation complete!")
    # You could save the heatmap if needed
    # plt.imsave("heatmap_output.png", heatmap, cmap='jet')