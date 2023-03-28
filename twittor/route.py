from flask import render_template, redirect, url_for, request, abort, current_app, flash
from flask_login import login_user, current_user, logout_user, login_required

from twittor.forms import LoginForm, RegisterForm, EditProfileForm, TweetForm, PasswordResetRequestForm, PasswdRestForm, EditTweetForm
from twittor.models.user import User #要讓 flask知道 model存在
from twittor.models.tweet import Tweet
from twittor.email import send_email
from twittor import db

from datetime import datetime, timezone
from functools import wraps
import json, requests

@login_required # 必須 login才能查看頁面
def index():
    form = TweetForm()
    if form.validate_on_submit():
        t = Tweet(body = form.tweet.data, author = current_user)
        db.session.add(t)
        db.session.commit()
        return redirect(url_for("index"))
    page_num = int(request.args.get("page") or 1)
    tweets = current_user.own_and_followed_tweets().paginate(page = page_num, per_page = current_app.config["TWEET_PER_PAGE"], error_out = False) # error_out==True: 為空時會報錯
    prev_url = url_for("index", page = tweets.prev_num) if tweets.has_prev else None
    next_url = url_for("index", page = tweets.next_num) if tweets.has_next else None
    return render_template("index.html", title = current_user.username, form = form, tweets = tweets.items,
        prev_url = prev_url, next_url = next_url)

def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username = form.username.data).first() #取第一個, 因為 username唯一, 所有只有一個或是 None
        if not user or not user.check_password(form.password.data):
            flash("invalid username or password")
            return redirect(url_for("login"))
        if not user.is_activated:
            flash("Send an email to your email address, please check!")
            send_email_for_user_activate(user)
            return redirect(url_for("login"))
        login_user(user, remember = form.remember_me.data) #記錄登入用戶資訊
        next_page = request.args.get("next") #搜尋別人網址時要求登入, 登入後直接跳轉該網址
        if next_page:
            return redirect(next_page)
        return redirect(url_for("index"))
    return render_template("login.html", title = "Sign In", form = form)

def to_json(func):
    @wraps(func) # avoid func.__name__屬性被修改成 wrap
    def wrap(*args, **kwargs):
        get_fun = func(*args, **kwargs)
        return json.dumps(get_fun)
    
    return wrap

@to_json
def API_FB_login():
    userID = request.json["userID"]
    accessToken = request.json["accessToken"]
    FBuser = User.query.filter_by(FBuserID = userID).first()
    if not FBuser:
        u = User(FBuserID = userID, FBaccessToken = accessToken)
        data = requests.get(
            "https://graph.facebook.com/me?fields=id,name,email&access_token=" + accessToken
        )
        if data.status.code == 200:
            u.username = data.json()["name"]
        db.session.add(u)
        db.session.commit()
        login_user(u, remember = True)
    else:
        login_user(FBuser, remember = True)
    return "FB_login_success"
    
def logout():
    logout_user()
    flash("You have successfully logged out.")
    return redirect(url_for("login"))

def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Send an email to confirm your email address, please check!")
        send_email_for_user_activate(user)
        return redirect(url_for("login"))
    return render_template("register.html", title = "Registeration", form = form)

@login_required
def user(username): #參數來自網址
    user = User.query.filter_by(username = username).first()
    if not user:
        abort(404)
    #1. tweets = Tweet.query.filter_by(user_id=u.id)
    #2. tweets = Tweet.query.filter_by(author=u) # model有設立 backref,直接透過 author=username搜尋,不需使用 user_id
    page_num = int(request.args.get("page") or 1)
    tweets = user.tweets.order_by(Tweet.create_time.desc()).paginate(page = page_num, per_page = current_app.config["TWEET_PER_PAGE"], error_out = False)
    prev_url = url_for("profile", username = username, page = tweets.prev_num) if tweets.has_prev else None
    next_url = url_for("profile", username = username, page = tweets.next_num) if tweets.has_next else None
    # 處理 follow/ unfollow
    if request.method == "POST": # GET, POST必須大寫
        # print(request.form.to_dict()) #key: submit.name, value: submit.value
        if request.form["request_button"] == "Follow":
            current_user.follow(user)
            db.session.commit()
        elif request.form["request_button"] == 'Unfollow':
            current_user.unfollow(user)
            db.session.commit()
        # else: # activate
        #     flash("Send an email to your email address, please check!")
        #     send_email_for_user_activate(current_user)
    return render_template("user.html", title = "Profile", user = user, tweets = tweets.items,
        prev_url = prev_url, next_url = next_url)

