import re
from os import getenv
from dotenv import load_dotenv
from pyrogram import filters

load_dotenv()

# Get this value from my.telegram.org/apps
API_ID = int(getenv("API_ID", "29893020"))
API_HASH = getenv("API_HASH", "28e79037f0b334ef0503466c53f08af5")
# Get your token from @BotFather on Telegram.
TOKEN = getenv("TOKEN", "")
# Get Your bot username
BOT_USERNAME = getenv("BOT_USERNAME", "itsWaifuBot")
# Get your mongo url from cloud.mongodb.com
MONGO_URL = getenv("MONGO_DB_URL", "mongodb+srv://sanasomani786:TJgADfpkI1XVUkKt@cluster0.ruhyad9.mongodb.net/?retryWrites=true&w=majority&appName=AtlasApp")
# Chat id of a group for logging bot's activities
GROUP_ID = int(getenv("GROUP_ID", "-1001423108989"))
CHARA_CHANNEL_ID = int(getenv("CHARA_CHANNEL_ID", "-1002084224770"))
# Get this value from  on Telegram by /id
OWNER_ID = int(getenv("OWNER_ID", 7006524418))
## Fill these variables if you're deploying on heroku.
# Your heroku app name
HEROKU_APP_NAME = getenv("HEROKU_APP_NAME")
# Get it from http://dashboard.heroku.com/account
HEROKU_API_KEY = getenv("HEROKU_API_KEY")

UPSTREAM_REPO = getenv(
    "UPSTREAM_REPO",
    "https://github.com/TheChampu/WaifuCatcher",
)
UPSTREAM_BRANCH = getenv("UPSTREAM_BRANCH", "main")
GIT_TOKEN = getenv(
    "GIT_TOKEN", None
)
UPDATE_CHAT = getenv("UPDATE_CHAT", "ShivanshuHUB")
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "TheChampuClub") 
PHOTO_URL = ["https://telegra.ph/file/7e5398823512d307128a3.jpg", "https://telegra.ph/file/c45dcb207d81e97cb4f6a.jpg", "https://telegra.ph/file/0bc6d65878e8300fbf0f8.jpg", "https://telegra.ph/file/0afb45203ff162ee7227b.jpg"]
# sudo_users
SUDOERS = ["5702648302", "7006524418", "1414327092", "1302298741"]
BANNED_USERS = filters.user()
TEMP_DB_FOLDER = "tempdb"
adminlist = {}
lyrical = {}
votemode = {}
autoclean = []
confirmer = {}
CLEANMODE_DELETE_MINS = int(
    getenv("CLEANMODE_MINS", 5)
)