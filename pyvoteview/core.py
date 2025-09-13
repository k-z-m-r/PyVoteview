"""Core functionality of PyVoteview"""

from concurrent.futures import ThreadPoolExecutor
from os import cpu_count
from typing import Literal

from polars import (
    DataFrame,
    concat,
    read_csv,
)

from ._url import _format_url
from ._utilities import (
    _cast_columns,
    _convert_year_to_congress_number,
)
from ._validators import (
    _validate_chamber,
    _validate_congress_number,
)

"""
Sequence of events:

1. User selects a congress congress_number and chamber.
2. Choices are formatted into a URL.
3. URL is loaded by Polars.
4. Data is returned in a meaningful way.

Additional questions:
1. We should figure out how to have readable values for stuff like votes,
political party, etc.
2. Pydantic? Could be a fun helper function.  Messy very quickly, though.
"""


def get_records_by_congress(
    congress_number: int, chamber: Literal["House", "Senate"]
) -> DataFrame:
    """
    Retrieves voting records by congress_number and chamber.

    Args:
        congress_number: Enumeration of which Congress to get.
        chamber: Which chamber of Congress to get.

    Returns:
        Polars DataFrame containing the voting records.
    """

    _validate_congress_number(congress_number)
    _validate_chamber(chamber)

    url_votes = _format_url(congress_number, chamber, "votes")
    url_members = _format_url(congress_number, chamber, "members")
    url_rollcalls = _format_url(congress_number, chamber, "rollcalls")

    record_votes = _cast_columns(read_csv(url_votes, null_values=["N/A"]))
    record_members = _cast_columns(read_csv(url_members, null_values=["N/A"]))
    record_rollcalls = _cast_columns(
        read_csv(url_rollcalls, null_values=["N/A"])
    ).rename({"nominate_log_likelihood": "log_likelihood"})

    return record_votes.join(
        record_members, on=["congress", "chamber", "icpsr"], coalesce=True
    ).join(record_rollcalls, on=["congress", "chamber", "rollnumber"])


def get_records_by_congress_range(
    start_congress_number: int,
    end_congress_number: int,
    chamber: Literal["House", "Senate"],
) -> DataFrame:
    """
    Retrieves voting records by sessions and chamber.

    Args:
        start_congress_number: The start of the congress_number range.
        end_congress_number: The end of the congress_number range.
        chamber: Which chamber of Congress to get.

    Returns:
        Polars DataFrame containing the voting records for that range.
    """

    if start_congress_number >= end_congress_number:
        err = (
            f"The first number ({start_congress_number}) must be strictly "
            f"less than the last number ({end_congress_number})."
        )
        raise ValueError(err)

    records = []
    with ThreadPoolExecutor(
        max_workers=min(32, (cpu_count() or 1) + 4)
    ) as executor:
        records = list(
            executor.map(
                lambda s: get_records_by_congress(s, chamber),
                range(start_congress_number, end_congress_number + 1),
            )
        )

    return concat(records, how="vertical").sort("congress")


def get_records_by_year(
    year: int, chamber: Literal["House", "Senate"]
) -> DataFrame:
    """
    Retrieves voting records by year and chamber.

    Args:
        year: The year that the congress took place.
        chamber: Which chamber of Congress to get.

    Returns:
        Polars DataFrame containing the voting records.
    """

    congress_number = _convert_year_to_congress_number(year)

    return get_records_by_congress(congress_number, chamber)


def get_records_by_year_range(
    start_year: int, end_year: int, chamber: Literal["House", "Senate"]
) -> DataFrame:
    """
    Retrieves voting records by years and chamber.

    Args:
        start_year: The start of the year range.
        end_year: The end of the year range.
        chamber: Which chamber of Congress to get.

    Returns:
        Polars DataFrame containing the voting records for that range.
    """

    start_congress_number = _convert_year_to_congress_number(start_year)
    end_congress_number = _convert_year_to_congress_number(end_year)

    return get_records_by_congress_range(
        start_congress_number, end_congress_number, chamber
    )
