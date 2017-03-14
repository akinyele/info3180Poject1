from flask import Flask
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)



# Config Values
USERNAME = 'admin'
PASSWORD = 'password123'

# SECRET_KEY is needed for session security, the flash() method in this case stores the message in a session
SECRET_KEY = 'Sup3r$3cretkey'
UPLOAD_FOLDER = './app/static/uploads' 
 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config.from_object(__name__)


app.config['SECRET_KEY'] = "hello world"
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://Project 1:C0de@localhost/project1"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True # added just to suppress a warning


db = SQLAlchemy(app)

# Flask-Login login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


from app import views
