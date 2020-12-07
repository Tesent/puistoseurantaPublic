from flask import (
    Blueprint, flash, g, request
)

from app.db import get_db
from app.authentication import authentication_required

bp = Blueprint('post', __name__, url_prefix='/post_data')

# Test page for POST-method
@bp.route('/testi', methods=['POST'])
@authentication_required
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

    return 'Kaikki ei ollut OK!'

@bp.route('/tarkkailu', methods=['POST'])
@authentication_required
def tarkkailu():
    db = get_db()
    laite_id  = request.form("laite_id")
    etaisyys1 = request.form.get("etaisyys1")
    etaisyys2 = request.form.get("etaisyys2")
    ip        = request.form.get("ip")
    error     = None

    if not laite_id:
        error = "Virheellinen laitteen tunnus"
    elif not etaisyys1:
        error = "Ei ensimmäistä etäisyyttä"
    elif not etaisyys2:
        error = "Ei toista etäisyyttä"
    elif not ip:
        error = "Virheellinen ip-osoite"
    # Jos kaikki on kunnossa lisätään laitteen tila tietokantaan
    if error is None:
        db.execute(
            'INSERT INTO laitteen_tila (laite_id, etaisyys1, etaisyys2, ip)'
            ' VALUES (?, ?, ?, ?)',
            (laite_id, etaisyys1, etaisyys2, ip)
        )
        db.commit()
        return "Kaikki OK!"

    return error