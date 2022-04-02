from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, EmailField
from wtforms.validators import DataRequired, Length, Email, InputRequired

class SignUpForm(FlaskForm):
    email = EmailField(label='Email',validators=[DataRequired(), Email()])
    username = StringField(label='Username', validators=[DataRequired(), Length(min = 7, max = 30)])
    password = PasswordField(label='Password', validators=[DataRequired(), InputRequired(), Length(min = 7, max = 30)])
    submit = SubmitField(label='Sign Up')