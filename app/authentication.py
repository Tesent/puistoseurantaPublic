import hashlib
from functools import wraps
from flask import (
    Blueprint, request, jsonify, session, render_template, redirect, url_for, flash
    )

from app.db import get_db

bp = Blueprint('authentication', __name__, url_prefix="/kirjaudu")

# Post-metodin autentikointi
def check_auth(username, password):
    return username == "laite" and password == "VahvaSalausOnVahva"

def authentication_required(f):
    @wraps(f)
    def wrapped_view(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            message = {'error': 'Basic Authentication required.'}
            resp = jsonify(message)
            resp.status_code = 401
            return resp

        return f(*args, **kwargs)

    return wrapped_view


# Kuorrute kirjautumisnäkymään
def auth (f):
    @wraps(f)
    def decorated(*args, **kwargs):
        if not 'kirjautunut' in session:
            return redirect(url_for('authentication.login'))
        return f(*args, **kwargs)

    return decorated

# Kirjautumista vaaditaan laitteen lisäämistä varten
@bp.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        error = None
        username = request.form.get("tunnus", "")
        password = request.form.get("salasana", "")
        m = hashlib.sha512()
        avain = u"omasalainenavain"
        m.update(avain.encode("UTF-8"))
        m.update(password.encode("UTF-8"))

        if username == "":
            error = 'Virheellinen käyttäjätunnus!'
        elif m.hexdigest() != "dabd321b339fd0c5f9e1a22b72c64aed0fa85127f3c876cc1c4b09a949be44ea9a316c4091a26e0b12f3d97c45ad1127acff71885b5efa3f9f9c4a1be8e72256":
            error = "Virheellinen salasana!"

        if error is None:
            session['kirjautunut'] = "ok"
            return redirect(url_for('yllapito.index'))

        flash(error)

    return render_template('authentication/kirjaudu.html')

# Logout-näkymä
@bp.route('/logout')
def logout():
    session.pop('kirjautunut',None)
    return redirect(url_for('hello'))