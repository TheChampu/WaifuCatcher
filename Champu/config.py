class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = "7006524418"
    SUDOERS = ["5702648302", "7006524418", "1414327092", "1302298741"]
    GROUP_ID = "-1001423108989"
    TOKEN = "7542742005:AAHnt7O-FLM9TE8t0EfwwPC45a1Adv5V8hk"
    MONGO_URL = "your db"
    PHOTO_URL = ["https://telegra.ph/file/7e5398823512d307128a3.jpg", "https://telegra.ph/file/c45dcb207d81e97cb4f6a.jpg", "https://telegra.ph/file/0bc6d65878e8300fbf0f8.jpg", "https://telegra.ph/file/0afb45203ff162ee7227b.jpg"]
    SUPPORT_CHAT = "TheChampuClub"
    UPDATE_CHAT = "ShivanshuHUB"
    BOT_USERNAME = "itsWaifuBot"
    CHARA_CHANNEL_ID = "-1002523648960"
    API_ID = "29893020"
    API_HASH = "28e79037f0b334ef0503466c53f08af5"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
