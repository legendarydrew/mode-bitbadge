"""
A script for generating every permutation of SilentMode's Bit Badge
for a defined list of colours.
"""

from modules.canvas import Canvas
from modules.base import Base
from modules.contact_sheet import ContactSheet


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
    use_all_colours = True

    """
    What I'd like to do next:
    - choose between use all colours or all permutations.
    - display the permutation count.
    - option to just display the permutation count.
    - option to render a demo image.
    - display a progress bar.
    - add a [copyright] notice to contact sheets.
    - generate a video? (á la mode-dotperms)
    """
    space_colour_ids = [0 for _ in range(len(spaces))]

    def increment_indices():
        for _i in range(len(space_colour_ids)):
            space_colour_ids[_i] += 1
            if space_colour_ids[_i] >= len(colours):
                space_colour_ids[_i] = 0
            else:
                return True
        return False

    def check_indices():
        if use_all_colours:
            for _i in range(len(colours)):
                if _i not in space_colour_ids:
                    return False
        return True

    sheet = ContactSheet(items_across=10, items_down=6, title="Contact Sheet")
    sheet_index = 0
    while True:
        if check_indices():
            space_colour_hex = [colours[i] for i in space_colour_ids]

            canvas = Canvas(spaces=Base.ORIGINAL)
            canvas.draw(colours=space_colour_hex)
            sheet.add(canvas)
            del canvas

            if sheet.is_full():
                sheet.save(f'sheet-{sheet_index}.png')
                sheet.reset()
                sheet_index += 1

        if not increment_indices():
            break

    # Save the last contact sheet.
    # (This shouldn't save anything if it is empty.)
    sheet.save(f'sheet-{sheet_index}.png')

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
