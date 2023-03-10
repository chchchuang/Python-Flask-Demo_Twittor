from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_mail import Mail

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
login_manager.login_view = "login" # 未登入時查看的頁面
mail = Mail()

from twittor.config import Config
from twittor.route import index, login, logout, register, user, page_not_found, edit_profile, reset_password_request, password_reset, explore, user_activate

def create_app():
    app = Flask(__name__, template_folder = "templates",
                static_folder = "static", static_url_path = "/img/")
    #app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///twittor.db"
    #app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:root@localhost:3306/twittor"
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    mail.init_app(app)

    #原裝飾器的功能 @app.route("/")
    # map(url, endpoint) & map(endpoint, view_func)
    # url_for(endpoint) 由 endpoint找到相關聯的 url, view_func 2023/3/2
    app.add_url_rule("/", endpoint = "index", view_func = index, methods = ["GET","POST"])
    app.add_url_rule("/index", "index", index, methods = ["GET","POST"])
    app.add_url_rule("/login", "login", login, methods = ["GET","POST"])
    app.add_url_rule("/logout", "logout", logout)
    app.add_url_rule("/register", "register", register, methods = ["GET","POST"])
    app.add_url_rule("/<username>", "profile", user, methods = ["GET","POST"])
    app.add_url_rule("/edit_profile", "edit_profile", edit_profile, methods = ["GET","POST"])
    app.add_url_rule("/reset_password_request", "reset_password_request", reset_password_request, methods = ["GET","POST"])
    app.add_url_rule("/password_reset/<token>", "password_reset", password_reset, methods = ["GET","POST"])
    app.add_url_rule("/explore", "explore", explore)
    app.add_url_rule("/activate/<token>", "user_activate", user_activate)
    app.register_error_handler(404, page_not_found) #abort 404錯誤代碼後執行 page_not_found func
    return app
 