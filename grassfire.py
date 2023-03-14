from random import randrange

import cv2
import queue
import numpy as np
import utils


# This is a simple implementation of the Grassfire algorithm
class Grassfire:
    def __init__(self, image_path, neighborhood=8):
        self.image_path = image_path
        self.neighborhood = neighborhood
        self.image = cv2.imread(self.image_path)
        self.nrows = self.image.shape[0]
        self.ncols = self.image.shape[1]
        self.last_visited_pixel = (0, 0)

        self.segments = np.zeros((self.nrows, self.ncols, 3), dtype=np.uint8)
        self.pixels_queue = queue.Queue()

    def showImage(self):
        self.startChecking()

    def startChecking(self):
        seed_pixel = self.findNextUnvisitedPixel()

        while seed_pixel[0] >= 0 and seed_pixel[1] >= 0:
            self.generateSegment(seed_pixel, self.generateId())
            seed_pixel = self.findNextUnvisitedPixel()

        utils.displayImage(self.segments, self.image_path)

    def generateSegment(self, seedPixel, segmentId):
        print("Generating segment id {}".format(segmentId))
        self.pixels_queue.queue.clear()
        self.pixels_queue.put(seedPixel)

        while not self.pixels_queue.empty():
            row, column = self.pixels_queue.get()
            self.segments[row, column] = segmentId
            self.checkPixelNeighborhood(row, column)

    @staticmethod
    def generateId():
        return randrange(1, 255), randrange(1, 255), randrange(1, 255)

    def findNextUnvisitedPixel(self):
        for row in range(self.last_visited_pixel[0], self.nrows):
            for column in range(self.last_visited_pixel[1], self.ncols):
                if not self.isPixelVisited(row, column):
                    if self.last_visited_pixel[0] == row:
                        self.last_visited_pixel = (row, column)
                    else:
                        self.last_visited_pixel = (row, 0)
                    return row, column
        return -1, -1

    def checkPixelNeighborhood(self, row, column):
        # A B C
        # D E F   -> E is the pixel at [row, column]
        # G H I

        # Check D
        if column > 0:
            self.analyzePixels(row, column, row, column - 1)

        # Check H
        if row + 1 < self.nrows:
            self.analyzePixels(row, column, row + 1, column)

        # Check F
        if column + 1 < self.ncols:
            self.analyzePixels(row, column, row, column + 1)

        # Check B
        if row > 0:
            self.analyzePixels(row, column, row - 1, column)

        # If 8-neighbourhood
        if self.neighborhood == 8:
            # Check A
            if row > 0 and column > 0:
                self.analyzePixels(row, column, row - 1, column - 1)

            # Check C
            if row > 0 and column + 1 < self.ncols:
                self.analyzePixels(row, column, row - 1, column + 1)

            # Check G
            if row + 1 < self.nrows and column > 0:
                self.analyzePixels(row, column, row + 1, column - 1)

            # Check I
            if row + 1 < self.nrows and column + 1 < self.ncols:
                self.analyzePixels(row, column, row + 1, column + 1)

    def analyzePixels(self, row, column, row_neighbour, column_neighbour):
        should_analyze = not self.isPixelVisited(row_neighbour, column_neighbour) and self.isSamePixel(
            self.image[row, column], self.image[row_neighbour, column_neighbour])

        if should_analyze:
            self.segments[row_neighbour, column_neighbour] = self.segments[row, column]
            self.pixels_queue.put((row_neighbour, column_neighbour))

    def isPixelVisited(self, row, column):
        return (self.segments[row, column] > 0).all()

    @staticmethod
    def isSamePixel(pixel1, pixel2):
        return (pixel1 == pixel2).all()
