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




    


# size =liquid[0].size
# ctr = 0
# prev = ivec2(0, 0)


# liquid_trans = liquid.transpose()
# print(liquid_trans)

# non_zero_trans = liquid_trans.nonzero()
# print(non_zero_trans[0])
# print(non_zero_trans[1])


# for i in range(len(non_zero[0])):
#     yArr = np.where(non_zero[1] == non_zero[1][i])[0]
#     if (len(yArr) < 4): # at least 4 on y axis
#         continue

#     p = yArr[0]
#     to_break = False
#     for y in yArr:
#         if (non_zero[1][y] > p + 1):
#             to_break = True
#             break

#     if (to_break):
#         break

#     print(f"{non_zero[0][i]} - {non_zero[1][i]}")

#     if (non_zero[1][i] - prev.y > 1):
#         continue
#     prev = ivec2(non_zero[0][i], non_zero[1][i])

#     print(f"{non_zero[0][i]} - {non_zero[1][i]}")
    # print(f"{yArr}")
# river_ctr = [0 for element in range(16)]
# for x in range(16):
#     for z in range(16):
#         if (liquid[x][z] > 0):
#             river_ctr[z] = river_ctr[z] + 1
#             print(chunkSlice.getBlock(ivec3(x, surface[x, z] - 1, z)))

#         else:
#             river_ctr[z] = 0


# while (chunk.x < buildSlice.chunkRect.last.x):
#     while(chunk.y < buildSlice.chunkRect.last.y):
#         print(f"chunk {tuple(chunk)}")
#         chunkRect = Rect(chunk * ivec2(16, 16), ivec2(16, 16))
#         chunkSlice = editor.loadWorldSlice(chunkRect)
#         water = chunkSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"] - chunkSlice.heightmaps["OCEAN_FLOOR"]
#         print(water.dtype)
#         # print(water)
#         # print(water)
#         break
#         chunk = chunk + ivec2(0, 1)

#     break
#     chunk = ivec2(chunk.x + 1, buildSlice.chunkRect.begin.y + 1)


# size = ivec2(7, 14)



# outlineA = dropY(buildArea.center)


# return

# outlineRect = Rect(outlineA, size)
# worldSlice = editor.loadWorldSlice(outlineRect)

# # offset = (20, 60)


# outlineA = dropY(buildArea.begin)# + offset
# outlineB = outlineA + (7, 14) - (1, 1)
# inlineA = outlineA + (1, 1)
# inlineB = outlineB - (1, 1)

# vec = addY(outlineA, buildArea.center.y + 17)
# print(f"Block at {tuple(vec)}: {worldSlice.getBlockGlobal(vec)}")

# heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

# localCenter = outlineRect.size // 2

# centerHeight = heightmap[tuple(localCenter)]
# # centerTopBlock = worldSlice.getBlock(addY(localCenter, centerHeight - 1))

# maxHeight = heightmap.max()

# print(heightmap)
# print(heightmap.max())
# print(f"center {tuple(localCenter)} height {centerHeight}")

# print(f"Available heightmaps: {worldSlice.heightmaps.keys()}")

# print(f"block rect {worldSlice.rect}")
# print(f"chunk rect {worldSlice.chunkRect}")
# print(f"nbt {worldSlice.nbt}")






# for point in outlineRect.outline:
#     height = heightmap[tuple(point - outlineRect.offset)]

    # editor.placeBlock(addY(point, height), Block("stone_bricks"))



    # y = height
    # while (y < maxHeight):
    #     editor.placeBlock(addY(point, y), Block("stone_bricks"))
    #     y = y+1

