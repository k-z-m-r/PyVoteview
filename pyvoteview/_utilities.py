"""Utility functions"""

from math import floor


def _convert_year_to_congress_number(year: int) -> int:
    """
    Converts a year to the corresponding U.S. Congress number.

    Args:
        year: The year to convert.

    Returns:
        The corresponding Congress number.  Assumes the January which comes at
        the tail end of a Congress is actually part of the next Congress.
    """

    return floor((year - 1789) / 2) + 1
