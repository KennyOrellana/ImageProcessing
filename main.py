from boundary_extraction import boundaryExtraction
from grassfire import Grassfire
from utils import readImages
from watershed import watershed

# Load all images paths
imagesPaths = readImages()


def applyBoundaryExtraction():
    # Apply boundary extraction to each image
    for image in imagesPaths:
        boundaryExtraction(image, 4)


def applyGrassfire():
    Grassfire("images/particles.png").showImage()
    # for image in imagesPaths:
    #     Grassfire(image, 8).showImage()


def applyWatershed():
    watershed("images/coffee_grains.jpg", "images/coffee_markers.png")


# applyWatershed()
# applyBoundaryExtraction()
applyGrassfire()
