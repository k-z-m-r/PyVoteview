"""Test utilities of PyVoteview"""

from pyvoteview._utilities import rename_columns
from pyvoteview.core import get_records_by_congress


# rename_columns ---------------------------------------------------------
def test_rename_columns() -> None:
    """Tests properties of the DataFrame from rename_columns():

    1. Rename with overwriting both cast_code and party_code
    2. Rename without overwriting either
    3. Rename with overwrite for only cast_code
    4. Rename with overwrite for only party_code
    """

    record = get_records_by_congress(100, "Senate")

    # Case 1
    rewritten_record = rename_columns(
        record.clone(), overwrite_cast_code=True, overwrite_party_code=True
    )
    cols = rewritten_record.columns

    assert "cast_code" in cols
    assert "party_code" in cols
    assert "cast_code_str" not in cols
    assert "party_code_str" not in cols

    # Case 2
    rewritten_record = rename_columns(
        record.clone(), overwrite_cast_code=False, overwrite_party_code=False
    )
    cols = rewritten_record.columns

    assert "cast_code" in cols
    assert "party_code" in cols
    assert "cast_code_str" in cols
    assert "party_code_str" in cols
    assert cols[cols.index("cast_code") + 1] == "cast_code_str"
    assert cols[cols.index("party_code") + 1] == "party_code_str"

    # Case 3
    rewritten_record = rename_columns(
        record.clone(), overwrite_cast_code=True, overwrite_party_code=False
    )
    cols = rewritten_record.columns

    assert "cast_code" in cols
    assert "party_code" in cols
    assert "cast_code_str" not in cols
    assert "party_code_str" in cols
    assert cols[cols.index("party_code") + 1] == "party_code_str"

    # Case 4
    rewritten_record = rename_columns(
        record.clone(), overwrite_cast_code=False, overwrite_party_code=True
    )
    cols = rewritten_record.columns

    assert "cast_code" in cols
    assert "party_code" in cols
    assert "cast_code_str" in cols
    assert "party_code_str" not in cols
    assert cols[cols.index("cast_code") + 1] == "cast_code_str"
