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
import argparse
from modules.generator import Generator
from modules.base import Base


def get_arguments():
    """
    Parse and return command line arguments.
    :return:
    """
    parser = argparse.ArgumentParser("main.py")
    parser.add_argument("-b", "--base", help="Which Bit Badge base to use.",
                        type=str,
                        choices=('test', 'original', 'wide'),
                        default='test')
    parser.add_argument("-c", "--colours", help="Colour hex codes to use for the Bit Badge.",
                        nargs="*",
                        type=str)
    parser.add_argument("-a", "--use-all-colours",
                        help="Whether all colours should be used in each permutation.",
                        type=bool,
                        default=False)
    parser.add_argument("-t", "--title",
                        help="The title to use on contact sheets.",
                        type=str,
                        required=False)
    parser.add_argument("-d", "--demo",
                        help="Generate a demonstration image.",
                        type=str)
    parser.add_argument("-p", "--only-perms",
                        help="Display the number of permutations.",
                        type=int,
                        default=False)
    parser.add_argument("-sx", "--sheet-x",
                        help="Set the number of images across on contact sheets.",
                        type=int,
                        default=12)
    parser.add_argument("-sy", "--sheet-y",
                        help="Set the number of images down on contact sheets.",
                        type=int,
                        default=8)
    parser.add_argument("-f", "--folder",
                        help="Save contact sheets in this folder.",
                        type=str,
                        default="./output")
    parser.add_argument("--delete",
                        help="Delete existing contact sheets.",
                        type=int,
                        default=False)
    return parser.parse_args()


def main():
    args = get_arguments()

    # Settings here...
    match args.base.upper():
        case 'WIDE':
            spaces = Base.WIDE
        case 'ORIGINAL':
            spaces = Base.ORIGINAL
        case _:
            spaces = Base.TEST

    colours = [
        '#2B59C3',  # SilentMode Blue
        '#49506F',  # SilentMode Grey
        '#11151C',  # SilentMode Black
        '#600587',  # SilentMode Purple
        '#F2F3F2',  # SilentMode White
        '#F5CD2F',  # SilentMode Yellow
    ]

    gen = Generator(spaces=spaces, colours=colours)
    gen.use_all_colours = args.all_colours
    gen.sheet_dimensions = (args.sheet_x, args.sheet_y)

    # TODO output folder.
    # TODO contact sheet title.
    # TODO display permutations.
    # TODO define colours.
    # TODO delete existing files.
    # TODO generate a demo image.

    gen.run()


if __name__ == '__main__':
    main()
