from telegram import Update
from telegram.ext import CommandHandler, CallbackContext
from Champu import Champuu as app
from Champu import SUDOERS_collection, application
from Champu.modules.database.sudo import add_to_SUDOERS, remove_from_SUDOERS, get_user_username, fetch_SUDOERS

DEV_LIST = [7006524418]
authorized_users = [7006524418]

async def is_user_sudo(user_id: int) -> bool:
    user = await SUDOERS_collection.find_one({"id": user_id})
    return bool(user)

async def add_sudo_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    
    # Check if the user is authorized
    if user_id not in authorized_users:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    if update.message.reply_to_message:
        replied_user_id = update.message.reply_to_message.from_user.id
        username = await get_user_username(replied_user_id)
        sudo_title = ' '.join(context.args) if context.args else "Sudo User"
        await add_to_SUDOERS(replied_user_id, username, sudo_title)
        await update.message.reply_text(f"User {username} has been added as sudo with title '{sudo_title}'.")
    else:
        await update.message.reply_text("Please reply to a message to add a user as sudo.")

async def remove_sudo_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id

    # Check if the user is authorized
    if user_id not in authorized_users:
        await update.message.reply_text("You are not authorized to use this command.")
        return

    if update.message.reply_to_message:
        replied_user_id = update.message.reply_to_message.from_user.id
        user = await SUDOERS_collection.find_one({"id": replied_user_id})
        if user:
            await remove_from_SUDOERS(replied_user_id)
            username = user.get('username')
            await update.message.reply_text(f"User {username} has been removed from sudo users.")
        else:
            await update.message.reply_text("User not found in sudo users.")
    else:
        await update.message.reply_text("Please reply to a message to remove a user from sudo.")

async def sudo_list_command(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    
    # Check if the user is a sudo user
    if not await is_user_sudo(user_id):
        await update.message.reply_text("You are not authorized to view the sudo list.")
        return

    SUDOERS = await fetch_SUDOERS()
    if not SUDOERS:
        await update.message.reply_text("No sudo users found.")
        return

    message = "Sudo Users:\n"
    for user in SUDOERS:
        message += f"User ID: {user['user_id']}, Username: @{user['username']}, Title: {user['sudo_title']}\n"
    
    await update.message.reply_text(message)

# Add command handlers
application.add_handler(CommandHandler("addsudo", add_sudo_command))
application.add_handler(CommandHandler("sudoremove", remove_sudo_command))
application.add_handler(CommandHandler("sudolist", sudo_list_command))
