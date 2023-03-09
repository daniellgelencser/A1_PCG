#!/usr/bin/env python3

from math import floor
import sys

from gdpc import __url__, Editor, Block, geometry
from gdpc.exceptions import InterfaceConnectionError, BuildAreaNotSetError
from gdpc.vector_tools import X, Y, Z, XZ, addY, dropY, loop2D, loop3D, perpendicular, toAxisVector2D, fittingCylinder, line3D, circle, Rect

from glm import ivec2

def generatePorch(outlineRect, heightmap):


    west = ivec2(outlineRect.end.x - 1, outlineRect.begin.y)
    y = heightmap[tuple(west - outlineRect.offset)]

    # y = y+1

    editor.placeBlock(addY(west + (0, -1), y), Block("stone_bricks"))
    editor.placeBlock(addY(west + (-2, -1), y), Block("stone_bricks"))
    editor.placeBlock(addY(west + (-3, -1), y),
                      Block("stone_brick_stairs", {"facing": "east"}))

    editor.placeBlock(addY(west + (0, -2), y), Block("stone_bricks"))
    editor.placeBlock(addY(west + (-2, -2), y), Block("stone_bricks"))
    editor.placeBlock(addY(west + (-3, -2), y), Block("stone_bricks"))
    editor.placeBlock(addY(west + (-4, -2), y), Block("stone_brick_wall"))

    y = y+1

    editor.placeBlock(addY(west + (0, -1), y), Block("stone_bricks"))
    editor.placeBlock(addY(west + (-1, -1), y), Block("stone_bricks"))
    editor.placeBlock(addY(west + (-2, -1), y),
                      Block("stone_brick_stairs", {"facing": "east"}))

    editor.placeBlock(addY(west + (0, -2), y), Block("stone_bricks"))
    editor.placeBlock(addY(west + (-1, -2), y), Block("stone_bricks"))
    editor.placeBlock(addY(west + (-2, -2), y), Block("stone_bricks"))
    editor.placeBlock(addY(west + (-3, -2), y), Block("stone_brick_wall"))

    y = y+1

    editor.placeBlock(addY(west + (0, -1), y), Block("stone_brick_wall"))
    editor.placeBlock(addY(west + (0, -2), y), Block("stone_brick_wall"))
    editor.placeBlock(addY(west + (-1, -2), y), Block("stone_brick_wall"))
    editor.placeBlock(addY(west + (-2, -2), y), Block("stone_brick_wall"))


def generateFundation(y, inlineRect, outlineRect, heightmap):
    maxHeight = heightmap.max()


    # geometry.placeRect(
    #     editor, outlineRect, y - 1, Block("stone_bricks"))
    # geometry.placeRect(
    #     editor, inlineRect, y, Block("air"))
    # geometry.placeRectOutline(
    #     editor, outlineRect, y, Block("stone_bricks"))
    # y = y+1
    # geometry.placeRectOutline(
    #     editor, outlineRect, y, Block("stone_bricks"))
    # y = y+1

    for point in outlineRect.outline:
        height = heightmap[tuple(point - outlineRect.offset)]

        y = height
        while (y < maxHeight):
            editor.placeBlock(addY(point, y), Block("stone_bricks"))
            y = y+1

    generatePorch(outlineRect, heightmap)

    # geometry.placeRectOutline(
    #     editor, outlineRect, y, Block("stone_bricks"))
    # y = y+1

    return y


