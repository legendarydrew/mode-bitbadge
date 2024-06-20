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

from modules.generator import Generator
from modules.base import Base

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

    gen = Generator(spaces=spaces, colours=colours)
    gen.use_all_colours = use_all_colours
    gen.run()


if __name__ == '__main__':
    main()
