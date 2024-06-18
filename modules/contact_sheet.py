from PIL import Image

from modules.canvas import Canvas


class ContactSheet:
    _x: int = 0
    _y: int = 0
    _canvas: Image = None

    def __init__(self, items_across: int, items_down: int, title: str = None):
        self.items_across = items_across
        self.items_down = items_down
        self.title = title

    def add(self, canvas: Canvas):
        # If adding the first image, create a canvas measuring (across x width) by (down x height).
        image = canvas.image()
        if self._canvas is None:
            canvas_width = self.items_across * image.width
            canvas_height = self.items_down * image.height
            self._canvas = Image.new(mode='RGBA',
                                     size=(canvas_width, canvas_height),
                                     color=(200, 200, 200))

        # Add the image to the canvas.
        self._canvas.alpha_composite(image, dest=(self._x, self._y))
        # self._canvas.paste(image, (self._x, self._y))
        self._x += image.width
        if self._x >= self._canvas.width:
            self._x = 0
            self._y += image.height

    def is_full(self):
        """
        Returns True if the contact sheet is "full" of images.
        :return:
        """
        return self._y >= self._canvas.height

    def save(self, filename: str):
        """
        Save the contact sheet as an image.
        :param filename:
        :return:
        """
        # TODO Add the title.
        # TODO Add a copyright notice at the bottom of the image.
        self._canvas.save(filename)
        pass

    def reset(self):
        """
        Reset the contact sheet by clearing the canvas.
        :return:
        """
        del self._canvas
        self._x = 0
        self._y = 0