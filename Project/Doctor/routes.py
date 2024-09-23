from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename
import os
from io import BytesIO
from fpdf import FPDF
from models import db, AppUser
from flask import get_flashed_messages

# Initialize Blueprint
doctor_routes = Blueprint('doctor_routes', __name__)

# Define upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route
@doctor_routes.route('/')
def home():
    return render_template('index.html')

# Login route
@doctor_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = AppUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('doctor_routes.dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', error=get_flashed_messages())

# Signup route
@doctor_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        position = request.form.get('position')
        qualification = request.form.get('qualification')
        age = request.form.get('age')

        if AppUser.query.filter_by(username=username).first():
            flash('Username already exists')
        else:
            new_user = AppUser(
                username=username,
                name=name,
                email=email,
                position=position,
                qualification=qualification,
                age=age
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!')
            return redirect(url_for('doctor_routes.login'))
    return render_template('signup.html')

# Logout route
@doctor_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('doctor_routes.login'))

# Dashboard route
@doctor_routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Profile route (updated)
@doctor_routes.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        position = request.form.get('position')
        qualification = request.form.get('qualification')
        age = request.form.get('age')
        
        # Handle profile picture upload
        profile_pic = request.files.get('profile_pic')
        if profile_pic and allowed_file(profile_pic.filename):
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            filename = current_user.profile_pic  # Keep existing profile picture if no new file

        # Update user details
        current_user.name = name
        current_user.email = email
        current_user.position = position
        current_user.qualification = qualification
        current_user.age = age
        current_user.profile_pic = filename
        db.session.commit()

        flash('Profile updated successfully!')
        return redirect(url_for('doctor_routes.profile'))

    return render_template('profile.html', user=current_user)

# API route for patient data
@doctor_routes.route('/api/patient-data', methods=['POST'])
def receive_patient_data():
    data = request.json
    # Process or save the patient data as needed
    print("Received data from patient application:", data)
    # Optionally save the received data in the database for later use
    return jsonify({"status": "success", "message": "Data received by doctor application"}), 200

# Generate report route
@doctor_routes.route('/generate-report', methods=['POST'])
@login_required
def generate_report():
    # Example data, this should be replaced with actual patient data
    data = {"input1": "value1", "input2": "value2", "input3": "value3"}

    # Initialize PDF document
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add data to the PDF
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    
    # Create a BytesIO stream to hold the PDF in memory
    output = BytesIO()
    pdf.output(output)
    output.seek(0)

    # Optionally send the PDF back to the patient or save to file
    # For now, send the file as a response
    return send_file(output, as_attachment=True, download_name="report.pdf")
from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify, send_file
from flask_login import login_required, current_user, login_user, logout_user
from werkzeug.utils import secure_filename
import os
from io import BytesIO
from fpdf import FPDF
from models import db, AppUser
from flask import get_flashed_messages

# Initialize Blueprint
doctor_routes = Blueprint('doctor_routes', __name__)

# Define upload folder and allowed extensions
UPLOAD_FOLDER = 'static/uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Function to check allowed file extensions
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

# Home route
@doctor_routes.route('/')
def home():
    return render_template('index.html')

# Login route
@doctor_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = AppUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('doctor_routes.dashboard'))
        else:
            flash('Invalid username or password')
    return render_template('login.html', error=get_flashed_messages())

# Signup route
@doctor_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        name = request.form['name']
        email = request.form['email']
        position = request.form.get('position')
        qualification = request.form.get('qualification')
        age = request.form.get('age')

        if AppUser.query.filter_by(username=username).first():
            flash('Username already exists')
        else:
            new_user = AppUser(
                username=username,
                name=name,
                email=email,
                position=position,
                qualification=qualification,
                age=age
            )
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!')
            return redirect(url_for('doctor_routes.login'))
    return render_template('signup.html')

# Logout route
@doctor_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('doctor_routes.login'))

# Dashboard route
@doctor_routes.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')

# Profile route (updated)
@doctor_routes.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        position = request.form.get('position')
        qualification = request.form.get('qualification')
        age = request.form.get('age')
        
        # Handle profile picture upload
        profile_pic = request.files.get('profile_pic')
        if profile_pic and allowed_file(profile_pic.filename):
            filename = secure_filename(profile_pic.filename)
            profile_pic.save(os.path.join(UPLOAD_FOLDER, filename))
        else:
            filename = current_user.profile_pic  # Keep existing profile picture if no new file

        # Update user details
        current_user.name = name
        current_user.email = email
        current_user.position = position
        current_user.qualification = qualification
        current_user.age = age
        current_user.profile_pic = filename
        db.session.commit()

        flash('Profile updated successfully!')
        return redirect(url_for('doctor_routes.profile'))

    return render_template('profile.html', user=current_user)

# API route for patient data
@doctor_routes.route('/api/patient-data', methods=['POST'])
def receive_patient_data():
    data = request.json
    # Process or save the patient data as needed
    print("Received data from patient application:", data)
    # Optionally save the received data in the database for later use
    return jsonify({"status": "success", "message": "Data received by doctor application"}), 200

# Generate report route
@doctor_routes.route('/generate-report', methods=['POST'])
@login_required
def generate_report():
    # Example data, this should be replaced with actual patient data
    data = {"input1": "value1", "input2": "value2", "input3": "value3"}

    # Initialize PDF document
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Add data to the PDF
    for key, value in data.items():
        pdf.cell(200, 10, txt=f"{key}: {value}", ln=True)
    
    # Create a BytesIO stream to hold the PDF in memory
    output = BytesIO()
    pdf.output(output)
    output.seek(0)

    # Optionally send the PDF back to the patient or save to file
    # For now, send the file as a response
    return send_file(output, as_attachment=True, download_name="report.pdf")
