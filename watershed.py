import cv2
import numpy as np

from utils import displayImage


def watershed(image_path, marker_path):
    # image = cv2.imread(image_path)
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    mark = cv2.imread(marker_path)
    #
    # ret, markers = cv2.connectedComponents(marker)
    # ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)
    #
    #
    # markers = markers + 1
    # displayImage(markers, "Markers")
    # # markers[unknown == 255] = 0
    #
    # result = cv2.watershed(gray, markers)
    # displayImage(result, image_path)

    img = cv2.imread(image_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding to the grayscale image
    ret, thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

    # Perform morphological operations to remove any noise and fill any gaps in the image
    kernel = np.ones((3, 3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, 2)
    sure_bg = cv2.dilate(opening, kernel, 3)

    # Find the distance transform of the image and normalize it
    dist_transform = cv2.distanceTransform(opening, cv2.DIST_L2, 5)
    ret, sure_fg = cv2.threshold(dist_transform, 0.7 * dist_transform.max(), 255, 0)

    # Subtract the foreground from the background to obtain the unknown region
    sure_fg = np.uint8(sure_fg)
    unknown = cv2.subtract(sure_bg, sure_fg)

    # Label the markers in the image
    ret, markers = cv2.connectedComponents(sure_fg)

    # Add 1 to all marker labels to make sure the background is 1, not 0
    markers = mark.copy()
    markers = markers + 1

    # Set the unknown region to 0 in the marker image
    markers[unknown == 255] = 0

    # Apply watershed to the image using the marker image
    markers = cv2.watershed(img, markers)

    # Apply a color map to the result and display it
    img[markers == -1] = [255, 0, 0]
    cv2.imshow('Segmented Image', img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
