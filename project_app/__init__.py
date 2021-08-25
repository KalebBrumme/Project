from flask import Flask
app = Flask(__name__)
app.secret_key = "shhhhhh"
UPLOAD_FOLDER = 'upload_folder/images'
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_PATH'] = UPLOAD_FOLDER
app.config['UPLOAD_EXTENSIONS'] = ALLOWED_EXTENSIONS
