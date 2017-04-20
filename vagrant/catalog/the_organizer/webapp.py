from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from flask_cors import CORS
from flask_restless import APIManager, ProcessingException
from flask_oauth import OAuth
from config import config
from flask import session as login_session
from flask_login import LoginManager, UserMixin, login_required, login_user, logout_user, current_user
import json


def auth_func(*args, **kw):
    if not current_user.is_authenticated:
        raise ProcessingException(
            description='Not authenticated! Log in at http://localhost:5000/login', code=401)

# 1) create the flask application.
app = Flask(__name__)

# 2) Set up the database. We can now import this anywhere.
database = SQLAlchemy(app)

# 3) Prepare for sessions
DBSession = sessionmaker(bind=database)
session = DBSession()

# 4) Start Login Manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
# 5) Load App Blueprints
from the_organizer.mod_item.controllers import mod_items as item_module
from the_organizer.mod_group.controllers import mod_groups as group_module
from the_organizer.mod_auth.controllers import mod_auth as auth_module

# 6) Register blueprint(s)
app.register_blueprint(item_module)
app.register_blueprint(group_module)
app.register_blueprint(auth_module)


def setup_app(config_name, app, database):
    """
    Creates a JSON:API compliant REST application.

    :param config_name str: String name of the config.
    :param app: The application.
    :param database: SQLAlchemy database.
    """

    # 0) Import models. SQLAlchemy requires this during app initialization.
    import models

    # 1) Set up appropriate app configs.
    app.config.from_object(config[config_name])
    
    # 2) Set up CORS.
    CORS(app)

    # 3) Get JSON:API compliant endpoints, based on models.
    apimanager = APIManager(
        app,
        flask_sqlalchemy_db=database,
        preprocessors=dict(GET_MANY=[auth_func], GET_SINGLE=[auth_func], POST=[auth_func], DELETE=[auth_func]))

    apimanager.create_api(models.Item, methods=['GET', 'POST', 'DELETE'])
    apimanager.create_api(models.Group, methods=['GET', 'POST', 'DELETE'])
    apimanager.create_api(models.ItemImage, methods=['GET', 'POST', 'DELETE'])

    return apimanager


@app.route('/')
def index():
    return render_template('start.html')


@app.route('/secret')
@login_required
def secret():
    return render_template('start.html')


# callback to reload the user object

@login_manager.user_loader
def load_user(userid):
    from the_organizer.models import User
    return User.query.get(userid)
