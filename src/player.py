#!/usr/bin/env python3
import sys
import os
from time import sleep

def main():
    vPath = sys.argv[1]

    f = open(vPath, "r")
    vid = f.read()

    # wait between printing each frame to resemble framerate
    vidInfo = iter(vid.split("\n\n"))
    frameRate = int(next(vidInfo))
    frames = vidInfo
    # TODO: this is probably wrong? when actually viewing something the
    # framerate feels too fast
    delaySecs = 1000 / frameRate / 1000 # secs per frame

    for frame in frames:
        print(frame, "\n")
        sleep(delaySecs)

if __name__ == "__main__":
    main()