def generateFloor(y, outlineRect, inlineRect, type):
    geometry.placeRectOutline(editor, outlineRect, y, Block("smooth_quartz"))
    # geometry.placeRect(editor, inlineRect, y, Block("tnt"))
    geometry.placeRect(editor, inlineRect, y, Block("dark_oak_planks"))

    if (type == 0):
        return y + 1

    startEast = outlineRect.begin + ivec2(1, 0)
    startWest = ivec2(outlineRect.end.x - 1,
                      outlineRect.begin.y) + ivec2(-1, 0)
    endEast = ivec2(outlineRect.begin.x, outlineRect.end.y) + ivec2(1, -1)
    endWest = ivec2(outlineRect.end) + ivec2(-2, -1)

    diff = startWest - startEast
    single_middle = (diff.x % 6 == 0 and type == 2) or (
        diff.x % 4 == 0 and type == 1)

    while(diff.x > 0):
        t = type
        while(t > 0):
            editor.placeBlock(
                addY(startEast, y), Block("smooth_quartz_stairs", {
                    "waterlogged": "false",
                    "half": "top",
                    "shape": "straight",
                    "facing": "south"}))
            editor.placeBlock(
                addY(endEast, y), Block("smooth_quartz_stairs", {
                    "waterlogged": "false",
                    "half": "top",
                    "shape": "straight",
                    "facing": "north"}))

            startEast = startEast + ivec2(1, 0)
            endEast = endEast + ivec2(1, 0)
            diff = diff + ivec2(-1, 0)

            editor.placeBlock(
                addY(startWest, y), Block("smooth_quartz_stairs", {
                    "waterlogged": "false",
                    "half": "top",
                    "shape": "straight",
                    "facing": "south"}))

            editor.placeBlock(
                addY(endWest, y), Block("smooth_quartz_stairs", {
                    "waterlogged": "false",
                    "half": "top",
                    "shape": "straight",
                    "facing": "north"}))

            startWest = startWest + ivec2(-1, 0)
            endWest = endWest + ivec2(-1, 0)
            diff = diff + ivec2(-1, 0)

            t = t-1

        startEast = startEast + ivec2(1, 0)
        endEast = endEast + ivec2(1, 0)
        startWest = startWest + ivec2(-1, 0)
        endWest = endWest + ivec2(-1, 0)
        diff = startWest - startEast

        if (single_middle):
            editor.placeBlock(
                addY(startEast, y), Block("smooth_quartz_stairs", {
                    "waterlogged": "false",
                    "half": "top",
                    "shape": "straight",
                    "facing": "south"}))
            editor.placeBlock(
                addY(endEast, y), Block("smooth_quartz_stairs", {
                    "waterlogged": "false",
                    "half": "top",
                    "shape": "straight",
                    "facing": "north"}))

        # t = type
        # while(t > 0):
        #     editor.placeBlock(
        #         addY(startEast, y), Block("smooth_quartz_stairs", {
        #             "waterlogged": "false",
        #             "half": "top",
        #             "shape": "straight",
        #             "facing": "south"}))
        #     editor.placeBlock(
        #         addY(endEast, y), Block("smooth_quartz_stairs", {
        #             "waterlogged": "false",
        #             "half": "top",
        #             "shape": "straight",
        #             "facing": "north"}))

        #     startEast = startEast + ivec2(1, 0)
        #     endEast = endEast + ivec2(1, 0)
        #     startWest = startWest + ivec2(-1, 0)
        #     endWest = endWest + ivec2(-1, 0)
        #     diff = startWest - startEast

        #     t = t-1

    return y+1


def generateWall(y, outlineRect):
    geometry.placeRectOutline(
        editor, outlineRect, y, Block("bricks"))
    return y+1

# type 1=single 2=double


