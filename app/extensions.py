from flask_assets import Environment
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail
from flask_rq2 import RQ
from flask_travis import Travis

assets = Environment()
bcrypt = Bcrypt()
lm = LoginManager()
mail = Mail()
rq = RQ()
travis = Travis()
