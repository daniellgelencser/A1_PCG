import sys

from gdpc import __url__, Editor, Block, geometry
from gdpc.exceptions import InterfaceConnectionError, BuildAreaNotSetError
from gdpc.vector_tools import addY, dropY, ivec2, ivec3, Rect
import numpy as np


editor = Editor()

# Check if the editor can connect to the GDMC HTTP interface.
try:
    editor.checkConnection()
except InterfaceConnectionError:
    print(
        f"Error: Could not connect to the GDMC HTTP interface at {editor.host}!\n"
        "To use GDPC, you need to use a \"backend\" that provides the GDMC HTTP interface.\n"
        "For example, by running Minecraft with the GDMC HTTP mod installed.\n"
        f"See {__url__}/README.md for more information."
    )
    sys.exit(1)

# Get the build area.
try:
    buildArea = editor.getBuildArea()
except BuildAreaNotSetError:
    print(
        "Error: failed to get the build area!\n"
        "Make sure to set the build area with the /setbuildarea command in-game.\n"
        "For example: /setbuildarea ~0 0 ~0 ~64 200 ~64"
    )
    sys.exit(1)

print(f"Build area offset: {tuple(buildArea.offset)}")
print(f"Build area size:   {tuple(buildArea.size)}")

# The Box class has many convenience methods and properties. Here are a few.
print(f"Build area start:  {tuple(buildArea.begin)}")
print(f"Build area end:    {tuple(buildArea.end)}")
# Last is inclusive, end is exclusive.
print(f"Build area last:   {tuple(buildArea.last)}")
print(f"Build area center: {tuple(buildArea.center)}")

buildRect = buildArea.toRect()
buildSlice = editor.loadWorldSlice(buildRect)

# print(f"chunk rect {buildSlice.chunkRect}")
# print(f"chunk rect end {buildSlice.chunkRect.end}")
# print(f"chunk rect last {buildSlice.chunkRect.last}")

# By default, world slices load the following four heightmaps:
# - "WORLD_SURFACE":             The top non-air blocks.
# - "MOTION_BLOCKING":           The top blocks with a hitbox or fluid.
# - "MOTION_BLOCKING_NO_LEAVES": Like MOTION_BLOCKING, but ignoring leaves.
# - "OCEAN_FLOOR":               The top non-air solid blocks.

# liquid = buildSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"] - buildSlice.heightmaps["OCEAN_FLOOR"]
# print(liquid)

# centre = buildSlice.chunkRect.center * ivec2(16, 16)

# print(centre)

def findChunk(buildSlice):
    chunk = buildSlice.chunkRect.begin + ivec2(1, 1) # only whole chunks

    while (chunk.x < buildSlice.chunkRect.last.x):
        while (chunk.y < buildSlice.chunkRect.last.y):
            chunkRect = Rect(chunk * ivec2(16, 16), ivec2(16, 16))
            chunkSlice = editor.loadWorldSlice(chunkRect)
            surface = chunkSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

            if surface.max() - 3 <= surface.min():
                return chunk * ivec2(16, 16)

            chunk = chunk + ivec2(0, 1)
        chunk = chunk + ivec2(1, 0)


def findRect(buildRect, size, pointRect):
    point = buildRect.begin

    while(point.x < buildRect.last.x):
        while (point.y < buildRect.last.y):

            pointRect = Rect(point, size)
            print(pointRect)

            pointSlice = editor.loadWorldSlice(pointRect)
            surface = pointSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
            liquid = surface - pointSlice.heightmaps["OCEAN_FLOOR"]

            print(surface)

            surfaceDiff = surface.max() - surface.min()

            if (surfaceDiff <= 3 and liquid.sum() == 0):
                return surface
            
            point = point + ivec2(0, size.y)
        point = ivec2(point.x + size.x, buildRect.begin.y)

    print("Not found")
    return False


    


size = ivec2(7, 14)
pointRect = Rect(dropY(buildArea.begin), size)
surface = findRect(buildRect, size, pointRect)

if (pointRect):
    print(pointRect)
    editor.placeBlock(addY(pointRect.begin, surface[0][0]), Block("blue_concrete"))



# findChunk(buildSlice)

# chunk = buildSlice.chunkRect.begin + ivec2(1, 1) # only whole chunks



# print(f"chunk {tuple(chunk)}")
# chunkRect = Rect(chunk * ivec2(16, 16), ivec2(16, 16))
# chunkSlice = editor.loadWorldSlice(chunkRect)

# surface = chunkSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
# liquid = surface - chunkSlice.heightmaps["OCEAN_FLOOR"]
# print(liquid)
# # print(surface.max() - surface.min())

# non_zero = liquid.nonzero()
# non_zero_vec = list(map(lambda x, y: ivec2(x,y), non_zero[0], non_zero[1]))

# print(tuple(non_zero[0]))
