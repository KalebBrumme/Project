from project_app.config.pymysqlconnections import connectToMySQL
from flask import flash
from project_app.models.user import User

class Channel:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.user_id = data["user_id"]
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
        query = "INSERT INTO channels (name, user_id) VALUES (%(name)s, %(user_id)s);"
        new_channel_id = connectToMySQL("project").query_db(query, data)
        return new_channel_id

    @classmethod
    def get_all_channels(cls):
        query= "SELECT * FROM channels;"
        results = connectToMySQL("project").query_db(query)
        all_channels= []
        for channel in results:
            all_channels.append(cls(channel))
        return all_channels