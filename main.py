"""
==============================================================================
  permutateBitBadge
  A script for generating every permutation of SilentMode's Bit Badge
  for a defined list of colours.
  This project follows mode-dotperms: a similar project involving LEGO DOTS.
==============================================================================
  developed in 2024 by Drew Maughan (SilentMode)
  with quite a bit of help!
==============================================================================
"""
import time

from alive_progress import alive_bar
from modules.grid import Grid
from modules.base import Base
from modules.contact_sheet import ContactSheet
from modules.permutations import Permutations

"""
What I'd like to do next:
- option to just display the permutation count.
- option to render a demo image.
- generate a video? (á la mode-dotperms)
"""


def main():
    # Settings here...
    spaces = Base.TEST
    colours = [
        '#2B59C3',  # SilentMode Blue
        '#49506F',  # SilentMode Grey
        '#11151C',  # SilentMode Black
        '#600587',  # SilentMode Purple
        '#F2F3F2',  # SilentMode White
        '#F5CD2F',  # SilentMode Yellow
    ]
    use_all_colours = True

    # ---------------------------------------------------------

    _space_counter = [0 for _ in range(len(spaces))]  # keeps track of colours for each space.
    _space_count = len(spaces)
    _colour_count = len(colours)
    _permutation_count = Permutations.calculate(space_count=_space_count,
                                                colour_count=_colour_count,
                                                use_all_colours=use_all_colours)

    def display_permutations():
        all_permutations = Permutations.calculate(space_count=_space_count,
                                                  colour_count=_colour_count,
                                                  use_all_colours=False)
        inclusive_permutations = Permutations.calculate(space_count=_space_count,
                                                        colour_count=_colour_count,
                                                        use_all_colours=True)
        print(
            f"With {len(colours)} colours and {len(spaces)} spaces, there are {all_permutations:,} total permutations.")
        print(
            f"Where all the colours have to be used at least once, there are {inclusive_permutations:,} permutations.")

    def increment_indices():
        """
        Increment the space counters to select the next permutation.
        :return: True if successful, False if the counters have reached the end.
        """
        for _i in range(len(_space_counter)):
            _space_counter[_i] += 1
            if _space_counter[_i] >= _colour_count:
                _space_counter[_i] = 0
            else:
                return True
        return False

    def check_indices():
        """
        Check whether the space counters are valid.
        In the case where each colour must appear at least once, this will return
        False if at least one colour is not represented.
        :return:
        """
        if use_all_colours:
            for _i in range(_colour_count):
                if _i not in _space_counter:
                    return False
        return True

    # Define the contact sheet.
    sheet = ContactSheet(items_across=12, items_down=8)
    _sheet_index = 0

    # Generate each permutation as an image, adding them to our contact sheet.
    print("Generating permutations...")
    try:
        with alive_bar(total=_permutation_count) as bar:
            while True:
                if check_indices():
                    # Update the progress bar.
                    # If you can't see the bar when running this in PyCharm:
                    # https://github.com/rsalmei/alive-progress#forcing-animations-on-pycharm-jupyter-etc
                    time.sleep(0.01)
                    bar()

                    # Select the respective colour hex codes for each space.
                    space_colour_hex = [colours[i] for i in _space_counter]

                    # Draw the grid, then add it to the contact sheet.
                    canvas = Grid(spaces)
                    canvas.draw(colours=space_colour_hex)
                    sheet.add(canvas)
                    del canvas

                    if sheet.is_full():
                        # Save the contact sheet.
                        _sheet_index += 1
                        sheet.save(f'output/sheet-{_sheet_index}.png', number=_sheet_index)
                        sheet.reset()

                if not increment_indices():
                    # Attempt to save the contact sheet as-is.
                    # (This shouldn't save anything if it is empty.)
                    if sheet.save(f'./output/sheet-{_sheet_index + 1}.png', number=_sheet_index + 1):
                        _sheet_index += 1
                    print("Done.")
                    break
    except KeyboardInterrupt:
        print("Stopped...")

    finally:
        # How many contact sheets were generated?
        if _sheet_index == 0:
            print("No contact sheets were generated.")
        elif _sheet_index == 1:
            print("One contact sheet was generated.")
        else:
            print(f"{_sheet_index:,} contact sheets were generated.")


"""
# As a sadistic mathematical challenge:
# how many individual cells would you have to produce for each colour,
# if you were going to physically create every single permutation?
"""

if __name__ == '__main__':
    main()
