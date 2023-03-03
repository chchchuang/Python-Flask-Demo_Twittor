import os

#當前文件目錄的絕對路徑
config_path = os.path.abspath(os.path.dirname(__file__)) # os.path.dirname(__file__)表示當前文件的名子

class Config():
    #改用絕對路徑, 如果有設置環境變量使用 DATABASE_URL, 沒有的話就用後者
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "sqlite:///" + os.path.join(config_path, 'twittor.db'))    
    # SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(config_path, 'twittor.db')
    # SQLALCHEMY_DATABASE_URI="mysql+pymysql://root:root@localhost:3306/twittor"
    SECRET_KEY="anything but secret" #for forms
    TWEET_PER_PAGE = 3