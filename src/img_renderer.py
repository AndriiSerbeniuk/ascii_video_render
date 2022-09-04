"""
    Image processor that prints an image in text
"""
import argparse
from genericpath import exists
import cv2
from cv2 import Mat
from typing import List, Sequence, Tuple

class ImageProcessor:
    class ProcessingAction:
        def __init__(self) -> None:
            pass

        def process(self, image: Mat) -> Mat:
            pass

    class Grayscale(ProcessingAction):
        def __init__(self) -> None:
            super().__init__()

        def process(self, image: Mat) -> Mat:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        def processStatic(image: Mat) -> Mat:
            return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    class Contrast(ProcessingAction):
        def __init__(self, contrast: float, brightness: float) -> None:
            super().__init__()
            self.contrast = contrast
            self.brightness = brightness

        def process(self, image: Mat) -> Mat:
            return cv2.convertScaleAbs(image, alpha=self.contrast, beta=self.brightness)

    class Blur(ProcessingAction):
        def __init__(self) -> None:
            super().__init__()

        def process(self, image: Mat) -> Mat:
            return cv2.GaussianBlur(image, (7, 7), 0) # TODO: make sense of these args

    default_pipeline = [Contrast(1.4, 0)]

    def __init__(self, width: int = 0, height: int = 0, contrast: float = 1.4,\
        brightness: float = 0, pipeline: List[ProcessingAction] = default_pipeline) -> None:
        self.targetWidth = width
        self.targetHeight = height
        self.contrast = contrast
        self.brigtness = brightness
        self.pipeline = pipeline

    def process(self, image: Mat) -> Mat:
        processed = image

        for action in self.pipeline:
            processed = action.process(processed)

        # grayscaling is mandatory
        if len(processed.shape) > 2:
            processed = self.Grayscale.processStatic(processed)

        # cut to size
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

def main():
    argParser = argparse.ArgumentParser(description="ascii image printer",\
        add_help=False)

    argParser.add_argument("target", type=str, help="Image to process")
    argParser.add_argument("-w", type=int, help="Width of the resulting image")
    argParser.add_argument("-h", type=int, help="Height of the resulting image")

    args = argParser.parse_args()

    imgPath = args.target
    if not exists(imgPath):
        print("Specified target doesn't exist")
        exit(1)

    if args.w == None:
        width = 120 # arbitrary default value
    elif args.w <= 0:
        print("Width cannot be <= 0")
        exit(1)
    else:
        width = args.w

    if args.h == None:
        height = 60 # arbitrary default value
    elif args.h <= 0:
        print("Height cannot be <= 0")
        exit(1)
    else:
        height = args.h

    image = cv2.imread(imgPath)
    renderer = Renderer()
    rendered = renderer.render(image, (width, height))

    print(rendered)

if __name__ == "__main__":
    main()
