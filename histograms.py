import numpy as np
import matplotlib.pyplot as plt
from PIL import Image

IMAGE_SIZE = 600

def build_histogram(filename, col):
    img = Image.open(filename)
    data = np.array(img, dtype=np.uint8).ravel()
    plt.hist(data, bins=256, color=col)
    plt.show()

build_histogram('images/red.jpg', 'red')
build_histogram('images/green.jpg', 'green')
build_histogram('images/blue.jpg', 'blue')
