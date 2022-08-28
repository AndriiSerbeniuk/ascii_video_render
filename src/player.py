#!/usr/bin/env python3
from os.path import exists
import argparse
from time import sleep

def main():
    argParser = argparse.ArgumentParser(description="A simple \"ascii video\"\
        player", add_help=True)
    argParser.add_argument("path", type=str, help="A path to the \"video\"")

    args = argParser.parse_args()
    vPath = args.path

    if not exists(vPath):
        print("Specified file doesn't exist")
        exit(1)

    f = open(vPath, "r")

    try:
        vid = f.read()
    except:
        print("Specified file has an unrecognised type")
        exit(1)

    f.close()

    vidData = vid.split("\n\n")

    if len(vidData) < 2:
        print("The file doesn't contain a \"video\"")
        exit(1)

    try:
        frameRate = int(vidData[0])
    except:
        print("Couldn't read framerate data")
        exit(1)

    if frameRate <= 0:
        print("Unsopported framerate value")
        exit(1)

    # wait between printing each frame to resemble framerate
    # TODO: this is probably wrong? when actually viewing something the
    # framerate feels too fast
    delaySecs = 1000 / frameRate / 1000 # secs per frame

    frames = vidData[1:]

    for frame in frames:
        print(frame, "\n")
        sleep(delaySecs)

if __name__ == "__main__":
    main()
