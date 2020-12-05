import os

from flask import Flask, url_for, render_template, request, flash

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
    app.register_blueprint(authentication.bp)

    # Simple test page
    @app.route('/')
    def hello():
        return render_template('Puistoseuranta.html')

    # Addition of new measurement devices
    @app.route('/lisaa', methods=['GET', 'POST'])
    @authentication.auth
    def lisays():
        if request.method == 'POST':
            tunnus   = request.form.get("tunnus", "")
            sijainti = request.form['sijainti'].lower()
            database = db.get_db()
            error    = None

            if not sijainti:
                error = 'Sijainti tarvitaan'
            elif database.execute(               # Check if the location is unique
                'SELECT id FROM laite WHERE sijainti = ?', (sijainti,)
            ).fetchone() is not None:
                error = 'Sijainti {} löytyy jo tietokannasta'.format(sijainti)
            elif tunnus is not None:
                if database.execute(
                    'SELECT id FROM laite WHERE id = ?', (tunnus,)
                ).fetchone() is not None:
                    error = 'Tunnus {} löytyy jo tietokannasta. Jätä kenttä tyhjäksi automaattista tunnuksen luontia varten'.format(tunnus)



            if error is None:
                # Generate new id
                if tunnus == "" or int(tunnus) < 0:
                    database.execute(
                        'INSERT INTO laite (sijainti) VALUES (?)',
                        (sijainti,)
                    )
                # Else use the given id
                else:
                    database.execute(
                        'INSERT INTO laite (id, sijainti) VALUES (?,?)',
                        (tunnus, sijainti,)
                    )
                database.commit()
                # Return the new id for rendering
                lisatty = database.execute(
                    'SELECT id FROM laite WHERE sijainti =?', (sijainti,)
                ).fetchone()
                print(lisatty)

                return render_template('lisaa.html', nayta=True, tunnus=lisatty['id'], sijainti=sijainti )

            flash(error)
        

        return render_template('lisaa.html')

    return app
