from PIL import Image, ImageDraw, ImageFont

from modules.canvas import Canvas
from modules.config import Config


class ContactSheet:
    _x: int = 0
    _y: int = 0
    _canvas: Image = None

    def __init__(self, items_across: int, items_down: int):
        self.items_across = items_across
        self.items_down = items_down

    def add(self, canvas: Canvas):
        # If adding the first image, create a canvas measuring (across x width) by (down x height).
        image = canvas.image()
        if self._canvas is None:
            canvas_width = self.items_across * image.width
            canvas_height = self.items_down * image.height + Config.SHEET_TITLE_HEIGHT + Config.SHEET_FOOTER_HEIGHT
            self._canvas = Image.new(mode='RGBA',
                                     size=(canvas_width, canvas_height),
                                     color=Config.SHEET_BG_COLOUR)

        # Add the image to the canvas.
        self._canvas.alpha_composite(image, dest=(self._x, self._y + Config.SHEET_TITLE_HEIGHT))
        self._x += image.width
        if self._x >= self._canvas.width:
            self._x = 0
            self._y += image.height

    def is_full(self):
        """
        Returns True if the contact sheet is "full" of images.
        :return:
        """
        return self._y >= self._canvas.height - Config.SHEET_TITLE_HEIGHT - Config.SHEET_FOOTER_HEIGHT

    def save(self, filename: str, number: int):
        """
        Save the contact sheet as an image.
        :param number:
        :param filename:
        :return:
        """
        if self._canvas is not None:
            draw_handle = ImageDraw.Draw(self._canvas)
            title_fount = ImageFont.truetype(Config.SHEET_TITLE_FOUNT, Config.SHEET_TITLE_TEXT_SIZE)
            footer_fount = ImageFont.truetype(Config.SHEET_FOOTER_FOUNT, Config.SHEET_FOOTER_TEXT_SIZE)

            # Add the title.
            draw_handle.text(text=Config.SHEET_TITLE_TEXT.replace('%u', str(number)).upper(),
                             font=title_fount,
                             fill=Config.SHEET_TITLE_TEXT_COLOUR,
                             spacing=0,
                             xy=(self._canvas.width / 2, Config.SHEET_TITLE_HEIGHT / 2),
                             anchor='mm')

            # Add a copyright notice at the bottom of the image.
            draw_handle.text(text=Config.SHEET_FOOTER_TEXT,
                             font=footer_fount,
                             fill=Config.SHEET_FOOTER_TEXT_COLOUR,
                             xy=(self._canvas.width / 2, self._canvas.height - (Config.SHEET_FOOTER_HEIGHT / 2)),
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
