import os
from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from flask_wtf.file import FileField, FileRequired
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


basedir = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///'+os.path.join(basedir, "data.sqlite")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = 'mysecretkey'

db = SQLAlchemy(app)

Migrate(app,db)

class Refer(db.Model):
	__tablename__ = "Referral"

	id = db.Column(db.Integer, primary_key=True)
	name = db.Column(db.Text)
	lastname = db.Column(db.Text)
	company = db.Column(db.Text)
	resume = db.Column(db.LargeBinary)

	def __init__(self, name, lastname, company, resume):
		self.name = name
		self.lastname = lastname
		self.company = company
		self.resume = resume

	def __repr__(self):
		return f"{self.name} requested referral for {self.company}"

class InfoForm(FlaskForm):
	name = StringField("Name?")
	lastname = StringField("Last name?")
	company = StringField("Company")
	resume = FileField(validators=[FileRequired()])
	submit = SubmitField("Submit")

@app.route('/')
def index():
	return render_template("index.html")


@app.route('/form', methods=['GET','POST'])
def form():
	name = False
	lastname = False
	company = False
	resume = False
	form = InfoForm()
	if form.validate_on_submit():
		name = form.name.data
		lastname = form.lastname.data
		company = form.company.data
		resume = form.resume.data

		newReferral = Refer(name, lastname, company, resume.read())
		db.session.add(newReferral)
		db.session.commit()

		return redirect(url_for("list_referrals"))
	return render_template("form.html", form=form)

		# f = form.resume.data
		# filename = secure_filename(f.filename)

	# 	form.name.data = ""
	# 	form.lastname.data = ""
	# 	form.company.data = ""
	# 	form.resume.data = ""
	# 	return redirect(url_for("thank_you"))
	#
	# return render_template("form.html", form=form, name=name, lastname=lastname, comppany=company, resume=resume)

@app.route("/list")
def list_referrals():
	refers = Refer.query.all()
	return render_template("list.html", refers=refers)

@app.route("/thank_you")
def thank_you():
	return render_template("thank_you.html")


@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404


if __name__ == '__main__':
	app.run(debug=True)
