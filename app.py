from flask import Flask
from application.database import db
from flask_login import LoginManager
from application.resources import api
from werkzeug.exceptions import Unauthorized
app=Flask(__name__)

app=None

def create_app():
    app = Flask(__name__)
    app.debug = True
    app.secret_key = 'abcdefghijklmnopqrstuvwxyz123'
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///LibraryManagementSys.sqlite3"
    app.config['SECRET_KEY']="abcdefghijklmnopqrstuvwxyz123"
    db.init_app(app)
    api.init_app(app)
    login_manager = LoginManager()
    login_manager.init_app(app)
    app.app_context().push()


    # login_manager.id_attribute = 'id'
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    @login_manager.unauthorized_handler
    def unauthorized():
        return render_template('unauthorized.html'), 401

    return app

app=create_app()

from application.controller import *

if __name__ == "__main__":
    app.run()