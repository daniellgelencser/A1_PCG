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

print(f"chunk rect {buildSlice.chunkRect}")
print(f"chunk rect end {buildSlice.chunkRect.end}")
print(f"chunk rect last {buildSlice.chunkRect.last}")
print(f"nbt {buildSlice.nbt}")

# By default, world slices load the following four heightmaps:
# - "WORLD_SURFACE":             The top non-air blocks.
# - "MOTION_BLOCKING":           The top blocks with a hitbox or fluid.
# - "MOTION_BLOCKING_NO_LEAVES": Like MOTION_BLOCKING, but ignoring leaves.
# - "OCEAN_FLOOR":               The top non-air solid blocks.

# liquid = buildSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"] - buildSlice.heightmaps["OCEAN_FLOOR"]
# print(liquid)

# centre = buildSlice.chunkRect.center * ivec2(16, 16)

# print(centre)

# size = ivec2(7, 14)


def findWater(buildRect, area):
    point = buildRect.begin

    while(point.x < buildRect.last.x):
        while (point.y < buildRect.last.y):

            pointRect = Rect(point, area)
            # print(pointRect)

            pointSlice = editor.loadWorldSlice(pointRect)
            surface = pointSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
            floor = pointSlice.heightmaps["OCEAN_FLOOR"]

            liquid = surface - floor
            # print(liquid)

            

            if(liquid.min() > 0): # only water in slice
                seaLevel = floor[0][0]

                print(pointRect)
                print(liquid)

                max = 1
                ctr = 0
                shore = point
                while (max > 0  and ctr <8):
                    shore = shore + ivec2(1, 0)
                    shoreRect = Rect(shore, ivec2(1, area.y + 2))
                    shoreSlice = editor.loadWorldSlice(shoreRect)
                    shoreLiquid = shoreSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"] - shoreSlice.heightmaps["OCEAN_FLOOR"]

                    
                    print(f"shore {shoreLiquid}")

                    max = shoreLiquid.max()
                    ctr = ctr + 1

                if (max > 0):
                    print("no shore found")
                    point = point + ivec2(0, area.y + 1)
                    continue

                print("shore found")

                min = 0
                shore = point
                while ((min == 0 or ctr < 6) and ctr < 256):
                    shore = shore + ivec2(1, 0)
                    shoreRect = Rect(shore, ivec2(1, area.y + 2))
                    shoreSlice = editor.loadWorldSlice(shoreRect)
                    shoreSurface = shoreSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
                    shoreFloor = shoreSlice.heightmaps["OCEAN_FLOOR"]
                    shoreLiquid = shoreSurface - shoreFloor

                    


                    if(shoreLiquid[0][0] > 0 or shoreLiquid[0][1] > 0):
                        y = seaLevel - 2
                        while (y <= seaLevel): 
                            editor.placeBlock(addY(shoreRect.begin + ivec2(0, 1) , y), Block("water"))
                            y = y + 1

                    else:
                        y = seaLevel - 2
                        while (y <= seaLevel):
                            editor.placeBlock(addY(shoreRect.begin + ivec2(0, 1) , y), Block("stone_bricks"))
                            y = y + 1

                    y = seaLevel - 3

                    if(shoreFloor.min() - 1 < y):
                        y = shoreFloor.min() - 1
                    editor.placeBlock(addY(shoreRect.begin + ivec2(0, 2) , y), Block("stone_bricks"))
                    editor.placeBlock(addY(shoreRect.begin + ivec2(0, 3) , y), Block("stone_bricks"))
                    editor.placeBlock(addY(shoreRect.begin + ivec2(0, 4) , y), Block("stone_bricks"))
                    editor.placeBlock(addY(shoreRect.begin + ivec2(0, 5) , y), Block("stone_bricks"))
                    y = y + 1
                    while (y <= seaLevel): 
                        editor.placeBlock(addY(shoreRect.begin + ivec2(0, 2) , y), Block("water"))
                        editor.placeBlock(addY(shoreRect.begin + ivec2(0, 3) , y), Block("water"))
                        editor.placeBlock(addY(shoreRect.begin + ivec2(0, 4) , y), Block("water"))
                        editor.placeBlock(addY(shoreRect.begin + ivec2(0, 5) , y), Block("water"))
                        y = y + 1

                    while (y <= shoreSurface.max()):
                        editor.placeBlock(addY(shoreRect.begin + ivec2(0, 1) , y), Block("air"))
                        editor.placeBlock(addY(shoreRect.begin + ivec2(0, 2) , y), Block("air"))
                        editor.placeBlock(addY(shoreRect.begin + ivec2(0, 3) , y), Block("air"))
                        editor.placeBlock(addY(shoreRect.begin + ivec2(0, 4) , y), Block("air"))
                        editor.placeBlock(addY(shoreRect.begin + ivec2(0, 5) , y), Block("air"))
                        editor.placeBlock(addY(shoreRect.begin + ivec2(0, 6) , y), Block("air"))
                        y = y + 1



                    if(shoreLiquid[0][6] > 0 or shoreLiquid[0][7] > 0):
                        y = seaLevel - 2
                        while (y <= seaLevel): 
                            editor.placeBlock(addY(shoreRect.begin + ivec2(0, 6) , y), Block("water"))
                            y = y + 1
                    else:
                        y = seaLevel - 2
                        while (y <= seaLevel):
                            editor.placeBlock(addY(shoreRect.begin + ivec2(0, 6) , y), Block("stone_bricks"))
                            y = y + 1





                    print(f"water {shoreLiquid}")

                    min = shoreLiquid.min()
                    ctr = ctr + 1

                print(f"found opposit side {shore}")


                # # return
                # if (max == 0):

                #     # return
                #     continue


                # editor.placeBlock(addY(pointRect.begin + ivec2(0, 1), surface[0][0]), Block("gray_concrete"))
                # editor.placeBlock(addY(pointRect.begin + ivec2(0, 2), surface[0][0]), Block("blue_concrete"))
                # editor.placeBlock(addY(pointRect.begin + ivec2(0, 3), surface[0][0]), Block("blue_concrete"))
                # editor.placeBlock(addY(pointRect.begin + ivec2(0, 4), surface[0][0]), Block("blue_concrete"))
                # editor.placeBlock(addY(pointRect.begin + ivec2(0, 5), surface[0][0]), Block("blue_concrete"))
                # editor.placeBlock(addY(pointRect.begin + ivec2(0, 6), surface[0][0]), Block("gray_concrete"))

                return

            point = point + ivec2(0, area.y + 1)
        point = ivec2(point.x + area.x + 1, buildRect.begin.y)

