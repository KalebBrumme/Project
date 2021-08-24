from project_app import app
from flask import render_template, request, redirect, session
# from project_app.models.post import Post
from project_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route("/dashboard")
def dashboard():
    if "account_logged_in" not in session:
        return redirect("/log_out")
    data = {
        "id" : session["account_logged_in"]
    }
    account_logged_in = User.get_one(data)
    all_users= User.get_all()
    return render_template("dashboard.html", user= account_logged_in, all_users= all_users)
    
