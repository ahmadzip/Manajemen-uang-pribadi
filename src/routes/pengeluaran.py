from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from src.lib.auth_checks import check_is_confirmed
from src.models.models import Pengeluaran
from src import db
from flask import flash
pengeluaranBp = Blueprint("pengeluaran", __name__)


@pengeluaranBp.route("/pengeluaran", methods=["GET", "POST"])
@login_required
@check_is_confirmed
def pengeluaran():
    if request.method == "POST":
        jumlah = request.form.get("nominal")
        jumlah = int(''.join(filter(str.isdigit, jumlah)))
        tanggal = request.form.get("tanggal")
        keterangan = request.form.get("deskripsi")
        user_id = current_user.id

        existing_entry = Pengeluaran.query.filter_by(
            jumlah=jumlah, tanggal=tanggal, keterangan=keterangan, user_id=user_id).first()

        if existing_entry is None:
            new_entry = Pengeluaran(
                jumlah=jumlah, tanggal=tanggal, keterangan=keterangan, user_id=user_id)
            db.session.add(new_entry)
            db.session.commit()
            flash("Data berhasil ditambahkan", "success")
        else:
            flash("Pengeluaran sudah terdaftar", "danger")
    return render_template("dashboard/pengeluaran.html")
