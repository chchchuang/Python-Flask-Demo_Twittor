from threading import Thread

from flask import current_app
from flask_mail import Message
from twittor import mail

def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)

def send_email(subject, recipients, text_body, html_body):
    msg = Message(
        subject = subject,
        recipients = recipients, # 接收者
        reply_to = 'noreply@twittor.com' # 回覆地址
    )
    # 看用戶端使用文本或 html格式閱讀 msg
    msg.body = text_body
    msg.html = html_body
    # mail.send(msg) # 單純使用 send, 沒有使用多 thread會卡住 3~4秒寄信
    Thread(
        target = send_async_email,
        args = (current_app._get_current_object(), msg)
    ).start()