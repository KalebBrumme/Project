import os
from uuid import uuid4
from project_app import app
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename
from project_app.models.post import Post
from project_app.models.user import User
from project_app.models.image import Image
from project_app.models.channel import Channel






@app.route('/upload')
def upload():
    return render_template('upload.html')

def generate_file_name():
    return f"{session['account_logged_in']}_{uuid4()}"


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_EXTENSIONS']


@app.route("/uploads", methods = ['POST'])
def upload_file():
    if "account_logged_in" not in session:
        return redirect("/log_out")
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
            filename = generate_file_name()
            data = {
                "user_id" : session['account_logged_in'],
                "filename" : filename
            }
            Image.add_image(data)
            file.save(os.path.join(app.static_folder, f"{app.config['UPLOAD_PATH']}/{filename}"))
            return redirect('/dashboard')
    return redirect('/dashboard')


@app.route('/uploads/<filename>')
def download_file(name):
    return send_from_directory(app.config['UPLOAD_PATH'], name)




@app.route('/profile_page')
def user_profile():
    user_data = {
        "id": session['account_logged_in']
    }
    all_user_posts = Post.get_all_users_posts(user_data)
    return render_template('profile_page.html', all_user_posts = all_user_posts)

@app.route("/delete/<id>")
def delete(id):
    data= {
        "id": id
    }
    Post.delete(data)
    return redirect("/dashboard")

@app.route("/like_post/<id>")
def like_post(id):
    data= {
        "id": id
    }
    Post.like_post(data)
    return redirect("/dashboard")

@app.route("/unlike_post/<id>")
def unlike_post(id):
    data= {
        "id": id
    }
    Post.unlike_post(data)