import ffmpeg
from pprint import pprint

def getFramesCount(vidPath: str) -> int:
    # TODO: is "nb_frames" the right thing here?
    # TODO: is assuming that the first stream is the vedeo stream a right thing?
    countVal = str(ffmpeg.probe(vidPath)["streams"][0]["nb_frames"])
    
    return int(countVal)

def getFrameRate(vidPath: str) -> int:
    frameRate = str(ffmpeg.probe(vidPath)["streams"][0]["avg_frame_rate"]).split("/")
    
    return round(int(frameRate[0]) / int(frameRate[1]))
