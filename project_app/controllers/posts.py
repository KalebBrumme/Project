from project_app import app
from flask import render_template, request, redirect, session
# from project_app.models.post import Post
from project_app.models.user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)


