import os
from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template("index.html")

@app.route('/teachers')
def teachers():
	return render_template("teachers.html")

@app.route('/principals')
def principals():
	return render_template("principals.html")

@app.route('/application')
def application():
	return render_template("application.html")

@app.route('/progeval')
def progeval():
	return render_template("progeval.html")

@app.route('/students')
def students():
	return render_template("students.html")

@app.route('/studapplication')
def studapplication():
	return render_template("studapplication.html")

@app.route('/studcontract')
def studcontract():
	return render_template("studcontract.html")

@app.route('/lessonplantemplate')
def lessonplantemplate():
	return render_template("lessonplantemplate.html")

@app.route('/samplelessonplans')
def samplelessonplans():
	return render_template("samplelessonplans.html")

@app.route('/planningcurriculum')
def planningcurriculum():
	return render_template("planningcurriculum.html")

@app.route('/postproject')
def postproject():
	return render_template("postproject.html")

@app.route('/families')
def families():
	return render_template("families.html")

@app.route('/projects')
def projects():
	return render_template("projects.html")

@app.route('/gallery')
def gallery():
	return render_template("gallery.html")

@app.route('/feedback')
def feedback():
	return render_template("feedback.html")

@app.route('/about')
def about():
	return render_template("about.html")

@app.route('/login')
def login():
	return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True, port=5001)