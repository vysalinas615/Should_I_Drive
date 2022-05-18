from BodyTracking import BodyConnect
from BodyTracking import BodyTrack
from BodyTracking.BigCSVs import ReformatCSV

BodyConnect.output("203_e2.mp4", 320, 180, 0.2)

BodyConnect.outputDefaults("s4.jpeg")

# BodyConnect.output(0, 320, 180, 0.2)

# output = BodyTrack.getFrameData(0)
# print(output)

# bodyFrames = BodyTrack.getVideoData("47_e3.mp4")
# print(bodyFrames)

# BodyTrack.allVideosToCSV("../mp4files/", "resized.csv")
