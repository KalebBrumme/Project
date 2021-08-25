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

    @classmethod
    def get_all_users_posts(cls, data):
        query = "SELECT * FROM posts WHERE id = %(id)s"
        results = connectToMySQL("project").query_db(query, data)
        all_user_posts = []
        for row_db in results:
            user_post = cls(row_db)
            all_user_posts.append(user_post)
        return all_user_posts