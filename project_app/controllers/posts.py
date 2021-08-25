import os
from uuid import uuid4
from project_app import app
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename
# from project_app.models.post import Post
from project_app.models.user import User
from project_app.models.channel import Channel

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
    return render_template("dashboard.html", user= account_logged_in, all_users= all_users, all_channels= all_channels)

@app.route("/to_dashboard")
def to_dashboard():
    return redirect("/dashboard")


@app.route('/upload')
def upload():
    return render_template('upload.html')





def allowed_file(filename):
    print(filename)
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_EXTENSIONS']


@app.route("/uploads", methods = ['POST'])
def upload_file():
    if request.method == 'POST':
        print(request.files)
        if 'file' not in request.files:
            flash('No file part')
            return redirect('/upload')
        file = request.files['file']
        if file.filename == '':
            flash('No file selected')
            return redirect('/upload')
        print(file)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.static_folder, f"{app.config['UPLOAD_PATH']}/{filename}"))
            return redirect('/dashboard')
    return redirect('/dashboard')


@app.route('/uploads/<filename>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_PATH'], name)