def generateWindows(y, outlineRect, type):

    startEast = outlineRect.begin + ivec2(1, 0)
    startWest = ivec2(outlineRect.end.x - 1,
                      outlineRect.begin.y) + ivec2(-1, 0)
    endEast = ivec2(outlineRect.begin.x, outlineRect.end.y) + ivec2(1, -1)
    endWest = ivec2(outlineRect.end) + ivec2(-2, -1)

    diff = startWest - startEast
    single_middle = (diff.x % 6 == 0 and type == 2) or (
        diff.x % 4 == 0 and type == 1)

    # print(f"difference is {diff.x} {single_middle}")

    # editor.placeBlock(addY(startEast , y), Block("red_concrete"))
    # editor.placeBlock(addY(endEast , y), Block("red_concrete"))
    # editor.placeBlock(addY(startWest , y), Block("red_concrete"))
    # editor.placeBlock(addY(endWest , y), Block("red_concrete"))
    # return

    while(diff.x > 0):
        t = type
        while(t > 0):
            editor.placeBlock(
                addY(startEast, y), Block("glass_pane"))
            editor.placeBlock(
                addY(endEast, y), Block("glass_pane"))

            startEast = startEast + ivec2(1, 0)
            endEast = endEast + ivec2(1, 0)
            diff = diff + ivec2(-1, 0)

            # if (diff.x == 0):
            #     break

            editor.placeBlock(
                addY(startWest, y), Block("glass_pane"))
            editor.placeBlock(
                addY(endWest, y), Block("glass_pane"))

            startWest = startWest + ivec2(-1, 0)
            endWest = endWest + ivec2(-1, 0)
            diff = diff + ivec2(-1, 0)

            t = t - 1

        startEast = startEast + ivec2(1, 0)
        endEast = endEast + ivec2(1, 0)
        startWest = startWest + ivec2(-1, 0)
        endWest = endWest + ivec2(-1, 0)
        diff = startWest - startEast

    if (single_middle):
        # print("single middle")
        editor.placeBlock(
            addY(startEast, y), Block("glass_pane"))
        editor.placeBlock(
            addY(endEast, y), Block("glass_pane"))

    # t = type
    # while(t > 0):
    #     editor.placeBlock(
    #             addY(startEast , y), Block("glass_pane"))
    #     editor.placeBlock(
    #         addY(endEast , y), Block("glass_pane"))

    #     startEast = startEast + ivec2(1, 0)
    #     endEast = endEast + ivec2(1, 0)
    #     startWest = startWest + ivec2(-1, 0)
    #     endWest = endWest + ivec2(-1, 0)
    #     diff = startWest - startEast

    #     t = t-1

    return y+1

# def generateDoor(y, position):
#     editor.placeBlock(addY(position , y), Block("glass_pane"))


def generateStory(y, inlineRect, outlineRect, height=3, type=2, is_ground=False):
    # outlineRect = Rect(outlineA, size)
    # inlineRect = Rect(inlineA, size + ivec2(-2, -2))

    tmp_y = y

    q = 0
    while(q < height):
        generateWall(y, outlineRect)
        y = generateWindows(y, outlineRect, type)
        q = q+1

    if (is_ground):
        west = ivec2(outlineRect.end.x, outlineRect.begin.y) + ivec2(-2, 0)
        editor.placeBlock(addY(west, tmp_y), Block(
            "dark_oak_door", {"facing": "south"}))

    return generateFloor(y, outlineRect, inlineRect, type)


