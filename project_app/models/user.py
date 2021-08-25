from project_app.config.pymysqlconnections import connectToMySQL
from flask import flash

import re  

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    def __init__(self, data):
        self.id= data["id"]
        self.first_name= data["first_name"]
        self.last_name= data["last_name"]
        self.email= data["email"]
        self.birthday= data["birthday"]
        self.password= data["password"]
        self.created_at= data["created_at"]
        self.updated_at= data["updated_at"]
    
    @staticmethod
    def validate_user(user):
        is_valid = True
        if len(user["first_name"]) < 2:
            flash("First name must be at least two characters", "first_name")
            is_valid = False
        if len(user["last_name"]) < 2:
            flash("Last name must be at least two characters", "last_name")
            is_valid = False
        if User.get_email({"email": user["email"]}):
            flash("Email already exists!", "email")
            is_valid = False
        if not EMAIL_REGEX.match(user["email"]): 
            flash("Invalid email address", "email")
            is_valid = False
        if len(user["birthday"]) == 0:
            flash("Birthday must be inputed", "birthday")
            is_valid = False
        if len(user["password"]) < 8:
            flash("Password must be at least eight characters", "password")
            is_valid = False
        if user["password"] != user["password_confirmation"]:
            flash("Passwords do not match", "password_confirmation")
            is_valid = False
        return is_valid

    @classmethod
    def get_email(cls, data):
        query= "SELECT * FROM users WHERE email = %(email)s;"
        results= connectToMySQL("project").query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results= connectToMySQL("project").query_db(query, data)
        return cls(results[0])

    @classmethod
    def save(cls, data):
        query= "INSERT INTO users (first_name, last_name, email, birthday, password) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(birthday)s, %(password)s);"
        return connectToMySQL("project").query_db(query, data)

    @classmethod
    def get_all(cls):
        query= "SELECT * FROM users;"
        results = connectToMySQL("project").query_db(query)
        all_users= []
        for user in results:
            all_users.append(cls(user))
        return all_users
    
    
