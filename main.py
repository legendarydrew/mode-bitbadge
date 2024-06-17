"""
A script for generating every permutation of SilentMode's Bit Badge
for a defined list of colours.
"""
import math
import random
from PIL import Image, ImageDraw

from modules.base import Base
from modules.hexagon import Hexagon

colours = [
    '#2B59C3',  # SilentMode Blue
    '#49506F',  # SilentMode Grey
    '#11151C',  # SilentMode Black
    '#600587',  # SilentMode Purple
    '#F2F3F2',  # SilentMode White
    '#F5CD2F'  # SilentMode Yellow
]

# A hexagon...
hex_side_length = 30
hex_edge_width = 2

image_padding = 10

spaces = Base.WIDE

# Calculate the coordinates of each hexagon for each of the defined spaces.
# The coordinates represent the centre of each hexagon.
min_x = None
min_y = None
max_x = None
max_y = None
coordinates = []
hex_dimensions = Hexagon.dimensions(hex_side_length)

for space in spaces:
    x, y = space
    min_x = min(min_x, x) if min_x is not None else x
    min_y = min(min_y, y) if min_y is not None else y
    max_x = max(max_x, x) if max_x is not None else x
    max_y = max(max_y, y) if max_y is not None else y
    hx = (hex_dimensions.width / 2) + (x * hex_dimensions.increment['x'])
    hy = (hex_dimensions.height / 2) + (y * hex_dimensions.increment['y'])
    coordinates.append([hx, hy])

# Determine the canvas dimensions.
hex_across = max(1, max_x - min_x + 1)
hex_down = max(1, int(max_y - min_y / 2) + 1)
canvas_width = int((hex_across * hex_side_length) + ((hex_across + 1) * hex_dimensions.point))
canvas_height = int((hex_down + 1) * hex_dimensions.increment['y'])

# canvas_width += 2 * hex_edge_width
# canvas_height += 2 * hex_edge_width

print("Based on the defined spaces,")
print(f"the hexagonal grid is {hex_across} spaces wide and {hex_down} spaces tall.")
print(f"That gives us a canvas of {canvas_width} x {canvas_height} pixels (before padding).")

# Shift the coordinates if necessary, so they are aligned with the top left
# of the canvas.
coordinates = [[
    c[0] - min_x * hex_dimensions.increment['x'] + image_padding,
    c[1] - min_y * hex_dimensions.increment['y'] + image_padding
] for c in coordinates]

# Create the canvas.
canvas_width += 2 * image_padding
canvas_height += 2 * image_padding + hex_edge_width

im = Image.new(mode='RGB',
               size=(canvas_width, canvas_height),
               color=(200, 200, 200))
draw = ImageDraw.Draw(im)

# Create the hexagons.
hexagons = tuple([Hexagon(c[0], c[1], hex_side_length) for c in coordinates])


def calculate_permutations(space_count, colour_count, use_all_colours=False):
    if use_all_colours:
        rs = space_count
        perms = 0
        for i in range(1, colour_count + 1):
            perms += math.pow(i, rs)
            rs -= 1
        perms += math.pow(colour_count, space_count - colour_count)
        return int(perms)
    else:
        return int(math.pow(colour_count, space_count))


for hexagon in hexagons:
    colour = colours[int(random.random() * len(colours))]
    hexagon.draw(draw_handle=draw, fill_colour=colour, edge_width=hex_edge_width)

im.save('./demo.png')

print("Done.")

"""
all_permutations = calculate_permutations(len(spaces), len(colours))
print(f"With {len(colours)} colours and {len(spaces)} spaces, there are {all_permutations:,} total permutations.")

inclusive_permutations = calculate_permutations(len(spaces), len(colours), True)
print(f"Where all the colours have to be used at least once, there are {inclusive_permutations:,} permutations.")
"""
