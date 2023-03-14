import os

import cv2


def readImages():
    images_paths = []
    for file in os.listdir("images"):
        images_paths.append("images/" + file)

    return images_paths


def displayImage(image, name="Result"):
    # Displaying the image
    cv2.imshow(name, image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
