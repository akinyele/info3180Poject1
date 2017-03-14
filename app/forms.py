from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, RadioField, validators
from flask_wtf.file import FileField, FileAllowed, FileRequired

from wtforms.validators import InputRequired

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[InputRequired()])
    password = PasswordField('Password', validators=[InputRequired()])






class uploadForm(FlaskForm):
    
    firstname = StringField('FirstName', validators=[InputRequired()])
    lastname = StringField('Lastname', validators=[InputRequired()])
    
    age = StringField('Age', validators=[InputRequired()])
    bio = StringField('Biography', validators=[InputRequired()])
    gender = RadioField('Gender',choices=[('male','Male'),('female','Female')] ,validators=[validators.Required("Gender Must be specified")])
    
    
    upload = FileField('image', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'png'], 'Images only!')
    ])