def generateFacade(y, outlineA, outlineB, rooftop):

    rooftop = rooftop-1
    east = ivec2(outlineA)
    west = ivec2(outlineB.x, outlineA.y)
    diff = west - east
    even = diff % 2 != 0
    flip = "top"

    while(diff.x > 0):
        print(f"west: {tuple(west)} east: {tuple(east)} diff: {tuple(diff)}, y: {y}, top: {rooftop}")

        if (flip == "top"):
            flip = "bottom"
        else:
            flip = "top"

        e = east
        w = west

        editor.placeBlock(
            addY(e, y), Block("smooth_quartz_stairs", {
                "waterlogged": "false",
                "half": flip,
                "shape": "straight",
                "facing": "east"}))
        e = e + ivec2(1, 0)

        editor.placeBlock(
            addY(w, y), Block("smooth_quartz_stairs", {
                "waterlogged": "false",
                "half": flip,
                "shape": "straight",
                "facing": "west"}))
        w = w + ivec2(-1, 0)

        d = w - e

        while (d.x > 0):

            editor.placeBlock(
                addY(e, y), Block("smooth_quartz"))
            e = e + ivec2(1, 0)

            editor.placeBlock(
                addY(w, y), Block("smooth_quartz"))
            w = w + ivec2(-1, 0)

            d = w - e

        if (flip == "top" and diff.x == 1):
            print("top 1")

            editor.placeBlock(
                addY(e, y - 1), Block("smooth_quartz"))
            editor.placeBlock(
                addY(e + (0, -1), y - 1), Block("dark_oak_fence"))
            editor.placeBlock(
                addY(e + (0, -1), y - 2), Block("chain"))
            
            if even:
                editor.placeBlock(
                    addY(w, y - 1), Block("smooth_quartz"))
                editor.placeBlock(
                    addY(w + (0, -1), y - 1), Block("dark_oak_fence"))
                editor.placeBlock(
                    addY(w + (0, -1), y - 2), Block("chain"))

            y = y+1
            break

        if (rooftop <= y):
            editor.placeBlock(
                addY(e, y), Block("smooth_quartz"))
            editor.placeBlock(
                addY(e, y + 1), Block("smooth_quartz_slab"))
            editor.placeBlock(
                addY(e + (0, -1), y - 0), Block("dark_oak_fence"))
            editor.placeBlock(
                addY(e + (0, -1), y - 1), Block("chain"))
            
            if even:
                editor.placeBlock(
                    addY(w, y + 1), Block("smooth_quartz_slab"))
                editor.placeBlock(
                    addY(w + (0, -1), y - 0), Block("dark_oak_fence"))
                editor.placeBlock(
                    addY(w + (0, -1), y - 1), Block("chain"))
            break

        else:
            print("glass")
            editor.placeBlock(
                    addY(e, y), Block("glass_pane"))
            if even:
                editor.placeBlock(
                    addY(w, y), Block("glass_pane"))

        
        if (flip == "bottom"):
            east = east + ivec2(1, 0)
            west = west + ivec2(-1, 0)

        diff = west - east
        y = y+1

    return y


def generateRoof(y, outlineA, outlineB):

    startEast = outlineA + ivec2(0, 1)
    endEast = ivec2(outlineA.x, outlineB.y)
    startWest = ivec2(outlineB.x, outlineA.y + 1)
    endWest = ivec2(outlineB)
    diff = startWest - startEast

    print(diff.x)

    while(diff.x >= 2):


        geometry.placeLine(
            editor,
            addY(startEast, y),
            addY(endEast, y),
            Block("dark_oak_stairs",
                  {
                      "waterlogged": "false",
                      "half": "bottom",
                      "shape": "straight",
                      "facing": "east"}
                  ),
            width=1
        )

        geometry.placeLine(
            editor,
            addY(startWest, y),
            addY(endWest, y),
            Block("dark_oak_stairs",
                  {
                      "waterlogged": "false",
                      "half": "bottom",
                      "shape": "straight",
                      "facing": "west"}
                  ),
            width=1
        )
        diff = startWest - startEast

        if (diff.x <= 2):
            if (diff.x % 2 == 0):
                editor.placeBlock(
                    addY(endWest - ivec2(1, 0), y), Block("glass_pane"))

            startEast = startEast + ivec2(1, 0)
            endEast = endEast + ivec2(1, 0)
            startWest = startWest + ivec2(-1, 0)
            endWest = endWest + ivec2(-1, 0)
            y = y+1
            break

        x = 1
        c = floor((diff.x / 2 - 1))

        i = c
        while (i > 0):
            editor.placeBlock(
                addY(endWest - ivec2(x, 0), y), Block("dark_oak_planks"))
            x = x + 1
            i = i - 1

        if (diff.x % 2 == 0):
            editor.placeBlock(
                addY(endWest - ivec2(x, 0), y), Block("glass_pane"))
            x = x+1
        else:
            editor.placeBlock(
                addY(endWest - ivec2(x, 0), y), Block("glass_pane"))
            x = x+1
            editor.placeBlock(
                addY(endWest - ivec2(x, 0), y), Block("glass_pane"))
            x = x+1

        i = c
        while (i > 0):
            editor.placeBlock(
                addY(endWest - ivec2(x, 0), y), Block("dark_oak_planks"))
            x = x + 1
            i = i - 1

        startEast = startEast + ivec2(1, 0)
        endEast = endEast + ivec2(1, 0)
        startWest = startWest + ivec2(-1, 0)
        endWest = endWest + ivec2(-1, 0)
        y = y+1

    if (diff.x == 2):

        geometry.placeLine(
            editor,
            addY(startEast, y),  # Endpoint 1
            addY(endEast, y),  # Endpoint 1
            Block("dark_oak_slab"),
            width=1
        )

    return y




