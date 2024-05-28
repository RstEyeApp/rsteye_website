from flask import render_template, request, redirect, url_for, session, flash, Blueprint, send_from_directory
from werkzeug.utils import secure_filename
import os

main = Blueprint("main", __name__)


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

@main.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # If the user does not select a file, the browser submits an
        # empty file without a filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file:
            try:
                filename = secure_filename(file.filename)
                file.save(os.path.join(UPLOAD_FOLDER_ABSOLUTE, filename))
                uploaded_file_url = url_for('main.uploaded_file', filename=filename)
                return redirect(uploaded_file_url)
            except Exception as e:
                print("Error saving file:", e)
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