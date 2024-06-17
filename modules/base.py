class Base:
    """
    A convenience class for Bit Badge base definitions.
    """

    """
    Here's how we're defining the hexagonal grid:
    
       0 1 2 3 4         0 1 2 3 4
    ------------      ------------
     0 - - x - -       0 - - x - -
     1 - x - x -       1 - x - x -
     2 - - x - -       2 x - x - x
     3 - x - x -       3 - x - x -
     4 - - x - -       4 x - x - x
     5 - x - x -       5 - x - x -
     6 - - x - -       6 - - x - -
    Original base       Wide base
    """

    ORIGINAL = (
        (2, 0),
        (1, 1),
        (3, 1),
        (2, 2),
        (1, 3),
        (3, 3),
        (2, 4),
        (1, 5),
        (3, 5),
        (2, 6),
    )

    WIDE = (
        (2, 0),
        (1, 1),
        (3, 1),
        (0, 2),
        (2, 2),
        (4, 2),
        (1, 3),
        (3, 3),
        (0, 4),
        (2, 4),
        (4, 4),
        (1, 5),
        (3, 5),
        (2, 6),
    )
