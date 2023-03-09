import sys

from gdpc import __url__, Editor, Block, geometry
from gdpc.exceptions import InterfaceConnectionError, BuildAreaNotSetError

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

# geometry.placeRect(editor, buildRect, buildArea.begin.y-22, Block("tnt"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y-21, Block("tnt"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y-20, Block("tnt"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y-19, Block("tnt"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y-18, Block("tnt"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y-17, Block("tnt"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y-120, Block("tnt"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y-110, Block("tnt"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y-160, Block("tnt"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y-140, Block("tnt"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y-120, Block("tnt"))

# geometry.placeRect(editor, buildRect, buildArea.begin.y-170, Block("tnt"))

# i = 171
# while(i < 180):
#     geometry.placeRect(editor, buildRect, buildArea.begin.y-i, Block("glass"))
#     print(i)
#     i = i+1

# geometry.placeRect(editor, buildRect, buildArea.begin.y-8, Block("stone"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y-7, Block("stone"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y-6, Block("stone"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y-5, Block("stone"))

# geometry.placeRect(editor, buildRect, buildArea.begin.y-4, Block("dirt"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y-3, Block("dirt"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y-2, Block("dirt"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y-1, Block("light_gray_concrete"))
# geometry.placeRect(editor, buildRect, buildArea.begin.y, Block("light_gray_concrete"))

geometry.placeRectOutline(editor, buildRect, buildArea.begin.y+1, Block("red_concrete"))
