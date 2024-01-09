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
        nominal = request.form.get("nominal")
        tanggal = request.form.get("tanggal")
        keterangan = request.form.get("keterangan")
        user_id = current_user.id
        print(nominal, tanggal, keterangan, user_id)
        existing_entry = Pemasukan.query.filter_by(
            nominal=nominal, tanggal=tanggal, keterangan=keterangan, user_id=user_id).first()
        if existing_entry is None:
            new_entry = Pemasukan(
                nominal=nominal, tanggal=tanggal, keterangan=keterangan, user_id=user_id)
            db.session.add(new_entry)
            db.session.commit()
            flash("Data berhasil ditambahkan", "success")
            return redirect(url_for("dashboard.home"))
        else:
            flash("Data sudah ada di database", "danger")
            return redirect(url_for("dashboard.home"))

    return render_template("dashboard/pemasukan.html")
