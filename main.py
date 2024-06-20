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
import os
import random

from colorama import init as colorama_init, Fore, Back, Style, just_fix_windows_console
from modules.generator import Generator
from modules.base import Base
from modules.grid import Grid
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
                        action='store_true',
                        help="Generate a demonstration image.")
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


def header():
    line_width = os.get_terminal_size().columns
    colour_bar = ''
    colour_bar += f"{Style.BRIGHT}{Back.LIGHTBLUE_EX}{' ' * (line_width // 6)}{Style.RESET_ALL}"
    colour_bar += f"{Style.DIM}{Back.WHITE}{' ' * (line_width // 6)}{Style.RESET_ALL}"
    colour_bar += f"{Style.NORMAL}{Back.BLACK}{' ' * (line_width // 6)}{Style.RESET_ALL}"
    colour_bar += f"{Style.NORMAL}{Back.MAGENTA}{' ' * (line_width // 6)}{Style.RESET_ALL}"
    colour_bar += f"{Style.BRIGHT}{Back.WHITE}{' ' * (line_width // 6)}{Style.RESET_ALL}"
    colour_bar += f"{Style.BRIGHT}{Back.LIGHTYELLOW_EX}{' ' * (line_width // 6)}{Style.RESET_ALL}"

    print()
    print(colour_bar)
    print("BIT BADGE Permutations".center(line_width))
    print("by Drew Maughan (SilentMode)".center(line_width))
    print(colour_bar)
    print()


def display_permutations(space_count, colour_count):
    """
    Display the total number of permutations for the provided values.
    :param space_count:
    :param colour_count:
    :return:
    """
    total_permutations = Permutations.calculate(space_count=space_count, colour_count=colour_count,
                                                use_all_colours=False)
    inclusive_permutations = Permutations.calculate(space_count=space_count, colour_count=colour_count,
                                                    use_all_colours=True)
    print(f"With {Style.BRIGHT}{Fore.YELLOW}{colour_count}{Style.RESET_ALL} colours", end=' ')
    print(f"and {Style.BRIGHT}{Fore.CYAN}{space_count}{Style.RESET_ALL} spaces,", end=' ')
    print(f"there are {Style.BRIGHT}{Fore.GREEN}{total_permutations:,}{Style.RESET_ALL} total permutations.")
    print("Where all the colours have to be used at least once,", end=' ')
    print(f"there are {Style.BRIGHT}{Fore.GREEN}{inclusive_permutations:,}{Style.RESET_ALL} permutations.")


def demo_image(filename, spaces, colours):
    """
    Generate and save a demonstration image of a single permutation.
    :param filename: the image file to save.
    :param spaces:
    :param colours:
    """
    random_colours = [colours[int(random.random() * len(colours))] for _ in range(len(spaces))]
    grid = Grid(spaces)
    grid.draw(random_colours)
    grid.image().save(filename)
    print(f"A demonstration image was created at {filename}.")


def main():
    colorama_init()
    just_fix_windows_console()
    args = get_arguments()

    # Settings here...
    match args.base.upper():
        case 'WIDE':
            spaces = Base.WIDE
        case 'ORIGINAL':
            spaces = Base.ORIGINAL
        case _:
            spaces = Base.TEST

    header()

    if args.demo:
        # Generate a demonstration image.
        demo_filename = f"{args.folder}/demo.png"
        colours = args.colours or Generator.colours
        demo_image(filename=demo_filename, spaces=spaces, colours=colours)

    elif args.only_perms:
        # Display the number of permutations for the specified base and colours.
        colour_count = len(args.colours or Generator.colours)
        space_count = len(spaces)
        display_permutations(space_count=space_count, colour_count=colour_count)

    else:
        # Generate contact sheets.
        gen = Generator(spaces=spaces, colours=args.colours)
        gen.use_all_colours = args.use_all_colours
        gen.sheet_dimensions = (args.sheet_x, args.sheet_y)

        # TODO output folder.
        # TODO contact sheet title.
        # TODO delete existing files.

        gen.run()


if __name__ == '__main__':
    main()
