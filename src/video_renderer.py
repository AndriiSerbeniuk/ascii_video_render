#!/usr/bin/env python3
"""
    A renderer that prints videos in characters.
"""
import argparse
from os.path import exists

import cv2

import img_renderer

class RenderCtx:
    def __init__(self, vidPath: str, renderedPath: str) -> None:
        self.vidPath = vidPath
        self.renderedPath = renderedPath

        # TODO: make these configurable
        # render settings
        self.targetWidth = 40
        self.charsRange = [ " ", ".", ",", "_", "-", "\'", "^", "*", ":", "!", "i", "|", "@", "#" ]

        # cli print settings
        self.printStep = 100

def renderVideo(ctx: RenderCtx):
    videoCapture = cv2.VideoCapture(ctx.vidPath)

    if not videoCapture.isOpened():
        print("Couldn't open the target file")
        exit(1)

    ret, frame = videoCapture.read()

    if ret == False:
        print("Error while reading from the file")
        videoCapture.release()
        exit(1)

    # TODO: remove when will figure out how to keep original aspect ratio
    targetWidth = ctx.targetWidth
    targetHeight = round(frame.shape[1] * (targetWidth / frame.shape[0]))
    targetHeight = targetHeight
    targetWidth *= 4

    imgRenderer = img_renderer.Renderer(charsRange = ctx.charsRange)

    frameRate = int(videoCapture.get(cv2.CAP_PROP_FPS))
    frameCount = int(videoCapture.get(cv2.CAP_PROP_FRAME_COUNT))
    print("Opened a video file with {} frames at {} FPS".format(frameCount, frameRate))

    renderedVid = ""
    prevPercent = -1
    idx = 1
    done = 0

    while(videoCapture.isOpened() and ret == True):
        rendered = imgRenderer.render(frame, (targetWidth, targetHeight))
        renderedVid += rendered
        renderedVid += "\n"

        # TODO: optional realtime preview?

        if idx == ctx.printStep:
            percent = int(done / frameCount * 100)
            if percent > prevPercent:
                print(percent, "% done")
                prevPercent = percent
            idx = 1
        else:
            idx += 1
        done += 1

        ret, frame = videoCapture.read()

    videoCapture.release()

    # save to a file
    f = open(ctx.renderedPath, "w")
    f.write(str(frameRate) + "\n\n")
    f.write(renderedVid)
    f.close()

    print("100% done, ", done, " frames")


def main():
    argParser = argparse.ArgumentParser(description="\"ascii video\"\
        renderer", add_help=True)

    argParser.add_argument("target", type=str, help="Video file to process")
    argParser.add_argument("output", type=str, help="Rendered result file")
    argParser.add_argument("-f", "--force", action="store_true", help="Forcefully\
        overwrite the result file if it already exists")

    args = argParser.parse_args()

    vPath = args.target
    if not exists(vPath):
        print("Specified target doesn't exist")
        exit(1)

    rendPath = args.output
    if not args.force and exists(rendPath):
        print("Warning: Specified result file already exists.\n\
            Run with -f to overwrite it.")
        exit(1)

    rendCtx = RenderCtx(vPath, rendPath)

    renderVideo(rendCtx)


if __name__ == "__main__":
    main()
