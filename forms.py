from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Datarequired, Email

class ContactForm(FlaskForm):
    name=StringField('Name', validators=[Datarequired()])
    email=StringField('Email', validators=[Datarequired(), Email()])
    submit=SubmitField('Submit')
