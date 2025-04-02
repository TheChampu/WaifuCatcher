import logging  
import os
from pyrogram import Client 
from telegram.ext import Application
from motor.motor_asyncio import AsyncIOMotorClient

logging.basicConfig(
    format="%(asctime)s - %(levelname)s - %(name)s - %(message)s",
    handlers=[logging.FileHandler("log.txt"), logging.StreamHandler()],
    level=logging.INFO,
)

logging.getLogger("apscheduler").setLevel(logging.ERROR)
logging.getLogger('httpx').setLevel(logging.WARNING)
logging.getLogger("pyrate_limiter").setLevel(logging.ERROR)
LOGGER = logging.getLogger(__name__)

from Champu.config import Development as Config


API_ID = Config.API_ID
API_HASH = Config.API_HASH
TOKEN = Config.TOKEN
GROUP_ID = Config.GROUP_ID
CHARA_CHANNEL_ID = Config.CHARA_CHANNEL_ID 
MONGO_URL = Config.MONGO_URL 
PHOTO_URL = Config.PHOTO_URL 
SUPPORT_CHAT = Config.SUPPORT_CHAT 
UPDATE_CHAT = Config.UPDATE_CHAT
BOT_USERNAME = Config.BOT_USERNAME 
SUDOERS = Config.SUDOERS
OWNER_ID = Config.OWNER_ID 
JOINLOGS = "-1001423108989"
LEAVELOGS = "-1001977783984"

application = Application.builder().token(TOKEN).build()
Champuu = Client("Champu", API_ID, API_HASH, bot_token=TOKEN)
lol = AsyncIOMotorClient(MONGO_URL)
db = lol['Character_catcher']
set_on_data = db['set_on_data']
refeer_collection = db['refeer_collection']
set_off_data = db['set_off_data']
collection = db['anime_characters_lol']
safari_cooldown_collection = db["safari_cooldown"]
safari_users_collection = db["safari_users_collection"]
SUDOERS_collection= db["SUDOERS_collection"]
user_totals_collection = db['user_totals_lmaoooo']
user_collection = db["user_collection_lmaoooo"]
global_ban_users_collection = db["global_ban_users_collection"]
group_user_totals_collection = db['group_user_totalsssssss']
top_global_groups_collection = db['top_global_groups']
pm_users = db['total_pm_users']
banned_groups_collection = db['Banned_Groups']
BANNED_USERS = db['Banned_Users']
registered_users = db['registered_users']
