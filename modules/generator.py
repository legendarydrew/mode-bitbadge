import os
import shutil
import time

from alive_progress import alive_bar
from modules.grid import Grid
from modules.base import Base
from modules.contact_sheet import ContactSheet
from modules.permutations import Permutations


class Generator:
    # Settings here...
    spaces: list[tuple[int, int]] = Base.TEST
    colours: list[str] = [
        '#2B59C3',  # SilentMode Blue
        '#49506F',  # SilentMode Grey
        '#11151C',  # SilentMode Black
        '#600587',  # SilentMode Purple
        '#F2F3F2',  # SilentMode White
        '#F5CD2F',  # SilentMode Yellow
    ]
    use_all_colours: bool = True
    delete_existing_sheets: bool = False
    sheet_title: str = ''
    sheet_dimensions: tuple[int, int] = (12, 8)  # items across and down on contact sheets.
    output_folder: str = './output'

    # ---------------------------------------------------------

    _permutation_count: int = None
    _sheet: ContactSheet = None
    _sheet_index: int = 0
    _space_counter: list[int] = None  # keeps track of colours for each space.

    def __init__(self, spaces, colours):
        if spaces:
            self.spaces = spaces
        if colours:
            self.colours = colours
        self._space_counter = [0 for _ in range(len(spaces))]
        self._space_count = len(self.spaces)
        self._colour_count = len(self.colours)

    def _increment(self):
        """
        Increment the space counters to select the next permutation.
        :return: True if successful, False if the counters have reached the end.
        """
        for _i in range(len(self._space_counter)):
            self._space_counter[_i] += 1
            if self._space_counter[_i] >= self._colour_count:
                self._space_counter[_i] = 0
            else:
                return True
        return False

    def _check_indices(self):
        """
        Check whether the space counters are valid.
        In the case where each colour must appear at least once, this will return
        False if at least one colour is not represented.
        :return:
        """
        if self.use_all_colours:
            for _i in range(self._colour_count):
                if _i not in self._space_counter:
                    return False
        return True

    def _sanitise(self):
        """
        Check that the Generator settings are valid.
        :return:
        """
        if not (self.spaces and len(self.spaces) > 0):
            raise ValueError('No spaces are defined.')
        if not (self.colours and len(self.colours) > 1):
            raise ValueError('At least two colours must be defined.')
        if not (self.sheet_dimensions and len(self.sheet_dimensions) > 0):
            raise ValueError('Contact sheet dimensions must be defined.')
        elif len(self.sheet_dimensions) == 1:
            # Only one dimension was provided: let's assume the user wants a square.
            self.sheet_dimensions = (self.sheet_dimensions[0], self.sheet_dimensions[0])
        if self.sheet_dimensions[0] < 1 or self.sheet_dimensions[1] < 1:
            raise ValueError('Each sheet dimension must be >= 1.')
        # TODO check whether the output folder exists.

    def delete_sheets(self):
        """
        Delete any existing contact sheets if configured to.
        https://stackoverflow.com/a/37215944/4073160
        :return:
        """
        if self.delete_existing_sheets:
            files = os.listdir(self.output_folder)
            for file in files:
                if 'sheet' in file:
                    os.remove(f"{self.output_folder}/{file}")

    def run(self):
        """
        Generate the contact sheets.
        :return:
        """
        self._sanitise()
        self._permutation_count = Permutations.calculate(space_count=self._space_count,
                                                         colour_count=self._colour_count,
                                                         use_all_colours=self.use_all_colours)

        # Remove existing contact sheets if required.
        self.delete_sheets()

        # Define the contact sheet.
        self._sheet = ContactSheet(title=self.sheet_title,
                                   items_across=self.sheet_dimensions[0],
                                   items_down=self.sheet_dimensions[1])
        self._sheet_index = 0

        # Generate each permutation as an image, adding them to our contact sheet.
        # The alive_progress package provides an animated progress bar.
        print("Generating permutations...")
        try:
            with alive_bar(total=self._permutation_count) as bar:
                while True:
                    if self._check_indices():
                        # Update the progress bar.
                        # If you can't see the bar when running this in PyCharm:
                        # https://github.com/rsalmei/alive-progress#forcing-animations-on-pycharm-jupyter-etc
                        time.sleep(0.01)
                        bar()

                        # Select the respective colour hex codes for each space.
                        space_colour_hex = [self.colours[i] for i in self._space_counter]

                        # Draw the grid, then add it to the contact sheet.
                        canvas = Grid(self.spaces)
                        canvas.draw(colours=space_colour_hex)
                        self._sheet.add(canvas)
                        del canvas

                        if self._sheet.is_full():
                            self._save_sheet()

                    if not self._increment():
                        # Attempt to save the contact sheet as-is.
                        # (This shouldn't save anything if it is empty.)
                        self._save_sheet()
                        break
        except KeyboardInterrupt:
            print("Stopped...")

        finally:
            # How many contact sheets were generated?
            if self._sheet_index == 0:
                print("No contact sheets were generated.")
            elif self._sheet_index == 1:
                print("A contact sheet was generated.")
            else:
                print(f"{self._sheet_index:,} contact sheets were generated.")

    def _save_sheet(self):
        """
        Save the contact sheet as is.
        Nothing will be saved if the contact sheet is "empty".
        :return:
        """
        next_sheet_index = self._sheet_index + 1
        if self._sheet.save(f'{self.output_folder}/sheet-{next_sheet_index}.png', number=next_sheet_index):
            self._sheet.reset()
            self._sheet_index = next_sheet_index
