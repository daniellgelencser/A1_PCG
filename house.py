#!/usr/bin/env python3

from math import floor
import sys

from gdpc import __url__, Editor, Block, geometry
from gdpc.exceptions import InterfaceConnectionError, BuildAreaNotSetError
from gdpc.vector_tools import X, Y, Z, XZ, addY, dropY, loop2D, loop3D, perpendicular, toAxisVector2D, fittingCylinder, line3D, circle, Rect

from glm import ivec2
import json, random

def generatePorch(outlineRect, minHeight, height):


    west = ivec2(outlineRect.end.x - 1, outlineRect.begin.y)
    y = minHeight

    # print(height)

    if (height >= 3):
        editor.placeBlock(addY(west + (0, -1), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-2, -1), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-3, -1), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-4, -1), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-5, -1), y), Block("stone_brick_stairs", {"facing": "east"}))

        editor.placeBlock(addY(west + (0, -2), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-1, -2), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-2, -2), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-3, -2), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-4, -2), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-5, -2), y), Block("stone_bricks"))

        y = y+1

    if (height >= 2):
        editor.placeBlock(addY(west + (0, -1), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-2, -1), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-3, -1), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-4, -1), y), Block("stone_brick_stairs", {"facing": "east"}))

        editor.placeBlock(addY(west + (0, -2), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-1, -2), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-2, -2), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-3, -2), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-4, -2), y), Block("stone_bricks"))
        editor.placeBlock(addY(west + (-5, -2), y), Block("stone_brick_wall"))

        y = y+1

    editor.placeBlock(addY(west + (0, -1), y), Block("stone_bricks"))
    editor.placeBlock(addY(west + (-2, -1), y), Block("stone_bricks"))
    editor.placeBlock(addY(west + (-3, -1), y),
                    Block("stone_brick_stairs", {"facing": "east"}))

    editor.placeBlock(addY(west + (0, -2), y), Block("stone_bricks"))
    editor.placeBlock(addY(west + (-1, -2), y), Block("stone_bricks"))
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
    diff = maxHeight - heightmap.min()

    for point in outlineRect.outline:
        y = heightmap[tuple(point - outlineRect.offset)]
        tmp_diff = diff

        while (y < maxHeight or tmp_diff < 1):
            editor.placeBlock(addY(point, y), Block("stone_bricks"))
            y = y + 1
            tmp_diff = tmp_diff + 1

    generatePorch(outlineRect, heightmap.min(), diff)

    return y

def generateLivingroom(y, rect, height):

    geometry.placeRect(editor, rect, y, Block("light_gray_carpet"))

    editor.placeBlock(addY(rect.begin, y), Block("oak_stairs", {"facing": "west", "shape":"inner_right"}))
    editor.placeBlock(addY(rect.begin + ivec2(1, 0), y), Block("oak_stairs", {"facing": "north"}))
    editor.placeBlock(addY(rect.begin + ivec2(2, 0), y), Block("potted_fern"))
    editor.placeBlock(addY(rect.begin + ivec2(0, 1), y), Block("oak_stairs", {"facing": "west"}))
    editor.placeBlock(addY(rect.begin + ivec2(0, 2), y), Block("oak_stairs", {"facing": "west"}))
    editor.placeBlock(addY(rect.begin + ivec2(0, 3), y), Block("oak_stairs", {"facing": "west"}))
    editor.placeBlock(addY(rect.begin + ivec2(0, 4), y), Block("bookshelf"))
    editor.placeBlock(addY(rect.begin + ivec2(0, 5), y), Block("bookshelf"))

    editor.placeBlock(addY(rect.last - ivec2(0, 2), y), Block("waxed_cut_copper"))
    editor.placeBlock(addY(rect.last - ivec2(0, 3), y), Block("campfire"))
    editor.placeBlock(addY(rect.last - ivec2(0, 4), y), Block("waxed_cut_copper"))

    y=y+1

    editor.placeBlock(addY(rect.begin + ivec2(0, 4), y), Block("lantern"))
    editor.placeBlock(addY(rect.begin + ivec2(0, 5), y), Block("bookshelf"))

    editor.placeBlock(addY(rect.last - ivec2(0, 2), y), Block("waxed_cut_copper_stairs", {"facing": "north"}))
    editor.placeBlock(addY(rect.last - ivec2(0, 3), y), Block("waxed_cut_copper_stairs", {"facing": "east", "half": "top"}))
    editor.placeBlock(addY(rect.last - ivec2(0, 4), y), Block("waxed_cut_copper_stairs", {"facing": "south"}))

    y=y+1

    editor.placeBlock(addY(rect.begin + ivec2(0, 4), y), Block("bookshelf"))
    editor.placeBlock(addY(rect.begin + ivec2(0, 5), y), Block("bookshelf"))

    editor.placeBlock(addY(rect.last - ivec2(0, 3), y), Block("waxed_cut_copper_slab"))


