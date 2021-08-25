import os
from project_app import app
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename
# from project_app.models.post import Post
from project_app.models.user import User


UPLOAD_FOLDER = '/upload_folder/images'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])


@app.route("/dashboard")
def dashboard():
    if "account_logged_in" not in session:
        return redirect("/log_out")
    data = {
        "id" : session["account_logged_in"]
    }
    account_logged_in = User.get_one(data)
    all_users= User.get_all()
    all_channels= Channel.get_all_channels()
    return render_template("dashboard.html", user= account_logged_in, all_users= all_users, all_channels = all_channels)


@app.route('/upload')
def upload():
    return render_template('upload.html')


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/uploads", methods = ['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file', filename = filename))
    return redirect('/dashboard')

@app.route('/uploads/<filename>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_FOLDER'], name)