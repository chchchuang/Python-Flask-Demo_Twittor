from twittor import db
from datetime import datetime
#記錄帳號資訊
class User(db.Model): #大寫User是class, 小寫user是db內表的名稱
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, index=True)
    email = db.Column(db.String(64), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    tweets = db.relationship('Tweet', backref='author', lazy='dynamic')

    def __repr__(self) -> str: #顯示實例值
        return "id={}, username={}, email={}, password_hash={}".format(
            self.id, self.username, self.email, self.password_hash
        )
#記錄發文推文
class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    create_time = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #user_id domain限制於 user表內的 id

    def __repr__(self) -> str:
        return "id={}, body={}, create_time={}, user_id={}".format(
            self.id, self.body, self.create_time, self.user_id
        )