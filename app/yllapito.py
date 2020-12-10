# Näkymä laitteiden ylläpidolle. 
# Näkymässä voi lisätä ja poistaa laitteita.
from flask import (
    Blueprint, redirect, render_template, request, flash
)

from app.db import get_db
from app.authentication import auth

bp = Blueprint('yllapito', __name__, url_prefix="/yllapito")

@bp.route('/', methods=['GET', 'POST'])
@auth
def index():
    # Haetaan tietokanta ja kaikki mittauslaitteet
    db = get_db()
    
    laitteet = db.execute(
        'SELECT id, sijainti'
        ' FROM laite'
        ' ORDER BY id DESC'
    ).fetchall()

    if request.method == 'POST':
        tunnus   = request.form.get("tunnus", "")
        sijainti = request.form['sijainti'].lower()
        error    = None

        if not sijainti:
            error = 'Sijainti tarvitaan!'
        elif db.execute(                  # Tarkistetaan, että sijainti on uniikki
            'SELECT id FROM laite WHERE sijainti = ?', (sijainti,)
        ).fetchone() is not None:
            error = 'Sijainti {} löytyy jo tietokannasta'.format(sijainti)
        elif tunnus != "":
            if db.execute(
                'SELECT id FROM laite WHERE id = ?', (tunnus,)
            ).fetchone() is not None:
                error = 'Tunnus {} löytyy jo tietokannasta. Jätä kenttä tyhjäksi automaattista tunnuksen luontia varten'.format(tunnus)
            

        if error is None:
            # Luodaan uusi tunnus, jos sellaista ei ole jo
            if tunnus == "" or int(tunnus) < 0:
                db.execute(
                    'INSERT INTO laite (sijainti) VALUES (?)',
                    (sijainti,)
                )
            # Muuten käytetään annettua tunnusta
            else:
                db.execute(
                    'INSERT INTO laite (id, sijainti) VALUES (?,?)',
                    (tunnus, sijainti,)
                )
            
            db.commit()
            # Palautetaan uusi tunnus verkkosivulle
            lisatty = db.execute(
                'SELECT id FROM laite WHERE sijainti =?', (sijainti,)
            ).fetchone()

            return render_template('yllapito/index.html', nayta_lisays=True, tunnus=lisatty['id'], sijainti=sijainti, laitteet=laitteet)

        flash(error)

    return render_template('yllapito/index.html', laitteet=laitteet)