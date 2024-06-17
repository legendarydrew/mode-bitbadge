import math


class Permutations:

    @staticmethod
    def calculate(space_count: int, colour_count: int, use_all_colours: bool = False):
        """
        Calculate the number of permutations for the provided number of spaces and colours.
        Each colour can be used at least once.
        :param space_count: the number of available spaces.
        :param colour_count: the number of available colours.
        :param use_all_colours: True if all colours have to be used at least once.
        :return: the total number of permutations.
        """
        if use_all_colours:
            # Each colour has to appear at least once.
            # (i.e. each colour appears 1 <= n <= (space_count - colour_count - 1) times).
            rs = space_count
            perms = 0
            for i in range(1, colour_count + 1):
                perms += math.pow(i, rs)
                rs -= 1
            perms += math.pow(colour_count, space_count - colour_count)
            return int(perms)
        else:
            # Each colour appears 0 <= n <= space_count times.
            return int(math.pow(colour_count, space_count))
