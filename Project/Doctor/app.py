from flask import Flask
from config import Config
from models import db, AppUser
from routes import doctor_routes
from flask_login import LoginManager
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database
db.init_app(app)

# Initialize Flask-Migrate for handling migrations
migrate = Migrate(app, db)

# Setup Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'doctor_routes.login'

# User loader callback for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return AppUser.query.get(int(user_id))

# Ensure tables are created in the database
with app.app_context():
    db.create_all()  # This creates the tables when the app is run

# Register blueprint for doctor-related routes
app.register_blueprint(doctor_routes)

# Start the Flask application
if __name__ == '__main__':
    app.run(port=5001)
