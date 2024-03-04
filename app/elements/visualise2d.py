import matplotlib.pyplot as plt
import cv2
import io
import os
import glob
import random
import numpy as np

# visualise the index-th image in the directory, it will firstly try search tiff then png files
def visualise2d_from_dir(directory):
    has_image = True
    images = glob.glob(os.path.join(directory,'*.tiff'))
    if len(images) == 0:
        images = glob.glob(os.path.join(directory,'*.png'))
        # a ValueError will occur if the images list is empty, or otherwise a random image is picked to show
    index = random.randrange(len(images))
    visualised_image = cv2.imread(images[index], cv2.IMREAD_UNCHANGED)

    # convert the data into iostream, so that pysimplegui can load
    plt.imshow(visualised_image)
    buf = io.BytesIO()
    plt.savefig(buf, format='png', transparent=True, bbox_inches='tight')
    buf.seek(0)
    visualised_image_iostream = cv2.imdecode(np.asarray(bytearray(buf.read()), dtype=np.uint8), cv2.IMREAD_COLOR)
    visualised_image_iostream = cv2.imencode('.png', visualised_image_iostream)[1].tobytes()
    
    return visualised_image_iostream