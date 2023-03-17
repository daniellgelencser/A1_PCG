### Procedural Content Generation in Minecraft

After a build area is selected the house structure can be automatically generated using the `house.py` script.
This scripts can be run with an argument that will be used as the seed for the random generation, however when no random seed is provided, the results will be random.

The algorithm looks for an area where there are no more than 3 blocks difference between the minimum and the maximum elevation of the terrain and no water or lava. The width and height of the house may vary randomly as well.