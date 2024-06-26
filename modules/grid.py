from PIL import Image, ImageDraw

from modules.config import Config
from modules.hexagon import Hexagon


class Grid:
    """
    A class used to draw the hexagonal grid of a Bit Badge.
    """

    _im = None
    _draw_handle = None

    hexagons = None
    hexagons_across = None
    hexagons_down = None

    def __init__(self, spaces: list):
        self._convert_spaces(spaces)
        self._create_canvas()

    def image(self):
        """
        Returns the image for this canvas.
        :return:
        """
        return self._im

    def _convert_spaces(self, spaces: list):
        """
        Convert a list of points to Hexagon objects.
        """

        # Calculate the coordinates of each hexagon for each of the defined spaces.
        # The coordinates represent the centre of each hexagon.
        min_x = None
        min_y = None
        max_x = None
        max_y = None
        coordinates = []
        hex_dimensions = Hexagon.dimensions(Config.HEXAGON_SIDE_LENGTH)

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
        self.hexagons_across = max(1, max_x - min_x + 1)
        self.hexagons_down = max(1, int(max_y - min_y / 2) + 1)
        self.width = int(
            (self.hexagons_across * Config.HEXAGON_SIDE_LENGTH) +
            ((self.hexagons_across + 1) * hex_dimensions.point)
        )
        self.height = int((self.hexagons_down + 1) * hex_dimensions.increment['y'])

        # Add the margin to the canvas dimensions.
        self.width += 2 * Config.HEX_GRID_MARGIN
        self.height += 2 * Config.HEX_GRID_MARGIN + Config.HEX_GRID_OUTLINE_WIDTH

        # Shift the coordinates if necessary, so the hexagons are aligned
        # with the top left of the canvas, offset by the margin.
        coordinates = [[
            c[0] - min_x * hex_dimensions.increment['x'] + Config.HEX_GRID_MARGIN,
            c[1] - min_y * hex_dimensions.increment['y'] + Config.HEX_GRID_MARGIN
        ] for c in coordinates]

        # Create the Hexagon objects.
        self.hexagons = tuple([
            Hexagon(c[0], c[1], Config.HEXAGON_SIDE_LENGTH) for c in coordinates
        ])

    def _create_canvas(self):
        self._im = Image.new(mode='RGBA',
                             size=(self.width, self.height))
        self._draw_handle = ImageDraw.Draw(self._im)

    def draw(self, colours: list[str]):
        for index, hexagon in enumerate(self.hexagons):
            fill_colour = colours[index]
            hexagon.draw(draw_handle=self._draw_handle,
                         fill_colour=fill_colour,
                         edge_colour=Config.HEX_GRID_OUTLINE_COLOUR,
                         edge_width=Config.HEX_GRID_OUTLINE_WIDTH)
