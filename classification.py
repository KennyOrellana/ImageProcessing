import cv2
import numpy as np
from matplotlib import pyplot as plt


def main():
    image = loadImage()
    equalized_image = applyHistogramEqualizationTo(image)
    displayImages(image, equalized_image)


def loadImage():
    return cv2.imread('images/Lenna.png')


def applyHistogramEqualizationTo(img):
    hist, bins = np.histogram(img.flatten(), 256, [0, 256])
    cdf = hist.cumsum()
    cdf_normalized = cdf * float(hist.max()) / cdf.max()

    cdf_m = np.ma.masked_equal(cdf, 0)
    cdf_m = (cdf_m - cdf_m.min()) * 255 / (cdf_m.max() - cdf_m.min())
    cdf = np.ma.filled(cdf_m, 0).astype('uint8')
    img2 = cdf[img]

    plt.plot(cdf, color='m')
    plt.hist(img.flatten(), 256, [0, 256], color='y')

    plt.plot(cdf_normalized, color='b')
    plt.hist(img2.flatten(), 256, [0, 256], color='r')


    plt.xlim([0, 256])
    plt.legend(('cdf', 'histogram'), loc='upper left')
    plt.show()

    return img2


def displayImages(original, result):
    cv2.imshow("Original Image", original)
    cv2.imshow("Result", result)

    cv2.waitKey(0)
    cv2.destroyAllWindows()


main()
