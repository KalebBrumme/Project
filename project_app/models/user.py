from flask import flash
from project_app import app
from flask import render_template, redirect, request, session
from project_app.models.user import User
from flask_bcrypt import Bcrypt     
bcrypt = Bcrypt(app)

@app.route("/")
def login_page():
    return render_template("login.html")

@app.route("/register_user", methods=["POST"])
def register_user():
    if not User.validate_user(request.form):
        return redirect("/")
    pw_hash = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "birthday" : request.form["birthday"],
        "password" : pw_hash
    }
    user_id = User.save(data)
    session["account_logged_in"] = user_id
    return redirect("/dashboard")

@app.route("/login_user", methods=["POST"])
def login():
    data = {
        "email" : request.form["email"]
    }
    user_data= User.get_email(data)
    if not user_data:
        flash("Wrong email or password", "login")
        return redirect('/')
    if not bcrypt.check_password_hash(user_data.password, request.form["password"]):
        flash("Wrong password", "login")
        return redirect("/")
    session["account_logged_in"] = user_data.id
    return redirect("/dashboard")

@app.route("/log_out")
def log_out():
    session.clear()
    return redirect("/")