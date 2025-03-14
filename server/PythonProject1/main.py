
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
from skimage.feature import hog
from skimage.color import rgb2gray
from skimage.io import imread
from skimage.transform import resize
from skimage.util import img_as_float


# create arrays
X = [] # features
y = [] # labels

# Create image directories
cat_dir ="training-data/PetImages/Cat"
dog_dir ="training-data/PetImages/Dog"

# test resize, grayscale and hog features for a single image
img_path = "training-data/PetImages/Cat/1.jpg"
img = imread(img_path)  # Load the image
img_resized = resize(img, (128, 128), anti_aliasing=True)  # Resize
img_gray = img_as_float(rgb2gray(img_resized))  # Convert to grayscale & normalize (ensuring pixel values are between 0 and 1)

# Extract HOG features and visualize
hog_features, hog_image = hog(img_gray, pixels_per_cell=(4, 4),
                              cells_per_block=(2, 2), orientations=9,
                              visualize=True)


fig, ax = plt.subplots(1, 3, figsize=(15, 5))

ax[0].imshow(img)
ax[0].set_title("Original Image")
ax[0].axis("off")

ax[1].imshow(img_gray, cmap="gray")
ax[1].set_title("Grayscale Image")
ax[1].axis("off")

ax[2].imshow(hog_image, cmap="gray")
ax[2].set_title("HOG Features")
ax[2].axis("off")

plt.show()


