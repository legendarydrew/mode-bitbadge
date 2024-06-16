"""
A script for generating every permutation of SilentMode's Bit Badge
for a defined list of colours.
"""
import math

from PIL import Image, ImageDraw

colours = [
    0x2B59C3,  # SilentMode Blue
    0x49506F,  # SilentMode Grey
    0x11151C,  # SilentMode Black
    0x600587,  # SilentMode Purple
    0xF2F3F2,  # SilentMode White
    0xF5CD2F  # SilentMode Yellow
]

# A hexagon...
hex_side_length = 30

# Calculate the dimensions of the hexagon, used for positioning and image size.
# We can use trigonometry: tan(theta) = opposite / adjacent. (Damn, I'm rusty.)
HEX_ANGLE = 360 / 6
TAN_HEX_ANGLE = math.tan(HEX_ANGLE * (math.pi / 180))
hex_height = 2 * TAN_HEX_ANGLE * (hex_side_length / 2)
hex_x_increment = hex_height / TAN_HEX_ANGLE  # adjacent = opposite / tan(theta)
hex_y_increment = hex_height / 2
hex_width = 2 * hex_x_increment + hex_side_length

hex_across = 3
hex_tall = 4

padding = 20
canvas_width = ((hex_across - 1) * hex_width) + (2 * padding)
canvas_height = (hex_tall * hex_height) + (2 * padding)


# Let's try to draw the original Bit Badge.
im = Image.new(mode='RGB',
               size=(int(canvas_width), int(canvas_height)),
               color=(200, 200, 200))
draw = ImageDraw.Draw(im)

mx = canvas_width / 2
spaces = (
    (mx, padding + hex_height / 2),
    (mx - hex_width / 2, padding + hex_y_increment + hex_height / 2),
    (mx, padding + hex_height + (hex_height / 2)),
    (mx + hex_width / 2, padding + hex_y_increment + hex_height / 2),
    (mx - hex_width / 2, padding + hex_y_increment + hex_height + hex_height / 2),
    (mx, padding + (2 * hex_height) + (hex_height / 2)),
    (mx + hex_width / 2, padding + hex_y_increment + hex_height + hex_height / 2),
    (mx - hex_width / 2, padding + hex_y_increment + (2 * hex_height) + hex_height / 2),
    (mx, padding + (3 * hex_height) + (hex_height / 2)),
    (mx + hex_width / 2, padding + hex_y_increment + (2 * hex_height) + hex_height / 2),
)


def get_hexagon_points(x, y, side_length):
    angle = 0
    _points = []
    hex_angle = 360 / 6
    while angle < 360:
        angle_to_radians = (90 + angle) * math.pi / 180
        px = x + math.sin(angle_to_radians) * side_length
        py = y + math.cos(angle_to_radians) * side_length
        _points.append((px, py))
        angle += hex_angle
    return tuple(_points)


for space in spaces:
    points = get_hexagon_points(space[0], space[1], hex_side_length)
    draw.polygon(tuple(points), fill=(200, 280, 10), outline=(20, 20, 30), width=3)

im.save('./demo.png')
