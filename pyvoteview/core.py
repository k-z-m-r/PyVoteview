"""Core functionality of PyVoteview"""

from datetime import UTC, datetime
from math import floor
from typing import Literal

from polars import DataFrame, read_csv

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


def _convert_year_to_session(year: int) -> int:
    """
    Converts a year to the corresponding U.S. Congress session.

    Args:
        year: The year to convert.

    Returns:
        The corresponding session.  Assumes the January which comes at the tail
        end of a session is actually part of the next session.
    """

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
        err = (
            "This session would occur after "
            f"{CURRENT_SESSION} ({CURRENT_YEAR})."
        )
        raise ValueError(err)
    if session < MINIMUM_SESSION:
        err = (
            f"This session cannot occur, as Congress begins "
            f"at session {MINIMUM_SESSION} ({START_OF_CONGRESS})"
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


def _format_url(session: int, chamber: Literal["House", "Senate"]) -> str:
    """
    Formats URL to be consistent with Voteview expectation.

    Args:
        session: The session of Congress.
        chamber: The chamber of Congress.

    Returns:
        URL formatted as:
        https://voteview.com/static/data/out/votes/{Chamber}{Session}_votes.csv
    """

    return (
        "https://voteview.com/static/data/out/votes/"
        f"{chamber[0]}{str(session).zfill(3)}_votes.csv"
    )


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

    _validate_session(session)
    _validate_chamber(chamber)

    url = _format_url(session, chamber)

    return read_csv(url)


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

    if start_session >= end_session:
        err = (
            f"The first session ({start_session}) must be strictly "
            f"less than the last session ({end_session})."
        )
        raise ValueError(err)

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