def page_not_found(e):
    return render_template("404.html", title = "Page Not Found!"), 404

def send_email_for_user_activate(user):
    token = user.get_jwt()
    url_user_activate = url_for("user_activate", token = token, _external = True)
    send_email(
        subject = current_app.config["MAIL_SUBJECT_USER_ACTIVATE"],
        recipients = [user.email],
        text_body = render_template(
            "email/us_activate_request.txt",
            username = user.username,
            url_user_activate = url_user_activate
        ),
        html_body = render_template(
            "email/us_activate_request.html",
            username = user.username,
            url_user_activate = url_user_activate
        )
    )

def user_activate(token):
    user = User.verify_jwt(token)
    if not user:
        msg = "Token has expired, please try to re-send email."
        return render_template("activated.html", title = "activated", msg = msg)
    if user.is_activated:
        flash("Your email is already confirmed!")
        return redirect(url_for("index"))
    else:
        user.is_activated = True
        db.session.commit()
        msg = "User has been activated!"
        return render_template("activated.html", title = "activated", msg = msg)

@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == "GET": # 原先已有 about_me
        form.about_me.data = current_user.about_me
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        return redirect(url_for("profile", username = current_user.username))
    return render_template("edit_profile.html", title = "Edit Profile", form = form)

@login_required
def edit_tweet(id):
    t = Tweet.query.filter_by(id = id).first()
    if not t:
        abort(404)
    form = EditTweetForm()
    # edit tweet
    if request.method == "GET":
        form.tweet.data = t.body
    if form.validate_on_submit():
        t.body = form.tweet.data
        t.is_edited = True
        db.session.commit()
        return redirect(url_for("profile", username = current_user.username))
    # delete/(un)like tweet
    if request.method == "POST": # GET, POST必須大寫
        # print(request.form.to_dict()) #key: submit.name, value: submit.value
        if request.form["request_button"] == "Delete":
            db.session.delete(t)
            db.session.commit()
        elif request.form["request_button"] == "Like":
            current_user.like(t)
            db.session.commit()
        elif request.form["request_button"] == "Unlike":
            current_user.unlike(t)
            db.session.commit()
        return redirect(url_for("index"))
    return render_template("edit_tweet.html", title = "Edit Tweet", form = form)

def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = PasswordResetRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email = form.email.data).first()
        if user:
            flash(
                "You should soon receive an email allowing you to reset your \
                password. Please make sure to check your spam and trash \
                if you can't find the email."
            )
            token = user.get_jwt()
            # url = 'http://127.0.0.1:5000/password_reset/{}'.format(token)
            url_password_reset = url_for("password_reset", token = token, _external = True) # _external==True: 會傳完整地址
            url_password_reset_request = url_for("reset_password_request", _external = True)
            send_email(
                subject = current_app.config["MAIL_SUBJECT_RESET_PASSWORD"],
                # sender = 'noreply@twittor.com', # config已設定 defalut sender
                recipients = [user.email],
                text_body = render_template(
                    "email/passwd_reset.txt",
                    url_password_reset = url_password_reset,
                    url_password_reset_request = url_password_reset_request
                ),
                html_body = render_template(
                    "email/passwd_reset.html",
                    url_password_reset = url_password_reset,
                    url_password_reset_request = url_password_reset_request
                ),
            )
        return redirect(url_for("login"))
    return render_template("password_reset_request.html", title = "Reset Password", form = form)

def password_reset(token):
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    user = User.verify_jwt(token)
    if not user:
        return redirect(url_for("login"))
    form = PasswdRestForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template("password_reset.html", title = "Reset Password", form = form)

@login_required
def explore():
    # get all tweets
    page_num = int(request.args.get("page") or 1)
    tweets = Tweet.query.order_by(Tweet.create_time.desc()).paginate(
        page = page_num, per_page = current_app.config["TWEET_PER_PAGE"], error_out = False
    )
    prev_url = url_for("explore", page = tweets.prev_num) if tweets.has_prev else None
    next_url = url_for("explore", page = tweets.next_num) if tweets.has_next else None
    return render_template("explore.html", title = "explore", tweets = tweets,
        prev_url = prev_url, next_url = next_url)


        
