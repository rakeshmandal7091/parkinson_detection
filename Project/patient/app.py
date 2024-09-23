from flask import Flask
from config import Config
from models import db, AppUser
from routes import patient_routes
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

db.init_app(app)

migrate = Migrate(app, db)  # Initialize Flask-Migrate

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'patient_routes.login'

@login_manager.user_loader
def load_user(user_id):
    return AppUser.query.get(int(user_id))

with app.app_context():
    db.create_all()

app.register_blueprint(patient_routes)

if __name__ == '__main__':
    app.run(port=5002)
