# Copyright (C) @TheSmartBisnu
# Channel: https://t.me/itsSmartDev

from os import getenv
from time import time
from dotenv import load_dotenv

try:
    load_dotenv("config.env.local")
    load_dotenv("config.env")
except:
    pass

    if not getenv("BOT_TOKEN") or not getenv("BOT_TOKEN").count(":") == 1:
        print("Error: BOT_TOKEN must be in format '8031981205:AAGz3oAzc7hvRHViOirPutAJeiP3t4lvu40'")
        exit(1)

    if (
        not getenv("SESSION_STRING")
        or getenv("SESSION_STRING") == "BQHGXjoABmMxqKLfb7AU86vPtLbNIBGttHEjSDCoV87Ph_UM_WRZ9ZdIxVcN0i4-6CckEo3qSXw7WRa_Zgj-OZjTVWtRtwFEpAmsvbhUHnQzv7u32dpENOs5DTR0mREjfdlPkcgbrQgLv6-BGcTiDgdmTriyYoigC-_gFcNaqYFkBcrtToBAjaf0XJDXgrxGXoeLAYk3PvgiGYw8HTH117tQ0jPpA7P63HTDNbopuL-CjyXlr-nURojIjAJiSGZofqqdRSlIpxg5knjTFE2ejorLsHitaBO7veaijkGg06yN-Yu7mrwX98ZyBfBq62rKK-wXQ5tR20ISEYcc8Qn07RuXGx6oowAAAAA1FSa2AA"
    ):
        print("Error: SESSION_STRING must be set with a valid string")
        exit(1)


# Pyrogram setup
class PyroConf(object):
    API_ID = int(getenv("API_ID", "29777466"))
    API_HASH = getenv("API_HASH", "a04b3df726520026f207079aec2f9879")
    BOT_TOKEN = getenv("BOT_TOKEN")
    SESSION_STRING = getenv("SESSION_STRING")
    BOT_START_TIME = time()

    MAX_CONCURRENT_DOWNLOADS = int(getenv("MAX_CONCURRENT_DOWNLOADS", "999991"))
    BATCH_SIZE = int(getenv("BATCH_SIZE", "999991"))
    FLOOD_WAIT_DELAY = int(getenv("FLOOD_WAIT_DELAY", "100"))
