import os
import logging
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from motor.motor_asyncio import AsyncIOMotorClient as MongoClient
def LOGGER(name: str) -> logging.Logger:
    return logging.getLogger(name)
# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[logging.FileHandler("bot.log"), logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

from Champu import API_ID, API_HASH, TOKEN as BOT_TOKEN, MONGO_URL as MONGO_DB_URI, OWNER_ID, BANNED_USERS
from motor.motor_asyncio import AsyncIOMotorClient as _mongo_client_
from pymongo import MongoClient
from pyrogram import Client

import Champu as config

TEMP_MONGODB = "mongodb+srv://yash:shivanshudeo@yk.6bvcjqp.mongodb.net/?retryWrites=true&w=majority&appName=yk"


if config.MONGO_DB_URI is None:
    LOGGER(__name__).warning(
        "ɴᴏ ᴍᴏɴɢᴏ  ᴅʙ ᴜʀʟ ғᴏᴜɴᴅ.. sᴏ ɪ ᴡɪʟʟ ᴜsᴇ ᴍʏ ᴏᴡɴᴇʀ's ᴍᴏɴɢᴏ ᴅʙ ᴜʀʟ"
    )
    temp_client = Client(
        "ChampuMusic",
        bot_token=config.BOT_TOKEN,
        api_id=config.API_ID,
        api_hash=config.API_HASH,
    )
    temp_client.start()
    info = temp_client.get_me()
    username = info.username
    temp_client.stop()
    _mongo_async_ = _mongo_client_(TEMP_MONGODB)
    _mongo_sync_ = MongoClient(TEMP_MONGODB)
    mongodb = _mongo_async_[username]
    pymongodb = _mongo_sync_[username]
else:
    _mongo_async_ = _mongo_client_(config.MONGO_DB_URI)
    _mongo_sync_ = MongoClient(config.MONGO_DB_URI)
    mongodb = _mongo_async_.Champu
    pymongodb = _mongo_sync_.Champu
from Sanatan import sudo_users_collection, app
SUDOERS = filters.user()
def sudo():
    global SUDOERS
    OWNER = config.OWNER_ID
    if config.MONGO_DB_URI is None:
        for user_id in OWNER:
            SUDOERS.add(user_id)
    else:
        sudoersdb = pymongodb.sudoers
        sudoers = sudoersdb.find_one({"sudo": "sudo"})
        sudoers = [] if not sudoers else sudoers["sudoers"]
        for user_id in OWNER:
            SUDOERS.add(user_id)
            if user_id not in sudoers:
                sudoers.append(user_id)
                sudoersdb.update_one(
                    {"sudo": "sudo"},
                    {"$set": {"sudoers": sudoers}},
                    upsert=True,
                )
        if sudoers:
            for x in sudoers:
                SUDOERS.add(x)
    LOGGER(__name__).info(f"Sudoers Loaded.")

# Load sudo users from the database
async def load_sudoers():
    global SUDOERS
    sudoers = await sudo_users_collection.find_one({"sudo": "sudo"})
    if sudoers:
        SUDOERS = set(sudoers.get("sudoers", []))
    SUDOERS.add(OWNER_ID)  # Add owner as a sudo user by default
    logger.info("Sudoers loaded.")

# Add a user to sudo
async def add_sudo(user_id: int) -> bool:
    SUDOERS.add(user_id)
    await sudo_users_collection.update_one(
        {"sudo": "sudo"},
        {"$addToSet": {"sudoers": user_id}},
        upsert=True
    )
    return True

async def remove_sudo(user_id: int) -> bool:
    if user_id in SUDOERS:
        # First remove the user from the in-memory list
        SUDOERS.remove(user_id)

        # Then update MongoDB
        result = await sudo_users_collection.update_one(
            {"sudo": "sudo"},
            {"$pull": {"sudoers": user_id}}
        )
        
        logger.info(f"MongoDB update result: {result.modified_count}")
        
        # If MongoDB update was successful (modified_count > 0), return True
        if result.modified_count > 0:
            return True
    return False




