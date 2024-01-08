from datetime import datetime
from flask_login import UserMixin
from src import bcrypt, db


class User(UserMixin, db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(122), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    is_admin = db.Column(db.Boolean, nullable=False, default=False)
    is_confirmed = db.Column(db.Boolean, nullable=False, default=False)
    confirmed_on = db.Column(db.DateTime, nullable=True)

    def __init__(self, email, password, is_admin=False, is_confirmed=False, confirmed_on=None):
        self.email = email
        self.password = bcrypt.generate_password_hash(password)
        self.created_on = datetime.now()
        self.is_admin = is_admin
        self.is_confirmed = is_confirmed
        self.confirmed_on = confirmed_on

    def __repr__(self):
        return f"<email {self.email}>"


class Pemasukan(db.Model):
    __tablename__ = "pemasukan"
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.DateTime, nullable=False)
    keterangan = db.Column(db.String(255), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship("User", backref=db.backref("pemasukan", lazy=True))

    def __init__(self, tanggal, keterangan, jumlah, user_id):
        self.tanggal = tanggal
        self.keterangan = keterangan
        self.jumlah = jumlah
        self.user_id = user_id
        self.created_on = datetime.now()

    def __repr__(self):
        return f"<keterangan {self.keterangan}>"


class Pengeluaran(db.Model):
    __tablename__ = "pengeluaran"
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.DateTime, nullable=False)
    keterangan = db.Column(db.String(255), nullable=False)
    jumlah = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship(
        "User", backref=db.backref("pengeluaran", lazy=True))

    def __init__(self, tanggal, keterangan, jumlah, user_id):
        self.tanggal = tanggal
        self.keterangan = keterangan
        self.jumlah = jumlah
        self.user_id = user_id
        self.created_on = datetime.now()

    def __repr__(self):
        return f"<keterangan {self.keterangan}>"


class Saldo(db.Model):
    __tablename__ = "saldo"
    id = db.Column(db.Integer, primary_key=True)
    tanggal = db.Column(db.DateTime, nullable=False)
    saldo = db.Column(db.Integer, nullable=False)
    created_on = db.Column(db.DateTime, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)
    user = db.relationship(
        "User", backref=db.backref("saldo", lazy=True))

    def __init__(self, tanggal, saldo, user_id):
        self.tanggal = tanggal
        self.saldo = saldo
        self.user_id = user_id
        self.created_on = datetime.now()

    def __repr__(self):
        return f"<saldo {self.saldo}>"