def generateBedroom(y, rect, height):
    geometry.placeRect(editor, rect, y, Block("green_carpet"))

    editor.placeBlock(addY(rect.begin + ivec2(0, 2), y), Block("bookshelf"))
    editor.placeBlock(addY(rect.begin + ivec2(0, 3), y), Block("green_bed", {"facing": "west", "part": "head"}))
    editor.placeBlock(addY(rect.begin + ivec2(0, 4), y), Block("green_bed", {"facing": "west", "part": "head"}))
    editor.placeBlock(addY(rect.begin + ivec2(1, 3), y), Block("green_bed", {"facing": "west", "part": "foot"}))
    editor.placeBlock(addY(rect.begin + ivec2(1, 4), y), Block("green_bed", {"facing": "west", "part": "foot"}))
    editor.placeBlock(addY(rect.begin + ivec2(0, 5), y), Block("bookshelf"))


    editor.placeBlock(addY(rect.last, y), Block("bookshelf"))
    editor.placeBlock(addY(rect.last - ivec2(0, 1), y), Block("oak_fence"))
    editor.placeBlock(addY(rect.last - ivec2(0, 2), y), Block("oak_fence"))

    editor.placeBlock(addY(rect.last - ivec2(1, 1), y), Block("oak_stairs", {"facing": "west"}))

    y=y+1

    editor.placeBlock(addY(rect.begin + ivec2(0, 2), y), Block("lantern"))
    editor.placeBlock(addY(rect.begin + ivec2(0, 5), y), Block("lantern"))

    editor.placeBlock(addY(rect.last, y), Block("lantern"))
    editor.placeBlock(addY(rect.last - ivec2(0, 1), y), Block("oak_pressure_plate"))
    editor.placeBlock(addY(rect.last - ivec2(0, 2), y), Block("oak_pressure_plate"))

def placeEntity(point, name, states):
    options = json.dumps(states)
    coordinates = "{x} {y} {z}".format(x=point.x, y=point.y, z=point.z)
    editor.runCommand(f"summon {name} {coordinates} {options}")

def generateKitchen(y, rect, height):

    ceiling = y+height

    editor.placeBlock(addY(rect.begin + ivec2(1, 1), y), Block("oak_fence"))
    editor.placeBlock(addY(rect.begin + ivec2(1, 2), y), Block("oak_fence"))
    editor.placeBlock(addY(rect.begin + ivec2(2, 1), y), Block("oak_fence"))
    editor.placeBlock(addY(rect.begin + ivec2(2, 2), y), Block("oak_fence"))

    editor.placeBlock(addY(rect.last - ivec2(1, 1), y), Block("oak_planks"))
    editor.placeBlock(addY(rect.last - ivec2(0, 1), y), Block("oak_planks"))
    editor.placeBlock(addY(rect.last - ivec2(0, 2), y), Block("water_cauldron",  {"level": 3}))
    editor.placeBlock(addY(rect.last - ivec2(0, 3), y), Block("furnace", {"facing": "west"}))
    editor.placeBlock(addY(rect.last - ivec2(0, 4), y), Block("oak_planks"))

    y=y+1

    editor.placeBlock(addY(rect.begin + ivec2(1, 1), y), Block("oak_pressure_plate"))
    editor.placeBlock(addY(rect.begin + ivec2(1, 2), y), Block("oak_pressure_plate"))
    editor.placeBlock(addY(rect.begin + ivec2(2, 1), y), Block("oak_pressure_plate"))
    editor.placeBlock(addY(rect.begin + ivec2(2, 2), y), Block("oak_pressure_plate"))

    placeEntity(addY(rect.last - ivec2(1, 1), y), "item_frame", {"Facing":1, "Item":{ "id":"minecraft:carrot", "Count":1}})
    placeEntity(addY(rect.last - ivec2(0, 3), y), "glow_item_frame", {"Facing":1, "Item":{ "id":"minecraft:chicken", "Count":1}})
    placeEntity(addY(rect.last - ivec2(0, 4), y), "item_frame", {"Facing":1, "Item":{ "id":"minecraft:baked_potato", "Count":1}})

    y=y+1

    # print(f"height {height}")

    if (height == 2):
        editor.placeBlock(addY(rect.begin, ceiling), Block("red_concrete"))
        editor.placeBlock(addY(ivec2(rect.last.x, rect.begin.y), ceiling), Block("red_concrete"))

        editor.placeBlock(addY(rect.begin, ceiling - 1), Block("lantern", {"hanging": True}))
        editor.placeBlock(addY(ivec2(rect.last.x, rect.begin.y), ceiling-1), Block("lantern", {"hanging": True}))

    elif(height > 2):

        editor.placeBlock(addY(rect.begin + ivec2(1, 1), ceiling), Block("red_concrete"))
        editor.placeBlock(addY(rect.begin + ivec2(1, 2), ceiling), Block("red_concrete"))
        editor.placeBlock(addY(rect.begin + ivec2(2, 1), ceiling), Block("red_concrete"))
        editor.placeBlock(addY(rect.begin + ivec2(2, 2), ceiling), Block("red_concrete"))

        editor.placeBlock(addY(rect.begin + ivec2(1, 1), ceiling-1), Block("lantern", {"hanging": True}))
        editor.placeBlock(addY(rect.begin + ivec2(1, 2), ceiling-1), Block("lantern", {"hanging": True}))
        editor.placeBlock(addY(rect.begin + ivec2(2, 1), ceiling-1), Block("lantern", {"hanging": True}))
        editor.placeBlock(addY(rect.begin + ivec2(2, 2), ceiling-1), Block("lantern", {"hanging": True}))

        editor.placeBlock(addY(rect.last - ivec2(0, 3), y), Block("stone_stairs", {"facing": "east"}))
        

