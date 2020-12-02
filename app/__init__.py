import os

from flask import Flask, url_for, render_template, request

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

    # database stuff
    from . import db
    db.init_app(app)
    app.register_blueprint(db.bp)

    # Handling of data post
    from . import post
    app.register_blueprint(post.bp)

    # not so secure authentication
    from . import authentication

    # Simple test page
    @app.route('/')
    def hello():
        return render_template('Puistoseuranta.html')

    return app
