from project_app.config.pymysqlconnections import connectToMySQL
from flask import flash



class Image:
    def __init__(self, data):
        self.id = data['id']
        self.link = data['link']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def add_image(cls, data):
        query = "INSERT INTO images (link, user_id) VALUES (%(filename)s, %(user_id)s);" #link should be filename
        return connectToMySQL('project').query_db(query, data)


    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM images WHERE id = %(id)s;"
        results = connectToMySQL('project').query_db(query, data)
        return cls(results[0])