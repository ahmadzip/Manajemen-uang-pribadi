from flask import Blueprint, render_template, request
from flask_login import login_required, current_user
from src.lib.auth_checks import check_is_confirmed
from src.models.models import Pengeluaran, Saldo
from src import db
from flask import flash
from src.lib.forms import PengeluaranForm
pengeluaranBp = Blueprint("pengeluaran", __name__)


@pengeluaranBp.route("/pengeluaran", methods=["GET", "POST"])
@login_required
@check_is_confirmed
def pengeluaran():
    form = PengeluaranForm(request.form)
    if request.method == "POST":
        jumlah = request.form.get("nominal")
        jumlah = int(''.join(filter(str.isdigit, jumlah)))
        tanggal = request.form.get("tanggal")
        keterangan = request.form.get("keterangan")
        user_id = current_user.id
        existing_entry = Pengeluaran.query.filter_by(
            jumlah=jumlah, tanggal=tanggal, keterangan=keterangan, user_id=user_id).first()
        existing_saldo = Saldo.query.filter_by(user_id=user_id).first()
        if existing_saldo is not None:
            if existing_saldo.saldo < jumlah:
                flash("Saldo tidak cukup", "error")
                return render_template("dashboard/pengeluaran.html")
        if existing_entry is None:
            db.session.add(Pengeluaran(jumlah=jumlah, tanggal=tanggal,
                           keterangan=keterangan, user_id=user_id))
            if existing_saldo is None:
                db.session.add(
                    Saldo(tanggal=tanggal, saldo=jumlah, user_id=user_id))
            else:
                existing_saldo.saldo -= jumlah
            db.session.commit()
            flash("Data berhasil ditambahkan", "success")
        else:
            flash("Pengeluaran sudah terdaftar", "error")
    get_pengeluaran = Pengeluaran.query.filter_by(
        user_id=current_user.id).all()
    for item in get_pengeluaran:
        item.type = "pengeluaran"
    short_pengeluaran = sorted(
        get_pengeluaran, key=lambda x: x.tanggal, reverse=True)
    return render_template("dashboard/pengeluaran.html", form=form, gabungkan=short_pengeluaran)
