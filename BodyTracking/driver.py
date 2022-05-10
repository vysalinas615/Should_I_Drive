from os import listdir
from os.path import isfile, join

import BodyTrack

# output = BodyTrack.getFrameData("s4.jpeg")
# print(output)

# bodyFrames = BodyTrack.getVideoData("47_e3.mp4")
# print(bodyFrames)
#
# output = BodyTrack.frameToCSV("s4.jpeg", "frame4.csv")
#
# output = BodyTrack.videoToCSV("9_e0.mp4", "video9.csv")

BodyTrack.allVideosToCSV("../mp4files/", "named.csv")


# path = "../mp4files"
#
# allVideos = [f for f in listdir(path) if isfile(join(path, f))]
#
# dir = "CSVs/"
#
# for filePath in allVideos:
#     BodyTrack.videoToCSV(path + "/" + filePath, "%s%s.csv" % (dir, filePath.rstrip(".mp4")))