def generateStudy(y, rect, height):
    geometry.placeRect(editor, rect, y, Block("white_carpet"))

    editor.placeBlock(addY(rect.begin, y), Block("bookshelf"))
    editor.placeBlock(addY(rect.begin + ivec2(1, 0), y), Block("bookshelf"))
    editor.placeBlock(addY(rect.begin + ivec2(0, 1), y), Block("bookshelf"))
    editor.placeBlock(addY(rect.begin + ivec2(0, 3), y), Block("bookshelf"))
    editor.placeBlock(addY(rect.begin + ivec2(0, 4), y), Block("oak_fence"))
    editor.placeBlock(addY(rect.begin + ivec2(0, 5), y), Block("oak_fence"))
    editor.placeBlock(addY(rect.begin + ivec2(1, 4), y), Block("oak_stairs", {"facing": "east"}))
    editor.placeBlock(addY(rect.begin + ivec2(2, 5), y), Block("potted_mangrove_propagule"))

    editor.placeBlock(addY(rect.last, y), Block("bookshelf"))
    editor.placeBlock(addY(rect.last - ivec2(0, 1), y), Block("oak_fence"))
    editor.placeBlock(addY(rect.last - ivec2(0, 2), y), Block("oak_fence"))
    editor.placeBlock(addY(rect.last - ivec2(1, 1), y), Block("oak_stairs", {"facing": "west"}))
    editor.placeBlock(addY(rect.last - ivec2(2, 0), y), Block("potted_mangrove_propagule"))

    y = y+1

    editor.placeBlock(addY(rect.begin, y), Block("bookshelf"))
    editor.placeBlock(addY(rect.begin + ivec2(1, 0), y), Block("bookshelf"))
    editor.placeBlock(addY(rect.begin + ivec2(0, 1), y), Block("bookshelf"))
    editor.placeBlock(addY(rect.begin + ivec2(0, 3), y), Block("lantern"))
    editor.placeBlock(addY(rect.begin + ivec2(0, 4), y), Block("oak_pressure_plate"))
    editor.placeBlock(addY(rect.begin + ivec2(0, 5), y), Block("oak_pressure_plate"))


    editor.placeBlock(addY(rect.last, y), Block("lantern"))
    editor.placeBlock(addY(rect.last - ivec2(0, 1), y), Block("oak_pressure_plate"))
    editor.placeBlock(addY(rect.last - ivec2(0, 2), y), Block("oak_pressure_plate"))


