"""Core functionality of PyVoteview"""

from typing import Literal

from polars import DataFrame

"""
Sequence of events:

1. User selects a congress session and chamber.
2. Choices are formatted into a URL.
3. URL is loaded by Polars.
4. Data is returned in a meaningful way.

Additional questions:
1. What if they want a range of sessions (114-115)?
2. What if they want a range of years (2004-2007)?
3. We should figure out how to have readable values for stuff like votes,
political party, etc.
"""


def get_voting_records(
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


def get_voting_records_by_year(
    year: int, chamber: Literal["House", "Senate"]
) -> DataFrame:
    """
    Retrieves voting records by year and chamber.

    Args:
        year: The year that the session took place.  Counts the end of one
            session from January onwards as part of the subsequent session.
        chamber: Which chamber of Congress to get.

    Returns:
        Polars DataFrame containing the voting records.
    """

    del year, chamber
    return DataFrame()
