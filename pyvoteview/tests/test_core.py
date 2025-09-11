"""Tests core functionality of PyVoteview."""

from pytest import raises

from pyvoteview._utilities import (
    _VOTEVIEW_DATAFRAME_SCHEMA,
    _convert_year_to_congress_number,
)
from pyvoteview.core import (
    get_records_by_congress_range,
    get_records_by_year,
    get_records_by_year_range,
)


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

    assert record.schema == _VOTEVIEW_DATAFRAME_SCHEMA

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

    assert records.schema == _VOTEVIEW_DATAFRAME_SCHEMA

    assert "Senate" not in records["chamber"]
    assert records["congress"].min() == start_number
    assert records["congress"].max() == end_number
    assert records["congress"].is_sorted()
