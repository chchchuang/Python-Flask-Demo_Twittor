from datetime import datetime

from twittor import db

#記錄發文推文
class Tweet(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    body = db.Column(db.String(140))
    create_time = db.Column(db.DateTime, default = datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id")) #一對多的多(一用戶對多 tweets), user_id domain限制於 user表內的 id
    is_edited = db.Column(db.Boolean, default = False)

    def __repr__(self) -> str:
        return "id={}, body={}, create_time={}, user_id={}".format(
            self.id, self.body, self.create_time, self.user_id
        )
