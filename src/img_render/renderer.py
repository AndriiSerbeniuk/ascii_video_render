"""
    Code for image processing and rendering into text.
"""
import cv2

from typing import Sequence, Tuple
from cv2 import Mat

class ImageProcessor:
    def __init__(self, width: int = 0, height: int = 0, contrast: float = 1.4,\
        brightness: float = 0) -> None:
        self.targetWidth = width
        self.targetHeight = height
        self.contrast = contrast
        self.brigtness = brightness

    def process(self, image: Mat) -> Mat:
        # Grayscale
        processed = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Contrast
        processed = cv2.convertScaleAbs(processed, alpha=self.contrast,\
            beta=self.brigtness)

        # Blur
        processed = cv2.GaussianBlur(processed, (7, 7), 0) # TODO: make sense of these args

        # Resize
        processed = cv2.resize(processed, (self.targetWidth,\
            self.targetHeight), interpolation = cv2.INTER_AREA)

        return processed

class Renderer:
    defaultChars = [ " ", ".", ",", "_", "-", "\'", "^", "*", ":", "!", "i",\
        "l", "z", "k", "F", "@", "#" ]

    def __init__(self, charsRange: Sequence[str] = defaultChars) -> None:
        self.processor = ImageProcessor()
        self.charsRange = charsRange

    # map brightness to a character
    # returns a character mapped to the brightness level
    def charByBrightness(self, brightness: int):
        # TODO: brightness value check
        charsNum = len(self.charsRange)
        # TODO: revisit this equation later
        idx = round((brightness * charsNum) / 255)
        #idx = charsNum - idx    # color inverse

        if idx < 0:
            idx = 0
        elif idx >= charsNum:
            idx = charsNum - 1

        return self.charsRange[idx]

    # Input - raw image, rendered image size
    def render(self, image: Mat, size: Tuple[int, int]) -> str:
        # TODO: add size checks
        self.processor.targetWidth = size[0]
        self.processor.targetHeight = size[1]

        processed = self.processor.process(image)
        h, w = processed.shape
        imgStr = ""

        # TODO: rewrite properly and make faster if possible
        for row in range(0, h):
            for col in range(0, w):
                imgStr += self.charByBrightness(processed[row, col])
            imgStr += "\n"

        return imgStr
