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
from colorama import init as colorama_init, Fore, Style
from modules.generator import Generator
from modules.base import Base
from modules.permutations import Permutations


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
                        action='store_true',
                        help="Only display the number of permutations.")
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
    colorama_init()
    args = get_arguments()

    # Settings here...
    match args.base.upper():
        case 'WIDE':
            spaces = Base.WIDE
        case 'ORIGINAL':
            spaces = Base.ORIGINAL
        case _:
            spaces = Base.TEST

    if args.demo:
        # Generate a demonstration image.
        pass
    elif args.only_perms:
        # Display the number of permutations for the specified base and colours.
        colour_count = len(args.colours or Generator.colours)
        space_count = len(spaces)
        total_permutations = Permutations.calculate(space_count=space_count, colour_count=colour_count,
                                                    use_all_colours=False)
        inclusive_permutations = Permutations.calculate(space_count=space_count, colour_count=colour_count,
                                                        use_all_colours=True)
        print(f"With {Style.BRIGHT}{Fore.YELLOW}{colour_count}{Style.RESET_ALL} colours", end=' ')
        print(f"{Style.BRIGHT}{Fore.CYAN}{space_count}{Style.RESET_ALL} spaces,", end=' ')
        print(f"there are {Style.BRIGHT}{Fore.GREEN}{total_permutations:,}{Style.RESET_ALL} total permutations.")
        print("Where all the colours have to be used at least once,", end=' ')
        print(f"there are {Style.BRIGHT}{Fore.GREEN}{inclusive_permutations:,}{Style.RESET_ALL} permutations.")

    else:
        # Generate contact sheets.
        gen = Generator(spaces=spaces, colours=args.colours)
        gen.use_all_colours = args.use_all_colours
        gen.sheet_dimensions = (args.sheet_x, args.sheet_y)

        # TODO output folder.
        # TODO contact sheet title.
        # TODO delete existing files.
        # TODO generate a demo image.

        gen.run()


if __name__ == '__main__':
    main()
