import os
from uuid import uuid4
from project_app import app
from flask import render_template, request, redirect, session, flash, url_for, send_from_directory
from werkzeug.utils import secure_filename
from project_app.models.post import Post
from project_app.models.user import User
from project_app.models.image import Image
from project_app.models.channel import Channel
from project_app.models.reply import Reply



def generate_file_name():
    return f"{session['account_logged_in']}_{uuid4()}"


def allowed_file(filename):
    return '.' in filename and \
        filename.rsplit('.', 1)[1].lower() in app.config['UPLOAD_EXTENSIONS']


@app.route("/uploads/<id>", methods = ['POST'])
def upload_file(id):
    channel_id= id
    if "account_logged_in" not in session:
        return redirect("/log_out")
    if request.method == 'POST':
        if 'file' not in request.files:
            return redirect(f"/go_to_channel/{ channel_id }")
        file = request.files['file']
        if file.filename == '':
            return redirect(f"/go_to_channel/{ channel_id }")
        if file and allowed_file(file.filename):
            filename = generate_file_name()
            data = {
                "user_id" : session['account_logged_in'],
                "filename" : filename
            }
            image_id = Image.add_image(data)
            file.save(os.path.join(app.static_folder, f"{app.config['UPLOAD_PATH']}/{filename}"))
            data = {
                "name" : request.form['name'],
                "description" : request.form['description'],
                "user_id" : session['account_logged_in'],
                "channel_id" : id,
                "image_id" : image_id
            }
            Post.save_post(data)
            return redirect(f"/go_to_channel/{ channel_id }")
    return redirect(f"/go_to_channel/{ channel_id }")

@app.route('/profile_page')
def user_profile():
    user_data = {
        "id": session['account_logged_in']
    }
    account_logged_in = User.get_one(user_data)
    all_users= User.all()
    all_user_posts = Post.get_all_users_posts(user_data)
    return render_template('profile_page.html', user= account_logged_in, all_user_posts = all_user_posts, all_users= all_users)


@app.route('/user_settings/<int:id>')
def user_settings():
    pass



@app.route("/delete/<id>")
def delete(id):
    data= {
        "id": id
    }
    Post.delete(data)

    return redirect(request.referrer)

@app.route("/like_post/<id>")
def like_post(id):
    data= {
        "id": id
    }
    Post.like_post(data)
    return redirect(request.referrer)

@app.route('/add_reply/<int:id>', methods=['POST'])
def add_reply(id):
    data = {
        "user_id": session['account_logged_in'],
        "replies": request.form['reply'],
        "post_id": id
    }
    Reply.make_reply(data)
    return redirect(request.referrer)