"""Tests URL functionality of PyVoteview."""

from pytest import raises

from pyvoteview._url import (
    _format_url,
)


# _format_url -----------------------------------------------------------------
def test__format_url() -> None:
    """Tests that _format_url() passes on the conditions:

    1. A chamber and an integer between 0-9
    2. A chamber and an integer between 10-99
    3. A chamber and an integer between 100-999
    4. Passing an unsupported category raises a ValueError.
    """

    # Case 1
    number = 1
    res = _format_url(number, "Senate", "votes")
    assert "S001" in res

    # Case 2
    number = 19
    res = _format_url(number, "Senate", "votes")
    assert "S019" in res

    # Case 3
    number = 115
    res = _format_url(number, "Senate", "votes")
    assert "S115" in res

    # Case 3
    with raises(
        ValueError,
        match="parties was selected, but is not one of: votes, members",
    ):
        _format_url(0, "", "parties")  # type: ignore
