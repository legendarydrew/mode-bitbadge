from PIL import Image, ImageDraw, ImageFont

from modules.canvas import Canvas


class ContactSheet:
    _x: int = 0
    _y: int = 0
    _canvas: Image = None
    _title_height: int = 40
    _footer_height: int = 30

    def __init__(self, items_across: int, items_down: int, title: str = None):
        self.items_across = items_across
        self.items_down = items_down
        self.title = title

    def add(self, canvas: Canvas):
        # If adding the first image, create a canvas measuring (across x width) by (down x height).
        image = canvas.image()
        if self._canvas is None:
            canvas_width = self.items_across * image.width
            canvas_height = self.items_down * image.height + self._title_height + self._footer_height
            self._canvas = Image.new(mode='RGBA',
                                     size=(canvas_width, canvas_height),
                                     color=(200, 200, 200))

        # Add the image to the canvas.
        self._canvas.alpha_composite(image, dest=(self._x, self._y + self._title_height))
        self._x += image.width
        if self._x >= self._canvas.width:
            self._x = 0
            self._y += image.height

    def is_full(self):
        """
        Returns True if the contact sheet is "full" of images.
        :return:
        """
        return self._y >= self._canvas.height - self._title_height - self._footer_height

    def save(self, filename: str):
        """
        Save the contact sheet as an image.
        :param filename:
        :return:
        """
        if self._canvas is not None:
            draw_handle = ImageDraw.Draw(self._canvas)
            title_fount = ImageFont.truetype("./founts/CooperHewitt-Bold.otf", self._title_height * 0.55)
            footer_fount = ImageFont.truetype("./founts/CooperHewitt-Light.otf", self._footer_height * 0.3)

            # Add the title.
            draw_handle.text(text=self.title.upper(),
                             font=title_fount,
                             fill='#09090A',
                             spacing=0,
                             xy=(self._canvas.width / 2, self._title_height / 2),
                             anchor='mm')

            # Add a copyright notice at the bottom of the image.
            draw_handle.text(text='© Drew Maughan (SilentMode).',
                             font=footer_fount,
                             fill='#09090A',
                             xy=(self._canvas.width / 2, self._canvas.height - (self._footer_height / 2)),
                             anchor='mm')

            self._canvas.save(filename)
            return True
        return False

    def reset(self):
        """
        Reset the contact sheet by clearing the canvas.
        :return:
        """
        del self._canvas
        self._x = 0
        self._y = 0
