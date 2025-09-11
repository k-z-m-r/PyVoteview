"""Utility functions"""

from math import floor

from polars import DataFrame, DataType, Float32, Int32, Utf8, col

VOTEVIEW_SCHEMA: dict[str, type[DataType]] = {
    "congress": Int32,
    "chamber": Utf8,
    "rollnumber": Int32,
    "icpsr": Int32,
    "cast_code": Int32,
    "prob": Float32,
    "state_icpsr": Int32,
    "district_code": Int32,
    "state_abbrev": Utf8,
    "party_code": Int32,
    "occupancy": Int32,
    "last_means": Int32,
    "bioname": Utf8,
    "bioguide_id": Utf8,
    "born": Int32,
    "died": Float32,
    "nominate_dim1": Float32,
    "nominate_dim2": Float32,
    "nominate_log_likelihood": Float32,
    "nominate_geo_mean_probability": Float32,
    "nominate_number_of_votes": Int32,
    "nominate_number_of_errors": Int32,
    "conditional": Utf8,
    "nokken_poole_dim1": Float32,
    "nokken_poole_dim2": Float32,
}

CAST_CODES_MAP: dict[int, str] = {
    0: "Not a member of the chamber when this vote was taken",
    1: "Yea",
    2: "Paired Yea",
    3: "Announced Yea",
    4: "Announced Nay",
    5: "Paired Nay",
    6: "Nay",
    7: "Present (some Congresses)",
    8: "Present (some Congresses)",
    9: "Not Voting (Abstention)",
}


def _convert_year_to_congress_number(year: int) -> int:
    """
    Converts a year to the corresponding U.S. Congress number.

    Args:
        year: The year to convert.

    Returns:
        The corresponding Congress number.  Assumes the January which comes at
        the tail end of a Congress is actually part of the next Congress.
    """

    return floor((year - 1789) / 2) + 1


def _cast_columns(record: DataFrame) -> DataFrame:
    """
    Casts columns in a DataFrame to specified types.

    Args:
        record: The Polars DataFrame.
        schema: Dict of column names to Polars types.

    Returns:
        DataFrame with columns cast to specified types.
    """
    return record.with_columns(
        [
            record[name].cast(VOTEVIEW_SCHEMA[name], strict=False)
            for name in record.columns
            if name in VOTEVIEW_SCHEMA
        ]
    )


def remap_record(record: DataFrame, overwrite: bool = True) -> DataFrame:
    """
    Replaces cast codes in the DataFrame with their description.

    Args:
        record: The DataFrame to modify in-place.
        overwrite: Whether or not to replace the existing column.  Defaults to
            True, so cast_code gets replaced with strings.

    Returns:
        The original DataFrame modified so that cast codes are their
        descriptions.
    """

    alias = "cast_code" if overwrite is True else "cast_code_str"
    return record.with_columns(
        col("cast_code")
        .map_elements(lambda x: CAST_CODES_MAP.get(x), return_dtype=Utf8)
        .alias(alias)
    )
