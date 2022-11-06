from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager

from twittor.config import Config

db=SQLAlchemy()
migrate=Migrate()
login_manager=LoginManager()
login_manager.login_view = 'login'

from twittor.route import index, login, logout, register

def create_app():
    app = Flask(__name__, template_folder='templates')
    #app.config["SQLALCHEMY_DATABASE_URI"]="sqlite:///twittor.db"
    #app.config["SQLALCHEMY_DATABASE_URI"]="mysql+pymysql://root:root@localhost:3306/twittor"
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    #原裝飾器的功能 @app.route("/")
    # map(url, endpoint) & map(endpoint, view_func)
    app.add_url_rule('/', endpoint='index', view_func=index)
    app.add_url_rule('/index', 'index', index)
    app.add_url_rule('/login', 'login', login, methods=['GET','POST'])
    app.add_url_rule('/logout', 'logout', logout)
    app.add_url_rule('/register', 'register', register, methods=['GET','POST'])
    return app
 