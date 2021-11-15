import project_app
from project_app.config.pymysqlconnections import connectToMySQL
from flask import flash
from project_app.models.user import User
from project_app.models.channel import Channel
from project_app.models.image import Image
from project_app.models.reply import Reply

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
        query = "SELECT * FROM posts WHERE user_id = %(id)s"
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
                "created_at" : row["channels.created_at"],
                "updated_at" : row["channels.updated_at"]
            }
            channel_posts.append(post)
        return channel_posts


    @classmethod
    def save_post(cls, data):
        query = "INSERT INTO posts (name, description, user_id, image_id, channel_id) VALUES (%(name)s, %(description)s, %(user_id)s, %(image_id)s, %(channel_id)s);"
        return connectToMySQL('project').query_db(query, data)


    @classmethod
    def get_all(cls, data):
        query= "SELECT * FROM posts WHERE channel_id = %(channel_id)s ORDER BY created_at DESC;"
        results = connectToMySQL("project").query_db(query, data)
        return [cls(row) for row in results]
    
    @property
    def posted_by(self):
        data = {
            'id' : self.user_id
        }
        return User.get_one(data)

    @property
    def channel(self):
        data = {
            'id' : self.channel_id
        }
        return Channel.get_one(data)

    @property
    def image(self):
        data = {
            'id' : self.image_id
        }
        return Image.get_one(data)

    @property
    def replies(self):
        data = {
            'id' : self.id
        }
        return Reply.get_all(data)

    @classmethod
    def delete(cls, data):
        query= "DELETE FROM posts WHERE id = %(id)s;"
        connectToMySQL("project").query_db(query, data)

    @classmethod
    def like_post(cls, data):
        query = "UPDATE posts SET like_count= like_count + 1 WHERE id= %(id)s;"
        connectToMySQL("project").query_db(query, data)
        return data["id"]