area = ivec2(2, 6)

findWater(buildRect, area)


def findWaterOld():
    chunk = buildSlice.chunkRect.begin + ivec2(3, 1) # only whole chunks
    print(f"chunk {tuple(chunk)}")
    chunkRect = Rect(chunk * ivec2(16, 16), ivec2(16, 16))
    chunkSlice = editor.loadWorldSlice(chunkRect)

    surface = chunkSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
    liquid = surface - chunkSlice.heightmaps["OCEAN_FLOOR"]
    print(liquid)
    # print(surface.max() - surface.min())

    non_zero = liquid.nonzero()
    non_zero_vec = list(map(lambda x, y: ivec2(x,y), non_zero[0], non_zero[1]))

    print(tuple(non_zero[0]))

    # pointA = ivec2(3,3)
    # pointB = ivec2(12,12)
    # print (f"{pointA} {pointB}")


    size = len(non_zero[0])
    river = ivec2(0,0)
    for i in range(size):
        block = chunkSlice.getBlock(addY(non_zero_vec[i], surface[non_zero_vec[i].x][non_zero_vec[i].y] - 1))

        if (not (
            "minecraft:water" == block.id 
            or "minecraft:seagrass" == block.id
            or "minecraft:tall_seagrass" == block.id
            or "minecraft:sea_pickle" == block.id)):
            continue

        print(f"{tuple(non_zero_vec[i])} | {block.id}")

        river_def = ivec2(4, 4)
        # scan for river
        river_found = True
        for x in range(river_def.x):

            for y in range(river_def.y):
                next = non_zero_vec[i] + ivec2(x, y)
                block = chunkSlice.getBlock(addY(next, surface[non_zero_vec[i].x][non_zero_vec[i].y] - 1))

                if (not (
                    "minecraft:water" == block.id 
                    or "minecraft:seagrass" == block.id
                    or "minecraft:tall_seagrass" == block.id
                    or "minecraft:sea_pickle" == block.id)):
                    river_found = False
                    break

            if (not river_found):
                break

        if (river_found):
            river = non_zero_vec[i]
            print(f"river found at {tuple(chunkRect.begin)}")
            height = surface[non_zero_vec[i].x][non_zero_vec[i].y]
            print(height)
            while (river.x < 16):
                y = surface.max()
                while (y >= height):
                    editor.placeBlock(addY(chunkRect.begin + river, y), Block("air"))
                    editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 1), y), Block("air"))
                    editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 2), y), Block("air"))
                    editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 3), y), Block("air"))
                    editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 4), y), Block("air"))
                    editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 5), y), Block("air"))
                    y = y-1
                # y = y-1

                print(y)
                
                for r in range(3):

                    editor.placeBlock(addY(chunkRect.begin + river, y), Block("stone_bricks"))
                    if (river.x == 15):
                        editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 1), y), Block("stone_bricks"))
                        editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 2), y), Block("stone_bricks"))
                        editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 3), y), Block("stone_bricks"))
                        editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 4), y), Block("stone_bricks"))
                    else:
                        editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 1), y), Block("water"))
                        editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 2), y), Block("water"))
                        editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 3), y), Block("water"))
                        editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 4), y), Block("water"))
                    editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 5), y), Block("stone_bricks"))
                    y = y-1

                editor.placeBlock(addY(chunkRect.begin + river, y), Block("stone_bricks"))
                editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 1), y), Block("stone_bricks"))
                editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 2), y), Block("stone_bricks"))
                editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 3), y), Block("stone_bricks"))
                editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 4), y), Block("stone_bricks"))
                editor.placeBlock(addY(chunkRect.begin + river + ivec2(0, 5), y), Block("stone_bricks"))


                river = river + ivec2(1, 0)

            break 
