"""Tests functionality of PyVoteview validators"""

from pytest import raises

from pyvoteview._validators import (
    CURRENT_CONGRESS_NUMBER,
    CURRENT_YEAR,
    _validate_chamber,
    _validate_congress_number,
)


# _validate_congress_number ----------------------------------------------------
def test__validate_congress_number() -> None:
    """Tests that _validate_congress_number works on three cases:

    1. No exception
    2. Raises exception when congress_number < 1
    3. Raises exception when congress_number > current congress_number
    """

    # Case 1
    _validate_congress_number(100)

    # Case 2
    with raises(
        ValueError,
        match=(
            "This Congress couldn't have occurred, "
            "because the 1st Congress started in 1789"
        ),
    ):
        _validate_congress_number(0)

    # Case 3
    with raises(
        ValueError,
        match="This Congress would occur after "
        rf"{CURRENT_CONGRESS_NUMBER} \({CURRENT_YEAR}\).",
    ):
        _validate_congress_number(CURRENT_CONGRESS_NUMBER + 1)


# _validate_chamber -----------------------------------------------------------
def test__validate_chamber() -> None:
    """Tests that _validate_chamber() passes on two conditions:

    1. A valid string ("House" or "Senate")
    2. Raises an error on an invalid string
    """

    # Case 1
    _validate_chamber("House")
    _validate_chamber("Senate")

    # Case 2
    bad_input = "Supreme Court"
    with raises(
        ValueError,
        match=(
            "Chamber must be one of House or Senate, "
            f"but {bad_input} was entered.  The input is case sensitive."
        ),
    ):
        _validate_chamber(bad_input)
