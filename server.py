from project_app import app
from project_app.controllers import users, posts, channels

if __name__ == "__main__":
    app.run(debug=True)