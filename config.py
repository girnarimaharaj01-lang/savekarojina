# Copyright (c) 2025 devgagan : https://github.com/devgaganin.  
# Licensed under the GNU General Public License v3.0.  
# See LICENSE file in the repository root for full license text.

import os
from dotenv import load_dotenv

load_dotenv()

# VPS --- FILL COOKIES 🍪 in """ ... """ 

INST_COOKIES = """
# wtite up here insta cookies
"""

YTUB_COOKIES = """
# write here yt cookies
"""

API_ID = os.getenv("API_ID", "29777466")
API_HASH = os.getenv("API_HASH", "a04b3df726520026f207079aec2f9879")
BOT_TOKEN = os.getenv("BOT_TOKEN", "8158405668:AAHJYP5Bc8OQl7-0IXPSx8RPppty16wjLdQ")
MONGO_DB = os.getenv("MONGO_DB", "mongodb+srv://girnarimaharaj01_db_user:KsxBY4eoUBwRKXXw@cluster0.6firafk.mongodb.net/?appName=Cluster0")
OWNER_ID = list(map(int, os.getenv("OWNER_ID", "8399557684").split())) # list seperated via space
DB_NAME = os.getenv("DB_NAME", "girnarimaharaj01_db_user")
STRING = os.getenv("STRING", None) # optional
LOG_GROUP = int(os.getenv("LOG_GROUP", "-1003164986113")) # optional with -100
FORCE_SUB = int(os.getenv("FORCE_SUB", "-1003164986113")) # optional with -100
MASTER_KEY = os.getenv("MASTER_KEY", "gK8HzLfT9QpViJcYeB5wRa3DmN7P2xUq") # for session encryption
IV_KEY = os.getenv("IV_KEY", "s7Yx5CpVmE3F") # for decryption
YT_COOKIES = os.getenv("YT_COOKIES", YTUB_COOKIES)
INSTA_COOKIES = os.getenv("INSTA_COOKIES", INST_COOKIES)
FREEMIUM_LIMIT = int(os.getenv("FREEMIUM_LIMIT", "0"))
PREMIUM_LIMIT = int(os.getenv("PREMIUM_LIMIT", "500"))
JOIN_LINK = os.getenv("JOIN_LINK", "https://t.me/Nikhilbhaiiibot") # this link for start command message
ADMIN_CONTACT = os.getenv("ADMIN_CONTACT", "https://t.me/Nikhilbhaiiibot")







