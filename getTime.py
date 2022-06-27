import os
from os import path
from getDurationsSection import *

if os.path.isfile(r"temp/crop.jpg") == False:
    getSection(r"temp/sample.png", r"images/object.png")
# import math

# ptsA = (0, 0)
# ptsB = (846, 458)
# ptsC = (485, 313)
# distance1 = math.dist(ptsA, ptsB)
# distance2 = math.dist(ptsA, ptsC)
# print(distance1)
# print(distance2)
