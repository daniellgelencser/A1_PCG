import sys

from gdpc import __url__, Editor, Block, geometry
from gdpc.exceptions import InterfaceConnectionError, BuildAreaNotSetError
from gdpc.vector_tools import addY, dropY, ivec2, Rect


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

size = ivec2(7, 14)

buildRect = buildArea.toRect()
outlineA = dropY(buildArea.center)

outlineRect = Rect(outlineA, size)
worldSlice = editor.loadWorldSlice(outlineRect)

# offset = (20, 60)


outlineA = dropY(buildArea.begin)# + offset
outlineB = outlineA + (7, 14) - (1, 1)
inlineA = outlineA + (1, 1)
inlineB = outlineB - (1, 1)

vec = addY(outlineA, buildArea.center.y + 17)
print(f"Block at {tuple(vec)}: {worldSlice.getBlockGlobal(vec)}")

heightmap = worldSlice.heightmaps["MOTION_BLOCKING_NO_LEAVES"]

# localCenter = buildRect.size // 2

# centerHeight = heightmap[tuple(localCenter)]
# centerTopBlock = worldSlice.getBlock(addY(localCenter, centerHeight - 1))

for point in outlineRect.outline:
    height = heightmap[tuple(point - outlineRect.offset)]
    # y = height
    # while (y < centerHeight):
    #     editor.placeBlock(addY(point, y), Block("orange_concrete"))
    #     y = y+1

