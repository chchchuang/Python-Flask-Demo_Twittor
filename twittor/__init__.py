from flask import Flask
from twittor.route import index, login


def create_app():
    app = Flask(__name__, template_folder='templates')
    app.secret_key="anything but secret"
    #原裝飾器的功能 @app.route("/")
    # map(url, endpoint) & map(endpoint, view_func)
    app.add_url_rule('/', endpoint='index', view_func=index)
    app.add_url_rule('/login', 'login', login, methods=['GET','POST'])
    return app
 