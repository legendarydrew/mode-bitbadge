import math


class Hexagon:
    INNER_ANGLE = 360 // 6
    ROTATION_ANGLE = 90  # 0 for a hexagon with vertical edges, 90 for horizontal edges.
    RADIAN_MULTIPLIER = math.pi / 180
    SIN_HEX_ANGLE = math.sin(INNER_ANGLE * RADIAN_MULTIPLIER)
    TAN_HEX_ANGLE = math.tan(INNER_ANGLE * RADIAN_MULTIPLIER)

    def __init__(self, x: int, y: int, side_length: int):
        self.x = x
        self.y = y
        self.side_length = side_length

    def draw(self, draw_handle, fill_colour: str = '#383838', edge_colour: str = '#141414', edge_width: int = 3):
        """
        Draws the hexagon.
        """
        points = self._points()
        draw_handle.polygon(tuple(points), fill=fill_colour, outline=edge_colour, width=edge_width)

    def _points(self):
        """
        Returns a tuple of coordinates representing the corners of the hexagon.
        :return:
        """
        _points = []
        for angle in range(0, 360, self.INNER_ANGLE):
            angle_to_radians = self._degrees_to_radians(self.ROTATION_ANGLE + angle)
            px = self.x + math.sin(angle_to_radians) * self.side_length
            py = self.y + math.cos(angle_to_radians) * self.side_length
            _points.append((px, py))
        return tuple(_points)

    @staticmethod
    def _degrees_to_radians(theta: int | float):
        """
        Returns the specified degrees converted to radians.
        """
        return theta * Hexagon.RADIAN_MULTIPLIER

    @staticmethod
    def dimensions(side_length: int):
        """
        Calculate and return the dimensions of a hexagon with each side of
        the specified length.
        # We can use trigonometry:
        # https://www.bbc.co.uk/bitesize/topics/z93rkqt/articles/z9pd239#zq7b9ty
        :param side_length: the length of each hexagon side.
        :return: information about the hexagon's dimensions.
        """

        # Half the height of the hexagon (edge to edge).
        # We have the hypotenuse (side_length) and the inner angle.
        # We're looking for the opposite side to the inner angle (>45°).
        # sin(theta) = opposite / hypotenuse
        # > sin(theta) * hypotenuse = opposite
        edge_to_centre = Hexagon.SIN_HEX_ANGLE * side_length

        # The "point" measurement: from one point to the centre, less half the width.
        # This is adjacent to the inner angle.
        # tan(theta) = opposite / adjacent
        # > adjacent = opposite / tan(theta)
        point_length = edge_to_centre / Hexagon.TAN_HEX_ANGLE

        return HexagonDimensions(width=(2 * point_length) + side_length,
                                 height=2 * edge_to_centre,
                                 point=point_length)


class HexagonDimensions:
    def __init__(self, width, height, point):
        self.width = int(width)
        self.height = int(height)
        self.point = int(point)
        self.increment = {
            'x': int(width - point),
            'y': int(height / 2)
        }

    def __repr__(self):
        return f"w: {self.width} h: {self.height} p: {self.point} i: {self.increment}"
