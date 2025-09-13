"""Tests core functionality of PyVoteview."""

from pytest import raises

from pyvoteview._utilities import (
    _VOTEVIEW_DATAFRAME_SCHEMA,
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

    record = get_records_by_year(year, "House")

    assert record.schema == _VOTEVIEW_DATAFRAME_SCHEMA

    assert "Senate" not in record["chamber"]
    assert record["date"].min().year == year  # type: ignore
    assert record["date"].max().year == year  # type: ignore


# get_records_by_year_range ----------------------------------------------------
def test_get_records_by_year_range() -> None:
    """Tests properties of the DataFrame from get_records_by_year_range()"""

    start_year = 2010
    end_year = 2012

    records = get_records_by_year_range(start_year, end_year, "House")

    assert records.schema == _VOTEVIEW_DATAFRAME_SCHEMA

    assert "Senate" not in records["chamber"]
    assert records["date"].min().year == start_year  # type: ignore
    assert records["date"].max().year == end_year  # type: ignore
    assert records["congress"].is_sorted()
