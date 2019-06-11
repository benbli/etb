from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, Length

class DraftForm(FlaskForm):
	player = StringField('player', validators=[Length(min=3, max=20)])