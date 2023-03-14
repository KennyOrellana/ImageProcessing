import cv2
import numpy as np

import utils


def boundaryExtraction(image_path, kernel_size=3):
    kernel = np.ones((kernel_size, kernel_size), np.uint8)

    image = cv2.imread(image_path)
    base_image = image.copy()
    eroded_image = cv2.erode(image, kernel)
    result = cv2.subtract(base_image, eroded_image)

    utils.displayImage(result, image_path)


