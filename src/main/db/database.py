"""
Database functions Module.
"""

from os import PathLike
from sqlite3 import connect
from typing import Any, Dict, Literal, Optional, Tuple, TypeAlias

CondsDict: TypeAlias = Dict[str, Any]
ResolutionValues: TypeAlias = Literal["ABORT", "FAIL", "IGNORE", "REPLACE", "ROLLBACK"]

DEFAULT_DB: PathLike = "src/main/db/db.sqlite3"
RESOLUTIONS: Tuple[str, ...] = "ABORT", "FAIL", "IGNORE", "REPLACE", "IGNORE"


def create_new_db(db_path: PathLike[str]="") -> None:
    """
    Creates a new db from a pre-defined template.
    This will NOT be the database botarius uses unless
    it is the DEFAULT_DB path.
    """

    db_path = db_path or DEFAULT_DB

    with connect(db_path) as con:
        cur = con.cursor()
        cur.executescript("""
        CREATE TABLE botarius_properties (
            prop_id INTEGER PRIMARY KEY,
            prop_name TEXT,
            prop_value TEXT
        ) STRICT;

        CREATE TABLE guild_prefixes (
            id INTEGER PRIMARY KEY,
            guild_id INTEGER,
            guild_name TEXT,
            prefix TEXT
        ) STRICT;

        CREATE TABLE paths (
            path_id INTEGER PRIMARY KEY,
            path_name TEXT,
            fpath TEXT
        ) STRICT;

        CREATE TABLE versions (
            program_id INTEGER PRIMARY KEY,
            program_name TEXT,
            major_version INTEGER,
            major_patch INTEGER,
            minor_patch INTEGER,
            dev_state TEXT
        ) STRICT;
        """)


def _where_conditions(**conditions: CondsDict) -> str:
    "Creates a SQL expresion with all the conditions in the kwargs."

    extra = None

    try:
        extra = conditions.pop("where")
        if not isinstance(extra, tuple):
            raise TypeError("extra conditions from 'where' parameter must be a tuple of strings.")
    except KeyError:
        extra = tuple()

    conds = " AND ".join([f"{k}={v!r}" for k, v in conditions.items()] + list(extra))
    return ('' if not conds else f" WHERE {conds}")


def _resolution_protocol(resolution: Optional[ResolutionValues]=None) -> str:
    "Parses an option to define a protocol in case some operation fails."

    if resolution is None:
        res_protocol = ''
    elif resolution.upper() not in RESOLUTIONS:
        raise ValueError(f"Resolution type must be one of {RESOLUTIONS}")
    else:
        res_protocol = f" OR {resolution} "

    return res_protocol


def fetch_records_from_table(table: str,
                             fetch_one: bool=False,
                             **conditions: CondsDict) -> Any:
    "Retrieves records from a table of the database."

    res = None
    conds = _where_conditions(**conditions)

    with connect(DEFAULT_DB) as con:
        cur = con.cursor()
        cur.execute(f"SELECT * FROM {table}{conds};")
        res = (cur.fetchone() if fetch_one else cur.fetchall())

    return res


def delete_records_from_table(table: str,
                              **conditions: CondsDict) -> None:
    """
    Deletes records from the database.

    * It does NOT support a LIMIT option.
    """

    conds = _where_conditions(**conditions)

    with connect(DEFAULT_DB) as con:
        cur = con.cursor()
        cur.execute(f"DELETE FROM {table}{conds};")


def insert_records_into_table(table: str,
                              resolution: Optional[ResolutionValues]=None,
                              *,
                              values=Tuple[Any, ...]) -> None:
    "Tries to insert a record into a table."

    res_protocol = _resolution_protocol(resolution)
    wrapped_values = [f"{v!r}" for v in values]
    final_values = f"(?, {', '.join(wrapped_values)})" # Must add placeholder first because of rowid

    with connect(DEFAULT_DB) as con:
        cur = con.cursor()
        cur.executescript(f"INSERT{res_protocol} INTO {table} VALUES{final_values};")


def update_records_of_table(table: str,
                            resolution: Optional[ResolutionValues]=None,
                            *,
                            set_values: Tuple[str, ...],
                            **conditions: CondsDict) -> None:
    "Updates some records already in tables."

    if not isinstance(set_values, tuple):
        raise TypeError("SET values must me a tuple of strings.")

    conds = _where_conditions(**conditions)
    res_protocol = _resolution_protocol(resolution)

    with connect(DEFAULT_DB) as con:
        cur = con.cursor()
        cur.execute(f"UPDATE{res_protocol} {table} SET {', '.join(set_values)} {conds};")
