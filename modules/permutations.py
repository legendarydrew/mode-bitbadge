import math


class Permutations:
    """
    A class used for calculating numbers or permutations.
    """

    @staticmethod
    def calculate(space_count: int, colour_count: int, use_all_colours: bool = False):
        """
        Calculate the number of permutations for the provided number of spaces and colours.
        :param space_count: the number of available spaces.
        :param colour_count: the number of available colours.
        :param use_all_colours: True if all colours have to be used at least once.
        :return: the total number of permutations.
        """
        if use_all_colours:
            # Each colour has to appear at least once.
            # Thank you, ChatGPT!
            # https://chatgpt.com/share/5a99ae0d-643c-4785-b668-d95e3246ef15
            if colour_count > space_count:
                raise ValueError("Colour count exceeds the number of spaces.")
            else:
                return int(math.factorial(colour_count) *
                           Permutations._stirling_number(subsets=colour_count, spaces=space_count))
        else:
            # Each colour appears 0 <= n <= space_count times.
            return int(math.pow(colour_count, space_count))

    @staticmethod
    def _stirling_number(spaces: int, subsets: int):
        """
        Recursively calculate the Stirling number: the number of ways to partition
        [spaces] items into [subsets] non-empty subsets.
        This helps with determining how many ways we can arrange colours into spaces,
        where each colour appears at least once.
        """

        # The base case is S(s,1) = 1 or S(s,s) = 1.
        if subsets == 1 or subsets == spaces:
            return 1
        else:
            return subsets * Permutations._stirling_number(spaces=spaces - 1, subsets=subsets) + \
                Permutations._stirling_number(spaces=spaces - 1, subsets=subsets - 1)
