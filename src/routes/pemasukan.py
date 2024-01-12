from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from src.lib.auth_checks import check_is_confirmed
from src.models.models import Pemasukan, Saldo
from src.lib.forms import PemasukanForm

from src import app, db
from flask import flash, redirect, url_for
pemasukanBp = Blueprint("pemasukan", __name__)


@pemasukanBp.route("/pemasukan", methods=["GET", "POST"])
@login_required
@check_is_confirmed
def pemasukan():
    form = PemasukanForm(request.form)
    if request.method == "POST":
        jumlah = request.form.get("nominal")
        jumlah = int(''.join(filter(str.isdigit, jumlah)))
        tanggal = request.form.get("tanggal")
        keterangan = request.form.get("keterangan")
        user_id = current_user.id
        existing_entry = Pemasukan.query.filter_by(
            jumlah=jumlah, tanggal=tanggal, keterangan=keterangan, user_id=user_id).first()
        existing_saldo = Saldo.query.filter_by(user_id=user_id).first()
        if existing_entry is None:
            db.session.add(Pemasukan(jumlah=jumlah, tanggal=tanggal,
                           keterangan=keterangan, user_id=user_id))
            if existing_saldo is None:
                db.session.add(
                    Saldo(tanggal=tanggal, saldo=jumlah, user_id=user_id))
            else:
                existing_saldo.saldo += jumlah
            db.session.commit()
            flash("Data berhasil ditambahkan", "success")
        else:
            flash("Data sudah ada di database", "danger")
    get_pemasukan = Pemasukan.query.filter_by(user_id=current_user.id).all()
    for item in get_pemasukan:
        item.type = "pemasukan"
    short_pemasukan = sorted(
        get_pemasukan, key=lambda x: x.tanggal, reverse=True)
    print(short_pemasukan)
    return render_template("dashboard/pemasukan.html", form=form, gabungkan=short_pemasukan)
