"""URL-based functions"""

from typing import Literal

from ._validators import _validate_category


def _format_url(
    congress_number: int,
    chamber: Literal["House", "Senate"],
    category: Literal["members", "rollcalls", "votes"],
) -> str:
    """
    Formats URL to be consistent with Voteview expectation.

    Args:
        congress_number: The number of Congress.
        chamber: The chamber of Congress.

    Returns:
        URL formatted as:
        voteview.com/static/data/out/{Category}/{Chamber}{Number}{Category}.csv
    """

    _validate_category(category)

    return (
        f"https://voteview.com/static/data/out/{category}/"
        f"{chamber[0]}{congress_number:03}_{category}.csv"
    )
