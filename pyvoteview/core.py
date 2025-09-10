"""Core functionality of PyVoteview"""

from datetime import UTC, datetime
from math import floor
from typing import Literal

from polars import DataFrame

"""
Sequence of events:

1. User selects a congress session and chamber.
2. Choices are formatted into a URL.
3. URL is loaded by Polars.
4. Data is returned in a meaningful way.

Additional questions:
1. We should figure out how to have readable values for stuff like votes,
political party, etc.
2. Pydantic? Could be a fun helper function.  Messy very quickly, though.
"""

START_OF_CONGRESS = 1789
CURRENT_YEAR = datetime.now(tz=UTC).year


def _validate_year(year: int) -> None:
    """
    Validate that a year is valid from the lens of Congress (1789-Now).

    Args:
        year: Year to validate.
    """

    if year > CURRENT_YEAR:
        err = "The year cannot be in the future."
        raise ValueError(err)
    if year < START_OF_CONGRESS:
        err = "The year cannot be before the U.S. Congress existed."
        raise ValueError(err)


def _convert_year_to_session(year: int) -> int:
    """
    Converts a year to the corresponding U.S. Congress session.

    Args:
        year: The year to convert.

    Returns:
        The corresponding session.  Assumes the January which comes at the tail
        end of a session is actually part of the next session.
    """

    _validate_year(year)

    return floor((year - START_OF_CONGRESS) / 2) + 1


MINIMUM_SESSION = 1
CURRENT_SESSION = _convert_year_to_session(CURRENT_YEAR)


def _validate_session(session: int) -> None:
    """
    Validate that a session is valid for a Congress.

    Args:
        session: Session to validate.
    """

    if session > CURRENT_SESSION:
        err = "This session hasn't happened yet."
        raise ValueError(err)
    if session < MINIMUM_SESSION:
        err = (
            f"This session cannot occur, as Congress begins"
            f"at session {MINIMUM_SESSION}"
        )
        raise ValueError(err)


def get_voting_records_by_session(
    session: int, chamber: Literal["House", "Senate"]
) -> DataFrame:
    """
    Retrieves voting records by session and chamber.

    Args:
        session: Enumeration of which Congress to get.
        chamber: Which chamber of Congress to get.

    Returns:
        Polars DataFrame containing the voting records.
    """

    del session, chamber
    return DataFrame()


def get_voting_records_by_sessions(
    start_session: int, end_session: int, chamber: Literal["House", "Senate"]
) -> DataFrame:
    """
    Retrieves voting records by sessions and chamber.

    Args:
        start_session: The start of the session range.
        end_session: The end of the session range.
        chamber: Which chamber of Congress to get.

    Returns:
        Polars DataFrame containing the voting records for that range.
    """

    _validate_session(start_session)
    _validate_session(end_session)

    records = DataFrame()
    for session in range(start_session, end_session + 1):
        record = get_voting_records_by_session(session, chamber)
        records.join(record)

    return records


def get_voting_records_by_year(
    year: int, chamber: Literal["House", "Senate"]
) -> DataFrame:
    """
    Retrieves voting records by year and chamber.

    Args:
        year: The year that the session took place.
        chamber: Which chamber of Congress to get.

    Returns:
        Polars DataFrame containing the voting records.
    """

    session = _convert_year_to_session(year)

    return get_voting_records_by_session(session, chamber)


def get_voting_records_by_years(
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

    start_session = _convert_year_to_session(start_year)
    end_session = _convert_year_to_session(end_year)

    return get_voting_records_by_sessions(start_session, end_session, chamber)
