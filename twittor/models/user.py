from datetime import datetime
from hashlib import md5
import time

from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from flask import current_app
import jwt

from twittor import db, login_manager
from twittor.models.tweet import Tweet

#記錄follow關係,沒定義class是因為是表示外來物件的關係
followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
    )
#記錄帳號資訊
class User(UserMixin, db.Model): #大寫User是class, 默認小寫user是實例(db的表) # User繼承 db: 類似執行 MySQL上的 create table user
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True) # index=True搜尋較快
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    about_me = db.Column(db.String(120)) #增加數據庫記得做 migration
    create_time = db.Column(db.DateTime, default=datetime.utcnow)

    tweets = db.relationship('Tweet', backref='author', lazy='dynamic') #一對多(一用戶對多 tweets), 非 user表內的 data, 使用 Tweet class, 非 tweet表
    # backref: 可以視為暗號, 使用 Tweet.author就可以視為 User, 讀取 User表格的內容

    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id), # follow者的 ID==自己 ID -> 自己 follow誰
        secondaryjoin=(followers.c.followed_id == id), #被 follow者的 ID==自己 ID -> 自己被誰 follow
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic') #多對多, 是一個 list, 可以藉由 append增加 follow對象

    def __repr__(self) -> str: #顯示實例值
        return "id={}, username={}, email={}, password_hash={}".format(
            self.id, self.username, self.email, self.password_hash
        )

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size=80): # 生成頭像
        md5_digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return "https://www.gravatar.com/avatar/{}?d=identicon&s={}".format(md5_digest, size)
        # d=identicon 生成隨機相對唯一頭像

    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
    def is_following(self, user): #check是否已 follow user
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0
        #在followed名單內,followed_id與user.id一致表示已追蹤
        #The “c” is an attribute of SQLAlchemy tables that are not defined as models. For these tables, the table columns are all exposed as sub-attributes of this “c” attribute.
    
    def own_and_followed_tweets(self):
        followed = Tweet.query.join(
            followers, (followers.c.followed_id == Tweet.user_id)).filter(
                followers.c.follower_id == self.id)
            #將有follow user的followers表與Tweet兜在一起, filter我有follow的就好
        own = Tweet.query.filter_by(user_id=self.id)
        return followed.union(own).order_by(Tweet.create_time.desc())
        #union:聯集
    
    def get_jwt(self, expire=7200):
        return jwt.encode(
            {
                'email': self.email,
                'exp': time.time() + expire
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        ) #.decode('utf-8') -> AttributeError: 'str' object has no attribute 'decode'

    @staticmethod # 因為 route.password_reset內 user = User.verify_jwt(token) 非使用實例, 直接使用類別方法
    def verify_jwt(token): # 不用 self
        try:
            email = jwt.decode(
                token,
                current_app.config['SECRET_KEY'],
                algorithms=['HS256']
            )
            email = email['email']
        except:
            return
        return User.query.filter_by(email=email).first()

# loginManager中的 user_loader方法作為裝飾器可以讓 login_user方法根據id找到用戶來記錄登入用戶資訊與狀態
@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))