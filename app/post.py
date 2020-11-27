from flask import (
    Blueprint, flash, g, request
)

from app.db import get_db

bp = Blueprint('post', __name__, url_prefix='/post_data')

# Test page for POST-method
@bp.route('/testi', methods=['POST'])
def post():
    db = get_db()
    laite_id = request.form.get("laite_id")
    sisaan = request.form.get("sisaan")
    aika = request.form.get('aika')
    error = None

    if not laite_id:
        error = "Virheellinen laite_id."
    elif not sisaan:
        error = "Ei mittaustulosta."

    # Jos kaikki on ok. Lisätää mittaus tietokantaan
    if error is None:
        db.execute(
            'INSERT INTO sensor_data (laite_id, sisaan, aika) VALUES (?, ?, ?)',
            (laite_id, sisaan, aika)
        )
        db.commit()
        return 'Kaikki OK!'

    flash(error)
    return 'Kaikki ei ollut OK!'
