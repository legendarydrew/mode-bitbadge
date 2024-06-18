"""
A script for generating every permutation of SilentMode's Bit Badge
for a defined list of colours.
"""

from modules.canvas import Canvas
from modules.base import Base
from modules.contact_sheet import ContactSheet


def main():
    colours = [
        '#2B59C3',  # SilentMode Blue
        '#49506F',  # SilentMode Grey
        '#11151C',  # SilentMode Black
        '#600587',  # SilentMode Purple
        '#F2F3F2',  # SilentMode White
        '#F5CD2F',  # SilentMode Yellow
    ]

    """
    What I'd like to do next:
    - choose between use all colours or all permutations.
    - display the permutation count.
    - option to just display the permutation count.
    - option to render a demo image.
    - iterate through permutations.
    - display a progress bar.
    - create contact sheets instead of individual images (define images across/down).
    - transparent background colour for Canvas, configurable background colour for the sheets.
    - add a [copyright] notice to contact sheets.
    - generate a video? (á la mode-dotperms)
    """
    c = 0
    sheet = ContactSheet(items_across=4, items_down=3, title="Contact Sheet")
    for i in range(20):
        canvas = Canvas(spaces=Base.ORIGINAL)
        canvas.draw(colours=colours)
        sheet.add(canvas)
        del canvas
        if sheet.is_full():
            sheet.save(f'sheet-{c}.png')
            sheet.reset()
            c += 1
    sheet.save(f'sheet-{c}.png')

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
