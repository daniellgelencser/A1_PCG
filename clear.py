import sys

from gdpc import __url__, Editor, Block, geometry
from gdpc.exceptions import InterfaceConnectionError, BuildAreaNotSetError
from gdpc.vector_tools import addY, dropY, Rect, ivec2


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

buildRect = buildArea.toRect()
worldSlice = editor.loadWorldSlice(buildRect)

offset = (20, 60)

outlineA = dropY(buildArea.begin) + (0, -1) + offset

outlineRect = Rect(outlineA + ivec2(-1, -41), ivec2(7, 14) + ivec2(30, 50))


# clear area
i = 1
while (i<50):
    geometry.placeRect(editor, outlineRect, buildArea.begin.y + i, Block("air"))
    i = i+1
