import PIL
from PIL import Image
import numpy as np
import sys
import subprocess

# Print out versions
print("Python version: ", sys.version)
print("PIL version:", PIL.__version__)
print("numpy version:", np.__version__)

# Print out CPU architecture
ps = subprocess.Popen('lscpu | grep -I "Architecture"', shell=True, stdout=subprocess.PIPE)
print("CPU architecture:", ps.communicate()[0])

# Make sure the file is exactly the same on different devices
ps = subprocess.Popen('md5sum lena.jpg', shell=True, stdout=subprocess.PIPE)
print("OS level data validation (md5sum):", ps.communicate()[0])

# Load and check the difference of loaded image
img = Image.open("lena.jpg")   # PIL object
img_np = np.array(img)         # Convert to numpy 3-D matrix
print("Image loaded. Data type:", img_np.dtype, ". Shape:", img_np.shape)  # What type of numpy array?
print("CheckSum: ", np.sum(img_np.astype("int")))   # Sum of all pixels
for k in range(3):                                  # Sum of all pixels in R, G, B channels
    print("  Channel-wise CheckSum[%d]: " %k, np.sum(img_np[:,:,k].astype("int")))

