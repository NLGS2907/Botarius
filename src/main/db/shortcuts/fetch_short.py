"""
FETCH Shortcut Functions Module.
"""

from os import PathLike
from typing import Any, Optional, Tuple

from ..database import fetch_records_from_table


def get_botarius_property(prop_name: str) -> Any:
    "Gets some property out of Botarius."

    return fetch_records_from_table("botarius_properties",
                                    fetch_one=True,
                                    prop_name=prop_name)[2]


def get_bot_id() -> int:
    "Gets Botarius' ID."

    return get_botarius_property("bot_id")


def get_default_prefix() -> str:
    "Gets Botarius' default command prefix."

    return get_botarius_property("default_prefix")


def get_path_from_db(path_name: str) -> PathLike:
    "Retrieves a path from the database."

    res = fetch_records_from_table("paths",
                                   fetch_one=True,
                                   path_name=path_name)

    # The path will always be the third column
    return res[2]


def get_paths_from_db(path_name: str) -> Tuple[PathLike, ...]:
    "Retrieves many paths from the database."

    res = fetch_records_from_table("paths",
                                   fetch_one=False,
                                   path_name=path_name)

    # The paths will always be the third column
    return tuple(col[2] for col in res)


def get_log_path() -> PathLike:
    "Gets the log path."

    return get_path_from_db("log_path")


def get_cogs_path() -> PathLike:
    "Gets the cogs path."

    return get_path_from_db("cogs_path")


def get_guild_prefix(guild_id: Optional[int]=None,
                     guild_name: Optional[str]=None) -> str:
    "Retrieves a guild prefix by id or name."

    if guild_id is None and guild_name is None:
        raise ValueError("Both guild id and name cannot be none. Must set at least one of them.")

    attributes = {}

    if guild_id is not None:
        attributes.update(guild_id=guild_id)

    if guild_name is not None:
        attributes.update(guild_name=guild_name)

    res = fetch_records_from_table("guild_prefixes",
                                   fetch_one=True,
                                   **attributes)

    if not res:
        return get_default_prefix()

    return res[3]


def get_botarius_version() -> str:
    "Gets Botarius' version in the vX.X.X format."

    res = fetch_records_from_table("versions",
                                   fetch_one=True,
                                   program_name="botarius")
    dev_state = (f"-{res[-1]}" if res[-1] else res[-1])
    return f"{'.'.join([str(v) for v in res[2:-1]])}{dev_state}"