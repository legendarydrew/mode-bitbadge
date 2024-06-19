"""
A script for generating every permutation of SilentMode's Bit Badge
for a defined list of colours.
"""
import time

from alive_progress import alive_bar
from modules.canvas import Canvas
from modules.base import Base
from modules.contact_sheet import ContactSheet
from modules.permutations import Permutations


def main():
    spaces = Base.TEST
    colours = [
        '#2B59C3',  # SilentMode Blue
        '#49506F',  # SilentMode Grey
        '#11151C',  # SilentMode Black
        '#600587',  # SilentMode Purple
        '#F2F3F2',  # SilentMode White
        '#F5CD2F',  # SilentMode Yellow
    ]
    use_all_colours = False

    """
    What I'd like to do next:
    - display the permutation count.
    - option to just display the permutation count.
    - option to render a demo image.
    - display a progress bar.
    - add a [copyright] notice to contact sheets.
    - generate a video? (á la mode-dotperms)
    """
    space_colour_ids = [0 for _ in range(len(spaces))]

    spaces_count = len(spaces)
    colours_count = len(colours)
    permutation_count = Permutations.calculate(space_count=spaces_count,
                                               colour_count=colours_count,
                                               use_all_colours=use_all_colours)
    print(f"Number of spaces: {spaces_count:,}")
    print(f"Number of colours: {colours_count:,}")
    print("Colour usage: " + ('one of each colour' if use_all_colours else 'any combination'))
    print(f"Total permutations: {permutation_count:,}\n")

    def increment_indices():
        for _i in range(len(space_colour_ids)):
            space_colour_ids[_i] += 1
            if space_colour_ids[_i] >= colours_count:
                space_colour_ids[_i] = 0
            else:
                return True
        return False

    def check_indices():
        if use_all_colours:
            for _i in range(colours_count):
                if _i not in space_colour_ids:
                    return False
        return True

    sheet = ContactSheet(items_across=10, items_down=6, title="Contact Sheet")
    sheet_index = 0

    with alive_bar(total=permutation_count) as bar:
        while True:
            if check_indices():

                # Update the progress bar.
                # If you can't see the bar when running this in PyCharm:
                # https://github.com/rsalmei/alive-progress#forcing-animations-on-pycharm-jupyter-etc
                time.sleep(0.01)
                bar()

                space_colour_hex = [colours[i] for i in space_colour_ids]

                canvas = Canvas(spaces)
                canvas.draw(colours=space_colour_hex)
                sheet.add(canvas)
                del canvas

                if sheet.is_full():
                    sheet.save(f'output/sheet-{sheet_index}.png')
                    sheet.reset()
                    sheet_index += 1

            if not increment_indices():
                break

    # Save the last contact sheet.
    # (This shouldn't save anything if it is empty.)
    sheet.save(f'./output/sheet-{sheet_index}.png')

    print("Done.")


"""
all_permutations = Permutations.calculate(space_count=len(spaces),
                                          colour_count=len(colours),
                                          use_all_colours=False)
print(f"With {len(colours)} colours and {len(spaces)} spaces, there are {all_permutations:,} total permutations.")

inclusive_permutations = Permutations.calculate(space_count=len(spaces),
                                                colour_count=len(colours),
                                                use_all_colours=True)
print(f"Where all the colours have to be used at least once, there are {inclusive_permutations:,} permutations.")

# As a sadistic challenge: how many individual cells would you have to produce
# for each colour, if you were going to create every single permutation?
"""

if __name__ == '__main__':
    main()
