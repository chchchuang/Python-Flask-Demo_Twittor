import os

#當前文件目錄的絕對路徑
config_path = os.path.abspath(os.path.dirname(__file__)) # os.path.dirname(__file__)表示當前文件的名子

class Config():
    #改用絕對路徑, 如果有設置環境變量使用 DATABASE_URL, 沒有的話就用後者
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(config_path, "twittor.db"))
    # SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:root@localhost:3306/twittor"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.environ.get("SECRET_KEY", "anything but secret") # for forms
    TWEET_PER_PAGE = os.environ.get("TWEET_PER_PAGE", 20)

    MAIL_DEFAULT_SENDER = os.environ.get("MAIL_DEFAULT_SENDER", "noreply@twittor.com")
    MAIL_SERVER = os.environ.get("MAIL_SERVER", "smtp.googlemail.com")
    MAIL_PORT = os.environ.get("MAIL_PORT", 587)
    MAIL_USE_TLS = os.environ.get("MAIL_USE_TLS", 1)
    MAIL_USERNAME = os.environ.get("MAIL_USERNAME", "email")
    MAIL_PASSWORD = os.environ.get("MAIL_PASSWORD", "password")
    MAIL_SUBJECT_RESET_PASSWORD = "[Twittor] Please Reset Your Password"
    MAIL_SUBJECT_USER_ACTIVATE = "[Twittor] Please Activate Your Account"

    SOCIAL_FACEBOOK = {
        "consumer_key": "facebook app id",
        "consumer_secret": "facebook app secret"
    }
    SECURITY_POST_LOGIN = "/profile"