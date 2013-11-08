import os
from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def hello():
	return render_template("index.html")

@app.route('/about')
def about():
	return render_template("about.html")