import os

from flask import Flask
from flask import url_for

def create_app(test_config=None):
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
            SECRET_KEY='dev',
            DATABASE=os.path.join(app.instance_path, 'app.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        # Oh oh
        pass

    # Simple test page
    @app.route('/')
    def hello():
        return app.send_static_file('Puistoseuranta.html')

    # database stuff
    from . import db
    db.init_app(app)

    return app
