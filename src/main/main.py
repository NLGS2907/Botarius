#pylint: disable=line-too-long
"""
Main Module.

-=-=-=-

Permissions:

- General Permissions

    Change Nickname
    Read Messages/View Channels

- Text Permissions

    Send Messages
    Create Public Threads
    Create Private Threads
    Send Messages in Threads
    Send TTS Messages
    Manage Messages
    Embed Links
    Attach Files
    Read Message History
    Mention Everyone
    Use External Emojis
    Use External Stickers
    Add Reactions
    Use Slash Commands

- Voice Permissions

    Connect
    Speak
    Mute Members
    Deafen Members
    Move Members
    Use Voice Activity

-=-=-=-

Permissions Integer: 534857120832

-=-=-=-

Bot Invite link: https://discord.com/api/oauth2/authorize?client_id=971819308810379295&permissions=534857120832&scope=bot%20applications.commands
Repository: https://github.com/NLGS2907/Botarius
"""

from os import getenv

from dotenv import load_dotenv

from .auxiliar import bot_args_parser
from .botarius import Botarius

load_dotenv()

def main(*_args, **_kwargs) -> int:
    "Main Function."

    bot_args_parser().parse_args()
    Botarius().run(getenv("DISCORD_TOKEN"))
    return 0


if __name__ == "__main__":
    main()
