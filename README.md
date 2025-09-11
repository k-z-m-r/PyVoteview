# PyVoteview

PyVoteview is a Python package for programmatically accessing and analyzing U.S. Congressional voting records from [Voteview](https://voteview.com/). It provides a simple interface to retrieve, filter, and process roll call data for both the House and Senate across sessions and years.

## Features

- Fetch voting records by Congress number or year
- Retrieve data for a range of sessions or years
- Fast, parallelized data loading using Polars and ThreadPoolExecutor


## Installation

PyVoteview requires Python 3.11+ and [Polars](https://pola.rs/):

```sh
pip install pyvoteview
```

## Quick Start

```python
from pyvoteview.core import get_records_by_congress, get_records_by_year

# Get House voting records for the 117th Congress
df = get_records_by_congress(117, "House")

# Get Senate voting records for the year 2020
df = get_records_by_year(2020, "Senate")

# Get records for a range of sessions
df_range = get_records_by_congress_range(115, 117, "House")
```

All functions return a Polars `DataFrame`.

## API Reference

### Fetching Voting Records

| Function | Description | Returns |
|----------|-------------|---------|
| `get_records_by_congress(number: int, chamber: Literal["House", "Senate"])` | Fetch roll call records for a specific Congress and chamber. | Polars `DataFrame` |
| `get_records_by_congress_range(start_congress_number: int, end_congress_number: int, chamber: Literal["House", "Senate"])` | Fetch records for a range of Congress sessions. | Polars `DataFrame` |
| `get_records_by_year(year: int, chamber: Literal["House", "Senate"])` | Fetch records for a specific year. | Polars `DataFrame` |
| `get_records_by_year_range(start_year: int, end_year: int, chamber: Literal["House", "Senate"])` | Fetch records across multiple years. | Polars `DataFrame` |

### Data Processing

| Function | Description | Parameters |
|----------|-------------|------------|
| `rename_columns(record: DataFrame, overwrite_cast_code: bool = True, overwrite_party_code: bool = True)` | Replace numeric codes with descriptive labels for cast and party codes. | `overwrite_cast_code`: overwrite `cast_code` column if True.<br>`overwrite_party_code`: overwrite `party_code` column if True. |

### Mappings

- `CAST_CODES_MAP`: Maps integer roll call codes to human-readable descriptions
  (see [Voteview enumeration](https://voteview.com/articles/data_help_votes)).
- `PARTY_CODES_MAP`: Maps integer party codes to party names (see [Voteview enumeration](https://voteview.com/articles/data_help_parties)).


## License

Licensed under the [Apache License 2.0](LICENSE).
