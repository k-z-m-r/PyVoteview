"""Utility functions"""

from math import floor
from typing import Literal

from polars import DataFrame, DataType, Date, Float32, Int32, Utf8, col

_VOTEVIEW_DATAFRAME_SCHEMA: dict[str, type[DataType]] = {
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
    "born": Date,
    "died": Date,
    "nominate_dim1": Float32,
    "nominate_dim2": Float32,
    "nominate_log_likelihood": Float32,
    "nominate_geo_mean_probability": Float32,
    "nominate_number_of_votes": Int32,
    "nominate_number_of_errors": Int32,
    "conditional": Utf8,
    "nokken_poole_dim1": Float32,
    "nokken_poole_dim2": Float32,
    "date": Date,
    "session": Utf8,
    "clerk_rollnumber": Utf8,
    "yea_count": Int32,
    "nay_count": Int32,
    "nominate_mid_1": Float32,
    "nominate_mid_2": Float32,
    "nominate_spread_1": Float32,
    "nominate_spread_2": Float32,
    "log_likelihood": Float32,
    "bill_number": Utf8,
    "vote_result": Utf8,
    "vote_desc": Utf8,
    "vote_question": Utf8,
    "dtl_desc": Utf8,
}

CAST_CODE_MAP: dict[int, str] = {
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

PARTY_CODE_MAP = {
    1: "Federalist Party",
    13: "Democratic-Republican Party",
    22: "Adams Party",
    26: "Anti Masonic Party",
    29: "Whig Party",
    37: "Constitutional Unionist Party",
    44: "Nullifier Party",
    46: "States Rights Party",
    100: "Democratic Party",
    108: "Anti-Lecompton Democrats",
    112: "Conservative Party",
    114: "Readjuster Party",
    117: "Readjuster Democrats",
    200: "Republican Party",
    203: "Unconditional Unionist Party",
    206: "Unionist Party",
    208: "Liberal Republican Party",
    213: "Progressive Republican Party",
    300: "Free Soil Party",
    310: "American Party",
    326: "National Greenbacker Party",
    328: "Independent",
    329: "Independent Democrat",
    331: "Independent Republican",
    340: "Populist PARTY",
    347: "Prohibitionist Party",
    354: "Silver Republican Party",
    355: "Union Labor Party",
    356: "Union Labor Party",
    370: "Progressive Party",
    380: "Socialist Party",
    402: "Liberal Party",
    403: "Law and Order Party",
    522: "American Labor Party",
    523: "American Labor Party (La Guardia)",
    537: "Farmer-Labor Party",
    555: "Jackson Party",
    603: "Independent Whig",
    1060: "Silver Party",
    1111: "Liberty Party",
    1116: "Conservative Republicans",
    1275: "Anti-Jacksonians",
    1346: "Jackson Republican",
    3333: "Opposition Party",
    3334: "Opposition Party (36th)",
    4000: "Anti-Administration Party",
    4444: "Constitutional Unionist Party",
    5000: "Pro-Administration Party",
    6000: "Crawford Federalist Party",
    7000: "Jackson Federalist Party",
    7777: "Crawford Republican Party",
    8000: "Adams-Clay Federalist Party",
    8888: "Adams-Clay Republican Party",
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
            record[name].cast(_VOTEVIEW_DATAFRAME_SCHEMA[name], strict=False)
            for name in record.columns
            if name in _VOTEVIEW_DATAFRAME_SCHEMA
        ]
    )


def rename_columns(
    record: DataFrame,
    overwrite_cast_code: bool = True,
    overwrite_party_code: bool = True,
) -> DataFrame:
    """
    Replaces cast codes in the DataFrame with their description.

    Args:
        record: The DataFrame to modify in-place.
        overwrite_cast_code: Whether or not to replace the existing column for
            cast code. Defaults to True.
        overwrite_party_code: Whether or not to replace the existing column for
            party code. Defaults to True.

    Returns:
        The original DataFrame modified so that cast codes are their
        descriptions.
    """

    def reorder_columns(
        df: DataFrame,
        column_name: Literal["cast_code", "party_code"],
    ) -> DataFrame:
        """Helper to reorder the columns so {x}_str is to the right of {x}."""
        cols = df.columns
        cols.remove(
            f"{column_name}_str",
        )
        order = [
            *cols[: cols.index(column_name) + 1],
            f"{column_name}_str",
            *cols[cols.index(column_name) + 1 :],
        ]
        return df.select(order)

    cast_code_alias = (
        "cast_code" if overwrite_cast_code is True else "cast_code_str"
    )
    party_code_alias = (
        "party_code" if overwrite_party_code is True else "party_code_str"
    )

    record = record.with_columns(
        col("cast_code")
        .map_elements(lambda x: CAST_CODE_MAP.get(x), return_dtype=Utf8)
        .alias(cast_code_alias),
        col("party_code")
        .map_elements(lambda x: PARTY_CODE_MAP.get(x), return_dtype=Utf8)
        .alias(party_code_alias),
    )

    if overwrite_cast_code is False:
        record = reorder_columns(record, "cast_code")
    if overwrite_party_code is False:
        record = reorder_columns(record, "party_code")

    return record
