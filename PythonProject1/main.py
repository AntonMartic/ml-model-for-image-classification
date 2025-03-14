
import numpy as np
import matplotlib.pyplot as plt
#import matplotlib.image as mpimg
#from skimage.feature import hog
from skimage.color import rgb2gray
from skimage.io import imread
from skimage.transform import resize

x = np.arange(0,1,0.01)
print(x)

# Create image directories
cat_dir ="training-data/PetImages/Cat"
cat_dog ="training-data/PetImages/Dog"

# test resize and grayscale for a single image
img_path = "training-data/PetImages/Cat/1.jpg"
img = imread(img_path)  # Load the image
img_resized = resize(img, (128, 128))  # Resize
img_gray = rgb2gray(img_resized)  # Convert to grayscale

plt.imshow(img)
plt.imshow(img_resized)
plt.imshow(img_gray)
plt.show()
