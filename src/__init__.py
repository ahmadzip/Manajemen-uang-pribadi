from decouple import config
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config.from_object(config("APP_SETTINGS"))

login_manager = LoginManager()
login_manager.init_app(app)
bcrypt = Bcrypt(app)
mail = Mail(app)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from src.routes.auth import auth_bp
from src.routes.views import dashboardBp
from src.routes.pemasukan import pemasukanBp
from src.routes.pengeluaran import pengeluaranBp

app.register_blueprint(auth_bp)
app.register_blueprint(dashboardBp)
app.register_blueprint(pemasukanBp)
app.register_blueprint(pengeluaranBp)

from .models.models import User

login_manager.login_view = "auth.login"
login_manager.login_message_category = "danger"

@login_manager.user_loader
def load_user(user_id):
    return User.query.filter(User.id == int(user_id)).first()
