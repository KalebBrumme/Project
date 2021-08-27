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
        query = "SELECT * FROM replies WHERE post_id = %(id)s;"
        results = connectToMySQL('project').query_db(query, data)
        replies = []
        if results:
            for row in results:
                replies.append(cls(row))
            return replies
        else:
            return results

    @classmethod
    def make_reply(cls, data):
        query = "INSERT INTO replies (replies, post_id, user_id) VALUES (%(replies)s, %(post_id)s, %(user_id)s);"
        return connectToMySQL('project').query_db(query, data)

