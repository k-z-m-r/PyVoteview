"""Tests core functionality of PyVoteview."""

from polars import Float32, Int32, Int64, Utf8
from pytest import raises

from pyvoteview.core import (
    CURRENT_CONGRESS_NUMBER,
    CURRENT_YEAR,
    _convert_year_to_congress_number,
    _format_url,
    _validate_chamber,
    _validate_congress_number,
    get_records_by_congress_range,
    get_records_by_year,
    get_records_by_year_range,
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


# _format_url -----------------------------------------------------------------
def test__format_url() -> None:
    """Tests that _format_url() passes on three conditions:

    1. A chamber and an integer between 0-9
    2. A chamber and an integer between 10-99
    3. A chamber and an integer between 100-999
    """

    # Case 1
    number = 1
    res = _format_url(number, "Senate")
    assert "S001" in res

    # Case 2
    number = 19
    res = _format_url(number, "Senate")
    assert "S019" in res

    # Case 3
    number = 115
    res = _format_url(number, "Senate")
    assert "S115" in res


# get_records_by_congress_range ------------------------------------------------
def test_get_records_by_congress_range() -> None:
    """Tests get_records_by_congress_range() fails on ill-formatted ranges"""

    start_number = 10
    end_number = 20

    with raises(
        ValueError,
        match=(
            rf"The first number \({end_number}\) must be strictly "
            rf"less than the last number \({start_number}\)."
        ),
    ):
        get_records_by_congress_range(end_number, start_number, "House")


# get_records_by_year ---------------------------------------------------------
def test_get_records_by_year() -> None:
    """Tests properties of the DataFrame from get_records_by_year()"""

    year = 2005
    number = _convert_year_to_congress_number(year)

    record = get_records_by_year(year, "House")

    expected_schema = {
        "congress": Int64,
        "chamber": Utf8,
        "rollnumber": Int32,
        "icpsr": Int32,
        "cast_code": Int32,
        "prob": Float32,
    }

    assert record.schema == expected_schema

    assert "Senate" not in record["chamber"]
    assert record["congress"].min() == number
    assert record["congress"].max() == number


# get_records_by_year_range ----------------------------------------------------
def test_get_records_by_year_range() -> None:
    """Tests properties of the DataFrame from get_records_by_year_range()"""

    start_year = 2010
    start_number = _convert_year_to_congress_number(start_year)
    end_year = 2012
    end_number = _convert_year_to_congress_number(end_year)

    records = get_records_by_year_range(start_year, end_year, "House")

    expected_schema = {
        "congress": Int64,
        "chamber": Utf8,
        "rollnumber": Int32,
        "icpsr": Int32,
        "cast_code": Int32,
        "prob": Float32,
    }

    assert records.schema == expected_schema

    assert "Senate" not in records["chamber"]
    assert records["congress"].min() == start_number
    assert records["congress"].max() == end_number
    assert records["congress"].is_sorted()
