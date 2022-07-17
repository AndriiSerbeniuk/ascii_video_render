#!/usr/bin/env python3
import sys
from time import sleep

import cv2

import vid_meta as vm
import img_renderer

class RenderCtx:
    def __init__(self, vidPath: str, renderedPath: str) -> None:
        self.vidPath = vidPath
        self.renderedPath = renderedPath

        self.frameCount = vm.getFramesCount(vidPath)
        self.frameRate = vm.getFrameRate(vidPath)

        # TODO: make these configurable
        # render settings
        self.targetWidth = 40
        self.charsRange = [ " ", ".", ",", "_", "-", "\'", "^", "*", ":", "!", "i", "|", "@", "#" ]

        # cli print settings
        self.printStep = 100

def renderVideo(ctx: RenderCtx):
    videoCapture = cv2.VideoCapture(ctx.vidPath)
    ret, frame = videoCapture.read()

    if ret == False:
        print("Couldn't read a frame")
        videoCapture.release()
        exit()

    # TODO: remove when will figure out how to keep original aspect ratio
    targetWidth = ctx.targetWidth
    targetHeight = round(frame.shape[1] * (targetWidth / frame.shape[0]))
    targetHeight = targetHeight
    targetWidth *= 4

    imgRenderer = img_renderer.Renderer(charsRange = ctx.charsRange)

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
            percent = int(done / ctx.frameCount * 100)
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
    f = open(ctx.renderedPath + ".avid", "w")
    f.write(str(ctx.frameRate) + "\n\n")
    f.write(renderedVid)
    f.close()

    print("100% done, ", done, " frames")


def main():
    # TODO: cli args and error checking
    vPath = sys.argv[1]
    rendPath = sys.argv[2]

    rendCtx = RenderCtx(vPath, rendPath)

    renderVideo(rendCtx)


if __name__ == "__main__":
    main()
