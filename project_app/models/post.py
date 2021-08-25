from project_app.config.pymysqlconnections import connectToMySQL
from flask import flash

class Post:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.like_count = data["like_count"]
        self.description = data["description"]
        self.user_id = data["user_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.posts= []