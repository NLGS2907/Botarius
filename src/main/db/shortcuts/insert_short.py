"""
INSERT Shorcuts Module.
"""

from ..database import fetch_records_from_table, insert_records_into_table


def register_guild(guild_id: int,
                   guild_name: str) -> None:
    "Registers a guild on the database."

    def_prefix = fetch_records_from_table("botarius_properties",
                                          fetch_one=True,
                                          prop_name="default_prefix")[2]

    insert_records_into_table("guild_prefixes",
                              values=(guild_id, guild_name, def_prefix))
