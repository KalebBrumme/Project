from types import MethodDescriptorType
from project_app import app
from flask import render_template, request, redirect, session
from project_app.models.channel import Channel
from project_app.models.user import User
from project_app.models.post import Post
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

# @app.route("/dashboard")
# def dashboard():
#     if "account_logged_in" not in session:
#         return redirect("/log_out")
#     data = {
#         "id" : session["account_logged_in"]
#     }
#     account_logged_in = User.get_one(data)
#     all_users= User.get_all()
#     all_channels= Channel.get_all_channels()
#     return render_template("dashboard.html", user= account_logged_in, all_users= all_users, all_channels= all_channels)

@app.route("/add_channel", methods=["POST"])
def add_channel():
    if not Channel.validate_channel(request.form):
        return redirect("/dashboard")
    data1 = {
        "name": request.form["name"]
    }
    Channel.create_channel(data1)
    # data2= {
    #     "channel_id" : channel_id,
    #     "user_id" : session["account_logged_in"]
    # }
    # Channel.add_user_to_channel(data2)
    return redirect("/dashboard")

@app.route("/go_to_channel/<id>")
def go_to_channel(id):
    data= {
        "id" : id
    }
    main_data= {
        "id" : session["account_logged_in"]
    }
    one_channel= Post.get_posts_channel(data)
    account_logged_in = User.get_one(main_data)
    all_users= User.get_all()
    all_channels= Channel.get_all_channels()
    return render_template("channel.html", user= account_logged_in, all_users= all_users, one_channel= one_channel, all_channels= all_channels)