def generateFloor(y, outlineRect, inlineRect, height, type):
    geometry.placeRectOutline(editor, outlineRect, y, Block("smooth_quartz"))
    geometry.placeRect(editor, inlineRect, y, Block("dark_oak_planks"))

    if(type != 3):
        tmp_rand = random.randint(1, 2)
        if(tmp_rand == 1):
            generateLivingroom(y+1, inlineRect.between(inlineRect.begin, ivec2(inlineRect.last.x, inlineRect.center.y-1)), height)
        else:
            generateKitchen(y+1, inlineRect.between(inlineRect.begin, ivec2(inlineRect.last.x, inlineRect.center.y-1)), height)

        tmp_rand = random.randint(1, 2)
        if(tmp_rand == 1):
            generateBedroom(y+1, inlineRect.between(ivec2(inlineRect.begin.x, inlineRect.center.y), inlineRect.last), height)
        else:
            generateStudy(y+1, inlineRect.between(ivec2(inlineRect.begin.x, inlineRect.center.y), inlineRect.last), height)
        
        

    else:
        type = 2
    

    stair_place = inlineRect.last + ivec2(-1, -5)
    if (type != 1):
        if (height == 0):
            editor.placeBlock(addY(stair_place + ivec2(0, -1), y), Block("air"))

        elif (height == 2):
            for i in range(height+1):
                editor.placeBlock(addY(stair_place, y), Block("air"))
                stair_place = stair_place + ivec2(0,1)

            editor.placeBlock(addY(stair_place + ivec2(0,1), y), Block("dark_oak_stairs", {"facing": "south"}))        

        else:
            for i in range(height):
                editor.placeBlock(addY(stair_place, y), Block("air"))
                stair_place = stair_place + ivec2(0,1)
            editor.placeBlock(addY(stair_place, y), Block("dark_oak_stairs", {"facing": "south"}))



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

    return y+1


def generateWall(y, outlineRect, wall_color):
    geometry.placeRectOutline(
        editor, outlineRect, y, Block(wall_color))
    return y+1

# type 1=single 2=double


def generateWindows(y, outlineRect, type):

    startEast = outlineRect.begin + ivec2(1, 0)
    startWest = ivec2(outlineRect.end.x - 1,
                      outlineRect.begin.y) + ivec2(-1, 0)
    endEast = ivec2(outlineRect.begin.x, outlineRect.end.y) + ivec2(1, -1)
    endWest = ivec2(outlineRect.end) + ivec2(-2, -1)

    if(type == 3):
        type = 2


    diff = startWest - startEast
    single_middle = (diff.x % 6 == 0 and type == 2) or (
        diff.x % 4 == 0 and type == 1)

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

    return y+1


def generateStory(y, inlineRect, outlineRect, height, type, is_ground, wall_color):
    y = generateFloor(y, outlineRect, inlineRect, height, type)
    tmp_y = y
    stair = inlineRect.last - ivec2(1, 5)

    q = 0
    while(q < height):
        generateWall(y, outlineRect, wall_color)
        if(height <= 2):
            editor.placeBlock(addY(stair, y), Block(
                "dark_oak_planks"))
            editor.placeBlock(addY(stair + ivec2(0, -1), y), Block(
                "ladder", {"facing": "north"}))
        else:
            editor.placeBlock(addY(stair, y), Block(
                "dark_oak_stairs", {"facing": "south"}))
            stair = stair + ivec2(0, 1)

        y = generateWindows(y, outlineRect, type)
        q = q+1

    if (is_ground):
        west = ivec2(outlineRect.end.x, outlineRect.begin.y) + ivec2(-2, 0)
        editor.placeBlock(addY(west, tmp_y), Block(
            "dark_oak_door", {"facing": "south"}))

    return y


def generateFacade(y, outlineA, outlineB, rooftop):

    rooftop = rooftop-1
    east = ivec2(outlineA)
    west = ivec2(outlineB.x, outlineA.y)
    diff = west - east
    even = diff % 2 != 0
    flip = "top"

    while(diff.x > 0):
        # print(f"west: {tuple(west)} east: {tuple(east)} diff: {tuple(diff)}, y: {y}, top: {rooftop}")

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
            # print("top 1")

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
            # print("glass")
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

    # print(diff.x)

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
            # print(chunkRect)
            
            chunkSlice = editor.loadWorldSlice(chunkRect)
            surface = chunkSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
            liquid = surface - chunkSlice.heightmaps["OCEAN_FLOOR"]

            # print(surface)

            # print(surface.max() - surface.min())

            if (liquid.sum() > 10):
                break

            if surface.max() - surface.min() <= 3 :
                return chunk * ivec2(16, 16)

            chunk = chunk + ivec2(0, 1)
        chunk = ivec2(chunk.x + 1, buildSlice.chunkRect.begin.y + 1)

    print("Not found suitable area")
    return False


