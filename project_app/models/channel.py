from project_app.config.pymysqlconnections import connectToMySQL
from flask import flash
from project_app.models import post, user


class Channel:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
    
    @staticmethod
    def validate_channel(channel):
        is_valid = True
        if len(channel["name"]) == 0:
            flash("Channel name must be inputed", "name")
            is_valid = False
        elif len(channel["name"]) < 2:
            flash("Channel name must be 2 characters or longer", "name")
            is_valid = False
        return is_valid

    @classmethod
    def create_channel(cls, data):
        query = "INSERT INTO channels (name) VALUES (%(name)s);"
        new_channel_id = connectToMySQL("project").query_db(query, data)
        return new_channel_id

    @classmethod
    def add_user_to_channel(cls, data):
        query = "INSERT INTO channels_has_users (user_id, channel_id) VALUES (%(user_id)s, %(channel_id)s);"
        new_channel_users_id = connectToMySQL("project").query_db(query, data)
        return new_channel_users_id

    @classmethod
    def get_all_channels(cls):
        query= "SELECT * FROM channels;"
        results = connectToMySQL("project").query_db(query)
        all_channels= []
        for channel in results:
            all_channels.append(cls(channel))
        return all_channels

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM channels WHERE id = %(id)s;"
        results = connectToMySQL("project").query_db(query, data)
        return cls(results[0])


    @property
    def posts(self):
        data = {
            "channel_id" : self.id
        }
        return post.Post.get_all(data)

    @property
    def users(self):
        data = {
            "channel_id" : self.id
        }
        return user.User.get_all(data)

