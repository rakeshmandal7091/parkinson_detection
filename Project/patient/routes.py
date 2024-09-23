from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from models import db, AppUser
from flask_login import login_user, logout_user, current_user, login_required
import requests
import pdfplumber  # To extract text from PDFs
from PIL import Image
import pytesseract  # For OCR on images

patient_routes = Blueprint('patient_routes', __name__)

@patient_routes.route('/')
def home():
    return render_template('index.html')

@patient_routes.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = AppUser.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for('patient_routes.dashboard'))
        else:
            flash('Invalid username or password', 'error')  # Flash message with category
    return render_template('login.html')

@patient_routes.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if AppUser.query.filter_by(username=username).first():
            flash('Username already exists', 'error')  # Flash message with category
        else:
            new_user = AppUser(username=username)
            new_user.set_password(password)
            db.session.add(new_user)
            db.session.commit()
            flash('Account created successfully!', 'success')  # Flash message with category
            return redirect(url_for('patient_routes.login'))
    return render_template('signup.html')

@patient_routes.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('patient_routes.login'))

@patient_routes.route('/dashboard')
@login_required
def dashboard():
    # Placeholder doctor data
    doctors = [
        {"id": 1, "name": "Dr. John Doe", "position": "Cardiologist", "image": "placeholder.jpg"},
        {"id": 2, "name": "Dr. Jane Smith", "position": "Neurologist", "image": "placeholder.jpg"},
        {"id": 3, "name": "Dr. Alan Brown", "position": "Orthopedic", "image": "placeholder.jpg"},
    ]
    return render_template('dashboard.html', doctors=doctors)

@patient_routes.route('/predict', methods=['GET', 'POST'])
@login_required
def predict():
    if request.method == 'POST':
        data = request.form.to_dict()
        # Send data to doctor application
        return jsonify({"status": "success", "message": "Data sent to the doctor"}), 200
    return render_template('predict.html')

@patient_routes.route('/upload-file', methods=['POST'])
@login_required
def upload_file():
    if 'fileUpload' not in request.files:
        return jsonify({"status": "error", "message": "No file uploaded"}), 400

    file = request.files['fileUpload']

    if file.filename.endswith('.pdf'):
        # Handle PDF files
        with pdfplumber.open(file) as pdf:
            text = "\n".join(page.extract_text() for page in pdf.pages)
            values = extract_values_from_text(text)
    elif file.filename.lower().endswith(('.png', '.jpg', '.jpeg')):
        # Handle image files
        image = Image.open(file)
        text = pytesseract.image_to_string(image)
        values = extract_values_from_text(text)
    else:
        return jsonify({"status": "error", "message": "Unsupported file type"}), 400

    return jsonify({"status": "success", "values": values})

def extract_values_from_text(text):
    # Placeholder function to parse the text and extract 22 values
    # You need to implement this based on the file content and format
    # For now, just return a list with 22 dummy values
    values = text.split()[:22]  # Example of extracting first 22 words
    return values

@patient_routes.route('/send-data-to-doctor', methods=['POST'])
@login_required
def send_data_to_doctor():
    doctor_id = request.form.get('doctor_id')
    # Assuming user data is sent as JSON
    data = {
        'doctor_id': doctor_id,
        'user_data': request.form.to_dict()  # Adjust as needed
    }
    url = "http://localhost:5001/api/patient-data"  # Adjust the URL to doctor app
    response = requests.post(url, json=data)
    return jsonify(response.json())
