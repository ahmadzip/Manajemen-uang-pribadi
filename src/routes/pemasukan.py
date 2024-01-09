from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from src.lib.auth_checks import check_is_confirmed
from src.models.models import Pemasukan
from src import app, db
from flask import flash, redirect, url_for
pemasukanBp = Blueprint("pemasukan", __name__)


@pemasukanBp.route("/pemasukan", methods=["GET", "POST"])
@login_required
@check_is_confirmed
def pemasukan():
    if request.method == "POST":
        jumlah = request.form.get("nominal")
        jumlah = int(''.join(filter(str.isdigit, jumlah)))
        tanggal = request.form.get("tanggal")
        keterangan = request.form.get("keterangan")
        user_id = current_user.id
        existing_entry = Pemasukan.query.filter_by(
            jumlah=jumlah, tanggal=tanggal, keterangan=keterangan, user_id=user_id).first()
        if existing_entry is None:
            new_entry = Pemasukan(
                jumlah=jumlah, tanggal=tanggal, keterangan=keterangan, user_id=user_id)
            db.session.add(new_entry)
            db.session.commit()
            flash("Data berhasil ditambahkan", "success")
        else:
            flash("Data sudah ada di database", "danger")

    return render_template("dashboard/pemasukan.html")
