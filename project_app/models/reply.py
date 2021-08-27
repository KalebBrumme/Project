from project_app.config.pymysqlconnections import connectToMySQL




class Reply:
    def __init__(self, data):
        self.id = data['id']
        self.replies = data['replies']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.post_id = data['post_id']
        self.user_id = data['user_id']

    @classmethod
    def get_all(cls, data):
        query = "SELECT * FROM replies WHERE id = %(id)s;"
        results = connectToMySQL('project').query_db(query, data)
        if results:
            return cls(results[0])
        else:
            return results

    @classmethod
    def make_reply(cls, data):
        query = "INSERT INTO replies (replies, post_id, user_id) VALUES (%(replies)s, %(post_id)s, %(user_id)s);"
        new_reply = connectToMySQL('project').query_db(query, data)
        return new_reply
