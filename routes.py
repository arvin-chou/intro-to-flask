from flask import Flask, render_template, request, flash
from forms import ContactForm, SearchForm
from flask_mail import Mail, Message
from flask.ext.qrcode import QRcode
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import exc
import os

mail = Mail()

DEBUG = True
SQLALCHEMY_DATABASE_URI = 'sqlite:///flaskr.db'
SQLALCHEMY_ECHO = DEBUG
SECRET_KEY = 'development key'
USERNAME = 'admin'
PASSWORD = 'default'

# create our little application :)
app = Flask(__name__)

app.secret_key = 'development key'

app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 465
app.config["MAIL_USE_SSL"] = True
app.config["MAIL_USERNAME"] = 'contact@example.com'
app.config["MAIL_PASSWORD"] = 'your-password'
app.config.from_object(__name__)
app.config.from_envvar('FLASKR_SETTINGS', silent=True)


db = SQLAlchemy(app)
mail.init_app(app)
QRcode(app)

# TODO move to other py
class Entry(db.Model):
    __tablename__ = "entries"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(120), unique=True)
    token = db.Column(db.String(48))

@app.route('/')
def home():
  return render_template('home.html')

@app.route('/search', methods=['GET', 'POST'])
def search():
  form = SearchForm()
  token = None
  if request.method == 'POST':
        token = form.token.data
  elif request.method == 'GET':
        token = request.args.get('token')

  e = None
  try:
    e = db.session.query(Entry).filter(Entry.token == token).one()
    form.name.data = e.name
    form.email.data = e.email
  except exc.SQLAlchemyError:
    form.token.errors = ["not found by token"]
    pass 

  return render_template('search.html', success=e, form=form)

@app.route('/contact', methods=['GET', 'POST'])
def contact():
  form = ContactForm()

  if request.method == 'POST':
    if form.validate() == False:
      flash('All fields are required.')
      return render_template('contact.html', form=form)
    else:
      #msg = Message(form.subject.data, sender='contact@example.com', recipients=['your_email@example.com'])
      #msg.body = """
      #From: %s <%s>
      #%s
      #""" % (form.name.data, form.email.data, form.message.data)
      #mail.send(msg)
      entry = Entry()
      form.populate_obj(entry)
      entry.token = os.urandom(24).encode('hex') #uuid.uuid4().hex)
      db.session.add(entry)
      try:
        db.session.commit()
      except exc.SQLAlchemyError:
        flash('All fields are required.')
        return render_template('contact.html', form=form, sqlerr="duplicate name/email")


      token = request.url_root + "search?token=" + entry.token
      print "token=", token
      return render_template('contact.html', success=True, qrcode_content=token, token=entry.token)

  elif request.method == 'GET':
    return render_template('contact.html', form=form)
  
if __name__ == '__main__':
  db.create_all()
  app.run(debug=True)