def findRect(buildRect, size):
    size = size + ivec2(0, 12)
    point = buildRect.begin

    while (point.y < buildRect.last.y):
        while(point.x < buildRect.last.x):
        

            pointRect = Rect(point, size)

            # print(pointRect)

            pointSlice = editor.loadWorldSlice(pointRect)
            surface = pointSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]
            liquid = surface - pointSlice.heightmaps["OCEAN_FLOOR"]

            # print(surface)

            surfaceDiff = surface.max() - surface.min()

            if (surfaceDiff <= 3 and liquid.sum() == 0):
                return point + ivec2(0, 9)
            
            point = point + ivec2(size.x , 0)
        point = ivec2(buildRect.begin.x, point.y + size.y)

    print("Not found suitable area")
    return False


def generateCanal(y, offset, size):
    frontRect = Rect(offset + ivec2(0, -9), ivec2(7, 9))
    for i in range(4):
        geometry.placeRect(editor, frontRect, y + i, Block("air"))

    baseRect = Rect(offset + ivec2(0, -5), size + ivec2(0, 8))
    geometry.placeRect(editor, baseRect, y - 1, Block("stone_bricks"))

    editor.placeBlock(addY(baseRect.begin + ivec2(1, 0), y-1), Block("grass_block"))
    editor.placeBlock(addY(baseRect.begin + ivec2(2, 0), y-1), Block("dirt"))
    editor.placeBlock(addY(baseRect.begin + ivec2(3, 0), y-1), Block("grass_block"))

    trunk_rand = random.randint(1, 100)
    trunk = 8 #30%
    if (trunk_rand > 30 and trunk_rand <= 55): #25%
        trunk = 7
    elif (trunk_rand > 55 and trunk_rand <= 80): #25%
        trunk = 9
    elif (trunk_rand > 80 and trunk_rand <= 90): #10%
        trunk = 6
    elif (trunk_rand > 90): #10%
        trunk = 10

    foliage_rand = random.randint(1, 100)
    foliage = 5 #30%
    if (foliage_rand > 30 and foliage_rand <= 55): #25%
        foliage = 4
    elif (foliage_rand > 55 and foliage_rand <= 80): #25%
        foliage = 6
    elif (foliage_rand > 80 and foliage_rand <= 90): #10%
        foliage = 3
    elif (foliage_rand > 90): #10%
        foliage = 7

    # print(f"trunk: {trunk} foliage: {foliage}")


    tmp_y = y
    for i in range(trunk):
        editor.placeBlock(addY(baseRect.begin + ivec2(2, 0), tmp_y), Block("acacia_log"))
        tmp_y = tmp_y + 1

    editor.placeBlock(addY(baseRect.begin+ ivec2(1, 0), tmp_y - 1), Block("oak_leaves"))
    editor.placeBlock(addY(baseRect.begin + ivec2(3, 0), tmp_y - 1), Block("oak_leaves"))
    editor.placeBlock(addY(baseRect.begin + ivec2(2, 1), tmp_y - 1), Block("oak_leaves"))
    editor.placeBlock(addY(baseRect.begin + ivec2(2, -1), tmp_y - 1), Block("oak_leaves"))

    for i in range(foliage):
        editor.placeBlock(addY(baseRect.begin + ivec2(1, 0), tmp_y), Block("acacia_log"))
        editor.placeBlock(addY(baseRect.begin + ivec2(3, 0), tmp_y), Block("acacia_log"))
        editor.placeBlock(addY(baseRect.begin + ivec2(2, 1), tmp_y), Block("acacia_log"))
        editor.placeBlock(addY(baseRect.begin + ivec2(2, -1), tmp_y), Block("acacia_log"))

        editor.placeBlock(addY(baseRect.begin + ivec2(0, 0), tmp_y), Block("oak_leaves"))
        editor.placeBlock(addY(baseRect.begin + ivec2(4, 0), tmp_y), Block("oak_leaves"))
        editor.placeBlock(addY(baseRect.begin + ivec2(2, 2), tmp_y), Block("oak_leaves"))
        editor.placeBlock(addY(baseRect.begin + ivec2(2, -2), tmp_y), Block("oak_leaves"))

        editor.placeBlock(addY(baseRect.begin + ivec2(1, 1), tmp_y), Block("oak_leaves"))
        editor.placeBlock(addY(baseRect.begin + ivec2(3, -1), tmp_y), Block("oak_leaves"))
        editor.placeBlock(addY(baseRect.begin + ivec2(3, 1), tmp_y), Block("oak_leaves"))
        editor.placeBlock(addY(baseRect.begin + ivec2(1, -1), tmp_y), Block("oak_leaves"))
        tmp_y = tmp_y + 1


    editor.placeBlock(addY(baseRect.begin + ivec2(2, 0), tmp_y), Block("acacia_log"))
    editor.placeBlock(addY(baseRect.begin+ ivec2(1, 0), tmp_y), Block("oak_leaves"))
    editor.placeBlock(addY(baseRect.begin + ivec2(3, 0), tmp_y), Block("oak_leaves"))
    editor.placeBlock(addY(baseRect.begin + ivec2(2, 1), tmp_y), Block("oak_leaves"))
    editor.placeBlock(addY(baseRect.begin + ivec2(2, -1), tmp_y), Block("oak_leaves"))
    tmp_y = tmp_y + 1

    editor.placeBlock(addY(baseRect.begin + ivec2(2, 0), tmp_y), Block("oak_leaves"))    

    canalRect = Rect(offset + ivec2(0, -9), ivec2(size.x, 4))
    geometry.placeRect(editor, canalRect, y - 1, Block("water"))
    geometry.placeRect(editor, canalRect, y - 2, Block("water"))




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


    random_width = random.randint(1, 100)
    width = 7 #40%
    if (random_width > 40 and random_width <= 60): #20%
        width = 6
    elif (random_width > 60 and random_width <= 80): #20%
        width = 8
    elif (random_width > 80 and random_width <= 90): #10%
        width = 5
    elif (random_width > 90): #10%
        width = 9

    size = ivec2(width, 14)


    offset = findRect(buildRect, size)
    
    if (not offset):
        print("could not find suitable area")
        return

    # print(tuple(offset))
    

    outlineA = offset
    outlineB = outlineA + size - (1, 1)
    inlineA = outlineA + (1, 1)

    outlineRect = Rect(outlineA, size)
    inlineRect = Rect(inlineA, size + ivec2(-2, -2))
    worldSlice = editor.loadWorldSlice(outlineRect)
    heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

    random_wall = random.randint(1, 100)
    wall_color = "bricks" #25%
    if (random_wall > 25 and random_wall <= 40): #15%
        wall_color = "mud_bricks"
    elif (random_wall > 40 and random_wall <= 55): #15%
        wall_color = "stone_bricks"
    elif (random_wall > 55 and random_wall <= 70): #15%
        wall_color = "smooth_quartz"
    elif (random_wall > 70 and random_wall <= 80): #10%
        wall_color = "end_stone_bricks"
    elif (random_wall > 80 and random_wall <= 90): #10%
        wall_color = "deepslate_bricks"
    elif (random_wall > 90): #10%
        wall_color = "red_nether_bricks"


    y = heightmap.min()

    generateCanal(y, offset, size)

    # print (f"generate fundation {outlineRect}")
    y = generateFundation(y, inlineRect, outlineRect, heightmap)

    y = generateStory(y, inlineRect, outlineRect, 3, 1, True, wall_color)

    rand_floor = random.randint(1, 100)

    floor_ctr = 2 #40%
    if (rand_floor > 40 and rand_floor <= 60): #20%
        floor_ctr = 1
    elif (rand_floor > 60 and rand_floor <= 80): #20%
        floor_ctr = 3
    elif (rand_floor > 80 and rand_floor <= 90): #10%
        floor_ctr = 0
    elif (rand_floor > 90): #10%
        floor_ctr = 4

    q = 0
    while (q < floor_ctr):
        y = generateStory(y, inlineRect, outlineRect, 3, 2, False, wall_color)
        q = q+1

    y = generateStory(y, inlineRect, outlineRect, 2, 2, False, wall_color)

    y = generateFloor(y, outlineRect, inlineRect, 0, 3)

    roof_rand = random.randint(1, 100)
    if (roof_rand <= 70):
        rooftop = generateRoof(y, outlineA, outlineB)
        generateFacade(y, outlineA, outlineB, rooftop)

    # flat roof 30% of the time


editor = Editor()

if (len(sys.argv)>1):
    print(f"random seed: {sys.argv[1]}")
    random.seed(sys.argv[1])
else:
    print("no random seed was provided")

while(True):
    main()
