"""Validator functions"""

from datetime import UTC, datetime

from ._utilities import _convert_year_to_congress_number

CURRENT_YEAR = datetime.now(tz=UTC).year
CURRENT_CONGRESS_NUMBER = _convert_year_to_congress_number(CURRENT_YEAR)


def _validate_congress_number(congress_number: int) -> None:
    """
    Validate that a number is valid for a Congress.

    Args:
        congress_number: Number to validate.
    """

    if congress_number > CURRENT_CONGRESS_NUMBER:
        err = (
            "This Congress would occur after "
            f"{CURRENT_CONGRESS_NUMBER} ({CURRENT_YEAR})."
        )
        raise ValueError(err)
    if congress_number < 1:
        err = (
            "This Congress couldn't have occurred, "
            "because the 1st Congress started in 1789"
        )
        raise ValueError(err)


def _validate_chamber(chamber: str) -> None:
    """
    Validate that a chamber is either House or Senate.

    Args:
        chamber: Chamber to validate.
    """

    if chamber not in ("House", "Senate"):
        err = (
            "Chamber must be one of House or Senate, "
            f"but {chamber} was entered.  The input is case sensitive."
        )
        raise ValueError(err)


def _validate_category(category: str) -> None:
    """
    Validate that a category is either votes or members.

    Args:
        category: Category to validate.
    """

    if category not in ("members", "rollcalls", "votes"):
        err = (
            f"{category} was selected, but is not one of: "
            "members, rollcalls, votes"
        )
        raise ValueError(err)
