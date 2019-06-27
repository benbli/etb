from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, IntegerField
from wtforms.validators import DataRequired, Length


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(min=3, max=20)])
    password = PasswordField('password', validators=[DataRequired(), Length(min=8, max=80)])
    submit = SubmitField('Register')


class TournamentForm(FlaskForm):
    name = StringField('name', validators=[DataRequired(), Length(min=3, max=30)])
    numofplayers = IntegerField('numofplayers', validators=[DataRequired()])
    submit = SubmitField('Create')