def findChunk(buildSlice):
    chunk = buildSlice.chunkRect.begin + ivec2(1, 1) # only whole chunks

    while (chunk.x < buildSlice.chunkRect.last.x):
        while (chunk.y < buildSlice.chunkRect.last.y):
            chunkRect = Rect(chunk * ivec2(16, 16), ivec2(16, 16))
            print(chunkRect)
            
            chunkSlice = editor.loadWorldSlice(chunkRect)
            surface = chunkSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
            liquid = surface - chunkSlice.heightmaps["OCEAN_FLOOR"]

            print(surface)

            print(surface.max() - surface.min())

            if (liquid.sum() > 10):
                break

            if surface.max() - surface.min() <= 3 :
                return chunk * ivec2(16, 16)

            chunk = chunk + ivec2(0, 1)
        chunk = ivec2(chunk.x + 1, buildSlice.chunkRect.begin.y + 1)

    print("Not found")
    return False


def findRect(buildRect, size):
    size = size + ivec2(2, 2)
    point = buildRect.begin

    while(point.x < buildRect.last.x):
        while (point.y < buildRect.last.y):

            pointRect = Rect(point + ivec2(-1, -1), size)
            print(pointRect)

            pointSlice = editor.loadWorldSlice(pointRect)
            surface = pointSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
            liquid = surface - pointSlice.heightmaps["OCEAN_FLOOR"]

            print(surface)

            surfaceDiff = surface.max() - surface.min()

            if (surfaceDiff <= 3 and liquid.sum() == 0):
                return point
            
            point = point + ivec2(0, size.y)
        point = ivec2(point.x + size.x, buildRect.begin.y)

    print("Not found")
    return False



def main():
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

        # buildArea is a Box object, which is defined by an offset and a size.
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

    size = ivec2(7, 14)

    offset = findRect(buildRect, size)
    
    if (not offset):
        print("could not find suitable area")
        return

    print(tuple(offset))

    # offset = (20, 60)

    

    outlineA = offset
    outlineB = outlineA + size - (1, 1)
    inlineA = outlineA + (1, 1)
    # inlineB = outlineB - (1, 1)

    # buildRect = buildArea.toRect()
    outlineRect = Rect(outlineA, size)
    inlineRect = Rect(inlineA, size + ivec2(-2, -2))
    worldSlice = editor.loadWorldSlice(outlineRect)
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

    # print(f"outline a: {tuple(outlineA)} b: {tuple(outlineB)} rect: {outlineRect} build: {buildRect}")

    y = buildArea.begin.y

    # y = generateStory(y, inlineRect, outlineRect, 1, 2, False)
    # generateWall(y, outlineRect)
    # generateWindows(y, outlineRect, 2)

    print (f"generate fundation {outlineRect}")
    y = generateFundation(y, inlineRect, outlineRect, heightmap)

    y = generateFloor(y, outlineRect, inlineRect, 0)
    y = generateStory(y, inlineRect, outlineRect, 3, 1, True)

    q = 0
    while (q < 2):
        y = generateStory(y, inlineRect, outlineRect, 3, 2, False)
        q = q+1

    y = generateStory(y, inlineRect, outlineRect, 2, 2, False)

    rooftop = generateRoof(y, outlineA, outlineB)
    generateFacade(y, outlineA, outlineB, rooftop)


editor = Editor()
main()

# generateFacade(y)

# generateRoof(y)
