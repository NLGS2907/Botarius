"""
Constants Module.
"""

from os import getenv

from dotenv import load_dotenv

load_dotenv()


BOT_TOKEN = getenv("DISCORD_TOKEN")
"Botarius' token, so it can login."

BOT_ID = 971819308810379295
"Botarius' specific id."

BOT_VERSION = "0.0.1"
"Botarius' current development version."

DEFAULT_PREFIX = '>'
"If needed, the default command prefix."

LOG_PATH = "botarius.log"
"Botarius' log file path."

PROPERTIES_PATH = "src/main/json/properties.json"

COGS_PATH = "src/main/cogs"
