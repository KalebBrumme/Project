from project_app.config.pymysqlconnections import connectToMySQL
from flask import flash

class Post:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.like_count = data["like_count"]
        self.description = data["description"]
        self.user_id = data["user_id"]
        self.channel_id = data["channel_id"]
        self.image_id = data["image_id"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]

    @classmethod
    def get_all_users_posts(cls, data):
        query = "SELECT * FROM posts WHERE id = %(id)s"
        results = connectToMySQL("project").query_db(query, data)
        all_user_posts = []
        for row_db in results:
            user_post = cls(row_db)
            all_user_posts.append(user_post)
        return all_user_posts

    @classmethod
    def get_posts_channel(cls, data):
        query= "SELECT * FROM posts LEFT JOIN channels ON channel_id = channels.id WHERE channels.id= %(id)s;"
        results= connectToMySQL("project").query_db(query, data)
        channel_posts= []
        for row in results:
            post= cls(row)
            data= {
                "id" : row["channels.id"],
                "name" : row["name"],
                "created_at" : row["channelss.created_at"],
                "updated_at" : row["channelss.updated_at"]
            }
            channel_posts.append(post)
        return channel_posts
        