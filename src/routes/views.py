from flask import Blueprint, render_template, jsonify, flash, redirect, url_for, request
from flask_login import login_required
from src.lib.auth_checks import check_is_confirmed
from src import app, db
from flask_login import current_user
from src.models.models import Pemasukan, Pengeluaran, Saldo
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta
from src.lib.forms import EditPemasukanForm
dashboardBp = Blueprint("dashboard", __name__)


@dashboardBp.route("/")
@login_required
@check_is_confirmed
def home():
    iduser = current_user.id
    pengeluaran = Pengeluaran.query.filter_by(user_id=iduser).all()
    pemasukan = Pemasukan.query.filter_by(user_id=iduser).all()
    saldouser = Saldo.query.filter_by(user_id=iduser).first()

    for item in pemasukan + pengeluaran:
        item.type = "pemasukan" if isinstance(
            item, Pemasukan) else "pengeluaran"

    gabungkan = sorted(pemasukan + pengeluaran,
                       key=lambda x: x.tanggal, reverse=True)

    today = datetime.now().date()
    yesterday = today - timedelta(days=1)
    the_day_after_tomorrow = today + timedelta(days=-2)
    pengeluaran_hari_ini = 0
    pengeluaran_kemarin = 0
    pemasukan_hari_ini = 0
    pengeluaran_lusa = 0
    saldo = saldouser.saldo if saldouser else 0

    for pengeluarann in pengeluaran:
        if pengeluarann.tanggal.date() == today:
            pengeluaran_hari_ini += pengeluarann.jumlah

    for pengeluarann in pengeluaran:
        if pengeluarann.tanggal.date() == yesterday:
            pengeluaran_kemarin += pengeluarann.jumlah

    for pemasukann in pemasukan:
        if pemasukann.tanggal.date() == today:
            pemasukan_hari_ini += pemasukann.jumlah

    for pengeluarannn in pengeluaran:
        if pengeluarannn.tanggal.date() == the_day_after_tomorrow:
            pengeluaran_lusa += pengeluarannn.jumlah

    pemasukan_kermain = 0
    pemasukan_tanpa_hari_ini = 0
    pengeluaran_tanpa_hari_ini = 0
    saldokemarin = 0

    for pembayaran in pemasukan:
        if pembayaran.tanggal.date() == yesterday:
            pemasukan_kermain += pembayaran.jumlah

    for pemasukann in pemasukan:
        if pemasukann.tanggal.date() != today:
            pemasukan_tanpa_hari_ini += pemasukann.jumlah

    for pengeluarann in pengeluaran:
        if pengeluarann.tanggal.date() != today:
            pengeluaran_tanpa_hari_ini += pengeluarann.jumlah

    saldokemarin = pemasukan_tanpa_hari_ini - pengeluaran_tanpa_hari_ini

    saldo_kemarin_percent = 0 if saldokemarin == 0 else round(
        (saldo - saldokemarin) / saldokemarin * 100)

    pengeluaran_kemarin_percent = 0 if pengeluaran_kemarin == 0 else round(
        (pengeluaran_hari_ini - pengeluaran_kemarin) / pengeluaran_kemarin * 100)

    pemasukan_kemarin_percent = 0 if pemasukan_kermain == 0 else round(
        (pemasukan_hari_ini - pemasukan_kermain) / pemasukan_kermain * 100)

    pengeluaran_kemarin_luas_percent = 0 if pengeluaran_lusa == 0 else round(
        (pengeluaran_kemarin - pengeluaran_lusa) / pengeluaran_lusa * 100)

    days_of_week = ['Senin', 'Selasa', 'Rabu',
                    'Kamis', 'Jumat', 'Sabtu', 'Minggu']
    current_date = datetime.now().date()
    start_of_week = current_date - timedelta(days=current_date.weekday())
    daily_pemasukan_data = {day: 0 for day in days_of_week}
    daily_pengeluaran_data = {day: 0 for day in days_of_week}

    for i in range(7):
        day = start_of_week + timedelta(days=i)
        for item in gabungkan:
            if item.tanggal.date() == day:
                if item.type == 'pemasukan':
                    daily_pemasukan_data[days_of_week[i]] += item.jumlah
                else:
                    daily_pengeluaran_data[days_of_week[i]] += item.jumlah

    daily_pemasukan_data_list = list(daily_pemasukan_data.values())
    daily_pengeluaran_data_list = list(daily_pengeluaran_data.values())
    return render_template("dashboard/index.html", gabungkan=gabungkan, saldo=saldo, pengeluaran_hari_ini=pengeluaran_hari_ini, pemasukan_hari_ini=pemasukan_hari_ini, pengeluaran_kemarin=pengeluaran_kemarin,
                           saldo_kemarin_percent=saldo_kemarin_percent, pengeluaran_kemarin_percent=pengeluaran_kemarin_percent, pemasukan_kemarin_percent=pemasukan_kemarin_percent, pengeluaran_kemarin_luas_percent=pengeluaran_kemarin_luas_percent,
                           daily_pemasukan_data_list=daily_pemasukan_data_list, daily_pengeluaran_data_list=daily_pengeluaran_data_list)


@dashboardBp.route("/delete/<int:id>", methods=["DELETE"])
@login_required
@check_is_confirmed
def delete(id):
    pemasukan = Pemasukan.query.filter_by(id=id).first()
    pengeluaran = Pengeluaran.query.filter_by(id=id).first()
    saldo = Saldo.query.filter_by().first()
    if pemasukan:
        db.session.delete(pemasukan)
        saldo.saldo = saldo.saldo - pemasukan.jumlah
    elif pengeluaran:
        saldo.saldo = saldo.saldo - pengeluaran.jumlah
        db.session.delete(pengeluaran)
    else:
        flash("Data tidak ditemukan", "danger")
        return {'status': 'failed'}
    db.session.commit()
    flash("Data berhasil dihapus", "success")
    return {'status': 'success'}


@dashboardBp.route("/edit/<int:id>", methods=["GET", "POST"])
@login_required
@check_is_confirmed
def edit(id):
    pemasukan = Pemasukan.query.filter_by(id=id).first()
    pengeluaran = Pengeluaran.query.filter_by(id=id).first()
    if request.method == "POST":
        jumlah = request.form.get("nominal")
        jumlah = int(''.join(filter(str.isdigit, jumlah)))
        tanggal = request.form.get("tanggal")
        keterangan = request.form.get("keterangan")
        if pemasukan:
            pemasukan.jumlah = jumlah
            pemasukan.tanggal = tanggal
            pemasukan.keterangan = keterangan
            db.session.commit()
            flash("Data berhasil diubah", "success")
        elif pengeluaran:
            pengeluaran.jumlah = jumlah
            pengeluaran.tanggal = tanggal
            pengeluaran.keterangan = keterangan
            db.session.commit()
            flash("Data berhasil diubah", "success")
        else:
            flash("Data tidak ditemukan", "danger")
    elif request.method == "GET":
        form = EditPemasukanForm(request.form)
        if pemasukan:
            return render_template("dashboard/edit.html", form=form, data=pemasukan)
        elif pengeluaran:
            return render_template("dashboard/edit.html", form=form, data=pengeluaran)
        else:
            flash("Data tidak ditemukan", "danger")
    else:
        flash("Data tidak ditemukan", "danger")
    return redirect(url_for("dashboard.home"))
