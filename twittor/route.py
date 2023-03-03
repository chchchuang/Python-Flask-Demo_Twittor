from flask import render_template, redirect, url_for, request, abort, current_app
from flask_login import login_user, current_user, logout_user, login_required
from twittor.forms import LoginForm, RegisterForm, EditProfileForm, TweetForm
from twittor.models import User, Tweet #要讓 flask知道 model存在
from twittor import db

@login_required # 必須 login才能查看頁面
def index():
    form = TweetForm()
    if form.validate_on_submit():
        t = Tweet(body=form.tweet.data, author=current_user)
        db.session.add(t)
        db.session.commit()
        return redirect(url_for('index'))
    page_num = int(request.args.get('page') or 1)
    tweets = current_user.own_and_followed_tweets().paginate(page=page_num, per_page=current_app.config["TWEET_PER_PAGE"], error_out=False) # error_out==True: 為空時會報錯
    prev_url = url_for('index', page=tweets.prev_num) if tweets.has_prev else None
    next_url = url_for('index', page=tweets.next_num) if tweets.has_next else None
    return render_template("index.html", tweets=tweets.items, form=form,
        prev_url=prev_url, next_url=next_url)


def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        u = User.query.filter_by(username=form.username.data).first() #取第一個, 因為 username唯一, 所有只有一個或是 None
        if u is None or not u.check_password(form.password.data):
            print("invalid username or password")
            return redirect(url_for('login'))
        login_user(u, remember=form.remember_me.data) #記錄登入用戶資訊
        next_page = request.args.get('next') #搜尋別人網址時要求登入, 登入後直接跳轉該網址
        if next_page:
            return redirect(next_page)
        return redirect(url_for('index'))
    return render_template("login.html", title="Sign In", form=form)

def logout():
    logout_user()
    return redirect(url_for('login'))

def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template("register.html", title="Registeration", form=form)

@login_required
def user(username): #參數來自網址
    u = User.query.filter_by(username=username).first()
    if u is None:
        abort(404)
    #1. tweets = Tweet.query.filter_by(user_id=u.id)
    #2. tweets = Tweet.query.filter_by(author=u) # model有設立 backref,直接透過 author=username搜尋,不需使用 user_id
    page_num = int(request.args.get('page') or 1)
    tweets = u.tweets.order_by(Tweet.create_time.desc()).paginate(page=page_num, per_page=current_app.config["TWEET_PER_PAGE"], error_out=False)
    prev_url = url_for('profile', username=username, page=tweets.prev_num) if tweets.has_prev else None
    next_url = url_for('profile', username=username, page=tweets.next_num) if tweets.has_next else None
    # 處理 follow/ unfollow
    if request.method == 'POST':
        # print(request.form.to_dict()) #key: submit.name, value: submit.value
        if request.form['request_button'] == 'Follow':
            current_user.follow(u)
            db.session.commit()
        else:
            current_user.unfollow(u)
            db.session.commit()
    return render_template("user.html", title="Profile", user=u, tweets=tweets.items,
        prev_url=prev_url, next_url=next_url)

def page_not_found(e):
    return render_template("404.html"), 404

@login_required
def edit_profile():
    form = EditProfileForm()
    if request.method == 'GET': # 原先已有 about_me
        form.about_me.data = current_user.about_me
    if form.validate_on_submit():
        current_user.about_me = form.about_me.data
        db.session.commit()
        return redirect(url_for('profile', username=current_user.username)) #url_for('endpoint') -> def user(username)
    return render_template("edit_profile.html", form=form)
