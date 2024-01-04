#3rd party packages
from flask import Flask, render_template, request, redirect, url_for
from flask_mongoengine import MongoEngine
from flask_bcrypt import Bcrypt
from flask_login import LoginManager, current_user


# local -- created objects
from .client import SchoolClient



#--------------- CONFIGURING IMPORTANT FLASK EXTENSIONS ------------------------
db = MongoEngine() # Creating database object to interact with MongoDB
login_manager = LoginManager() # manages user's sessions,settings for logging in
bcrypt = Bcrypt()  # for password hashing.
school_client = SchoolClient()

# ------------------ importing blueprints to be used --------------
from .content.routes import content
from .users.routes import users

# custom 404
def custom_404(e):
    return render_template("404.html"), 404


# Todo
def create_app(test_config=None):
    app = Flask(__name__)

    #  storing the configuration of out Flask app.
    app.config.from_pyfile("config.py", silent=False)

    # this simply checks if I set up configuration for testing
    if test_config is not None:
        app.config.update(test_config)
    
    # initializes the created app based on what is needed
    db.init_app(app)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    # registering the blueprint to the created app and creating a custom error page
    app.register_blueprint(users)
    app.register_blueprint(content)
    app.register_error_handler(404, custom_404)

    login_manager.login_view = "users.login"
    
    return app