# Extract user from a message
async def extract_user(message: Message):
    if message.reply_to_message:
        return message.reply_to_message.from_user
    elif len(message.command) > 1:
        try:
            return await app.get_users(message.command[1])
        except Exception as e:
            logger.error(f"Error extracting user: {e}")
            return None
    return None

# Maintenance mode
maintenance = []

async def is_maintenance():
    if not maintenance:
        get = await sudo_users_collection.find_one({"on_off": 1})
        if get is None:
            maintenance.append(2)  # Maintenance mode active
            return True
        else:
            maintenance.append(1)  # Maintenance mode inactive
            return False
    else:
        return maintenance[0] == 2  # Return True if maintenance mode is active

# Language decorator (placeholder)
def language(func):
    async def wrapper(client, message, **kwargs):
        # Allow the owner to bypass maintenance mode
        if await is_maintenance() and message.from_user.id not in SUDOERS and message.from_user.id != OWNER_ID:
            return await message.reply_text("Bot is under maintenance. Please try again later.")
        return await func(client, message, **kwargs)
    return wrapper



@app.on_message(filters.command(["addsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
@language
async def useradd(client, message: Message):
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("Please reply to a user's message or give username/user_id.")
    user = await extract_user(message)
    if user.id in SUDOERS:
        return await message.reply_text(f"{user.mention} ɪs ᴀʟʀᴇᴀᴅʏ ᴀ sᴜᴅᴏ ᴜsᴇʀ.")
    added = await add_sudo(user.id)
    if added:
        SUDOERS.add(user.id)
        await message.reply_text(f"ᴀᴅᴅᴇᴅ **{user.mention}** ᴛᴏ sᴜᴅᴏ ᴜsᴇʀs." )
    else:
        await message.reply_text("❌ Failed to update sudo user list. Please try again later.")



@app.on_message(filters.command(["delsudo", "rmsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
@language
async def userdel(client, message: Message):
    logger.info("Received delsudo command.")
    
    if not message.reply_to_message:
        if len(message.command) != 2:
            return await message.reply_text("Please reply to a user's message or give username/user_id.")
    
    user = await extract_user(message)
    logger.info(f"Extracted user: {user.id if user else 'None'}")
    
    if user.id not in SUDOERS:
        return await message.reply_text(f"**{user.mention}** is not part of bot's sudo.")
    
    removed = await remove_sudo(user.id)
    logger.info(f"Removed user: {user.id}, success: {removed}")
    
    if removed:
        # If the user was removed from both the in-memory list and the database
        await message.reply_text(f"**{user.mention}** removed from bot's sudo users.")
    else:
        await message.reply_text("❌ Failed to update sudo user list. Please try again later.")


@app.on_message(filters.command(["sudolist", "listsudo", "sudoers"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & ~BANNED_USERS)
async def sudoers_list(client, message: Message):
    keyboard = [[InlineKeyboardButton("๏ ᴠɪᴇᴡ sᴜᴅᴏʟɪsᴛ ๏", callback_data="check_sudo_list")]]
    reply_markups = InlineKeyboardMarkup(keyboard)
    await message.reply_video(video="https://telegra.ph/file/3c9b53024f150d99032e1.mp4", caption="**» ᴄʜᴇᴄᴋ sᴜᴅᴏ ʟɪsᴛ ʙʏ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ.**\n\n**» ɴᴏᴛᴇ:**  ᴏɴʟʏ sᴜᴅᴏ ᴜsᴇʀs ᴄᴀɴ ᴠɪᴇᴡ. ", reply_markup=reply_markups)
    

@app.on_callback_query(filters.regex("^check_sudo_list$"))
async def check_sudo_list(client, callback_query: CallbackQuery):
    keyboard = []
    SUDOERS.add(OWNER_ID)
    if callback_query.from_user.id not in SUDOERS:
        return await callback_query.answer("sᴏʀʀʏ ʏᴀᴀʀ sɪʀғ ᴏᴡɴᴇʀ ᴏʀ sᴜᴅᴏ ᴡᴀʟᴇ ʜɪ sᴜᴅᴏʟɪsᴛ ᴅᴇᴋʜ sᴀᴋᴛᴇ ʜᴀɪ", show_alert=True)
    else:
        user = await app.get_users(OWNER_ID)

        # Ensure user is a single object and handle it accordingly
        if isinstance(user, list):
            user_mention = ", ".join([u.mention for u in user if hasattr(u, 'mention')]) or "Unknown User"
        else:
            user_mention = user.mention if hasattr(user, 'mention') else user.first_name

        caption = f"**˹ʟɪsᴛ ᴏғ ʙᴏᴛ ᴍᴏᴅᴇʀᴀᴛᴏʀs˼**\n\n**🌹Oᴡɴᴇʀ** ➥ {user_mention}\n\n"

        keyboard.append([InlineKeyboardButton("๏ ᴠɪᴇᴡ ᴏᴡɴᴇʀ ๏", url=f"tg://openmessage?user_id={OWNER_ID}")])
        
        count = 1
        for user_id in SUDOERS:
            if user_id != OWNER_ID:
                try:
                    user = await app.get_users(user_id)
                    user_mention = user.mention if user else f"**🎁 Sᴜᴅᴏ {count} ɪᴅ:** {user_id}"
                    caption += f"**🎁 Sᴜᴅᴏ** {count} **»** {user_mention}\n"
                    button_text = f"๏ ᴠɪᴇᴡ sᴜᴅᴏ {count} ๏ "
                    keyboard.append([InlineKeyboardButton(button_text, url=f"tg://openmessage?user_id={user_id}")])
                    count += 1
                except Exception as e:
                    logging.error(f"Error fetching user {user_id}: {e}")
                    continue

        # Add a "Back" button at the end
        keyboard.append([InlineKeyboardButton("๏ ʙᴀᴄᴋ ๏", callback_data="back_to_main_menu")])

        if keyboard:
            reply_markup = InlineKeyboardMarkup(keyboard)
            await callback_query.message.edit_caption(caption=caption, reply_markup=reply_markup)

@app.on_callback_query(filters.regex("^back_to_main_menu$"))
async def back_to_main_menu(client, callback_query: CallbackQuery):
    keyboard = [[InlineKeyboardButton("๏ ᴠɪᴇᴡ sᴜᴅᴏʟɪsᴛ ๏", callback_data="check_sudo_list")]]
    reply_markupes = InlineKeyboardMarkup(keyboard)
    await callback_query.message.edit_caption(caption="**» ᴄʜᴇᴄᴋ sᴜᴅᴏ ʟɪsᴛ ʙʏ ɢɪᴠᴇɴ ʙᴇʟᴏᴡ ʙᴜᴛᴛᴏɴ.**\n\n**» ɴᴏᴛᴇ:**  ᴏɴʟʏ sᴜᴅᴏ ᴜsᴇʀs ᴄᴀɴ ᴠɪᴇᴡ. ", reply_markup=reply_markupes)




@app.on_message(filters.command(["delallsudo"], prefixes=["/", "!", "%", ",", "", ".", "@", "#"]) & filters.user(OWNER_ID))
@language
async def del_all_sudo(client, message: Message):
    count = len(SUDOERS) - 1  # Exclude the admin from the count
    for user_id in SUDOERS.copy():
        if user_id != OWNER_ID:
            removed = await remove_sudo(user_id)
            if removed:
                SUDOERS.remove(user_id)
                count -= 1
    await message.reply_text(f"ʀᴇᴍᴏᴠᴇᴅ {count} ᴜsᴇʀs ғʀᴏᴍ ᴛʜᴇ sᴜᴅᴏ ʟɪsᴛ.")
