from flask_wtf import FlaskForm
#from wtforms import StringField
#from wtforms.validators import DataRequired
from flask_wtf import Form
from wtforms import TextField, BooleanField, validators, TextAreaField, SubmitField
from wtforms.validators import Required
#from flask.ext.wtf import Form, TextField, TextAreaField, SubmitField, validators, ValidationError

class ContactForm(Form):
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  subject = TextField("Subject",  [validators.Required("Please enter a subject.")])
  message = TextAreaField("Message",  [validators.Required("Please enter a message.")])
  submit = SubmitField("Send")

class SearchForm(Form):
  token = TextField("Token",  [validators.Required("Please enter token for search.")])
  name = TextField("Name",  [validators.Required("Please enter your name.")])
  email = TextField("Email",  [validators.Required("Please enter your email address."), validators.Email("Please enter your email address.")])
  submit = SubmitField("Send")
