"""Tests core functionality of PyVoteview."""

from pytest import raises

from pyvoteview.core import CURRENT_SESSION, CURRENT_YEAR, _validate_session

# _validate_session ------------------------------------------------------------


def test__validate_session() -> None:
    """Tests that _validate_session works on three cases:

    1. No exception
    2. Raises exception when session < 1
    3. Raises exception when session > current session
    """

    # Case 1
    _validate_session(100)

    # Case 2
    with raises(
        ValueError,
        match=(
            "This session cannot occur, "
            r"as Congress begins at session 1 \(1789\)"
        ),
    ):
        _validate_session(0)

    # Case 3
    with raises(
        ValueError,
        match="This session would occur after "
        rf"{CURRENT_SESSION} \({CURRENT_YEAR}\).",
    ):
        _validate_session(CURRENT_SESSION + 1)
