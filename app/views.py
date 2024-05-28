import os

from flask import render_template, request, redirect, url_for, session, flash, Blueprint, send_from_directory
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

main = Blueprint("main", __name__)

admin_username = os.getenv('ADMIN_USERNAME')
admin_password = os.getenv('ADMIN_PASSWORD')


@main.route("/")
def home():
    return render_template("home.html")

@main.route("/downloads")
def downloads():
    return render_template("downloads.html")

@main.route("/about")
def about():
    return render_template("about.html")

UPLOAD_FOLDER = 'static/downloads'
UPLOAD_FOLDER_ABSOLUTE = os.path.join(os.path.dirname(os.path.abspath(__file__)), UPLOAD_FOLDER)

# Ensure the upload directory exists
os.makedirs(UPLOAD_FOLDER_ABSOLUTE, exist_ok=True)

# Function to check if user is authenticated as admin
def login_required_admin(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        print(list(session))
        if 'username' not in session or 'password' not in session or \
           session['username'] != admin_username or \
            admin_password != session['password']:
            print("sjhsjh kyu ayya be")
            return redirect(url_for('main.login_admin'))
        return f(*args, **kwargs)
    return decorated_function

# Login page for admin
@main.route('/login_admin', methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        print(username,password,admin_password,admin_username)
        if username == admin_username and admin_password == password:
            session['username'] = username
            session['password'] = password
            print("indie")
            return redirect(url_for('main.upload_file'))
    return '''
    <form method="post">
        <p><input type=text name=username>
        <p><input type=password name=password>
        <p><input type=submit value=Login>
    </form>
    '''

# Logout route for admin
@main.route('/logout_admin')
def logout_admin():
    session.pop('username', None)
    session.pop('password', None)
    return redirect(url_for('login_admin'))


@main.route('/upload', methods=['GET', 'POST'])
@login_required_admin
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            filename = secure_filename(file.filename)
            # Create the UPLOAD_FOLDER directory if it doesn't exist
            os.makedirs(UPLOAD_FOLDER, exist_ok=True)
            file.save(os.path.join(UPLOAD_FOLDER, filename))
            return redirect(url_for('main.uploaded_file', filename=filename))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    '''


@main.route('/uploads/<filename>')
def uploaded_file(filename):
    return f"{filename} uploaded"