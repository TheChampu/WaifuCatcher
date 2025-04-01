class Config(object):
    LOGGER = True

    # Get this value from my.telegram.org/apps
    OWNER_ID = 7006524418
    SUDOERS = "7006524418", "7006524418"
    GROUP_ID = "-1002032426353"
    TOKEN = "6707490163:AAHZzqjm3rbEZsObRiNaT7DMtw_i5WPo_0o"
    MONGO_URL = "mongodb+srv://yash:shivanshudeo@yk.6bvcjqp.mongodb.net/?retryWrites=true&w=majority&appName=yk"
    PHOTO_URL = ["https://telegra.ph/file/b925c3985f0f325e62e17.jpg", "https://telegra.ph/file/4211fb191383d895dab9d.jpg"]
    SUPPORT_CHAT = "ShivanshuHUB"
    UPDATE_CHAT = "ChattingClub007"
    BOT_USERNAME = "ItsWaifuBot"
    CHARA_CHANNEL_ID = "-1002032426353"
    API_ID = 26626068
    API_HASH = "bf423698bcbe33cfd58b11c78c42caa2"

    
class Production(Config):
    LOGGER = True


class Development(Config):
    LOGGER = True
