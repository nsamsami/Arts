import os
from flask import Flask, render_template, redirect, request, g, session, url_for, flash, send_from_directory
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user
from flask.ext.markdown import Markdown
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
from model import Admin, User
import model
import forms
import string

UPLOAD_FOLDER = '/images'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS

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

# @app.route('/projects')
# def projects():
# 	return render_template("projects.html")

# @app.route('/projects', methods=["POST"])
# def projects_upload():
# 	user_id = session.get('user_id')
# 	if 'image' in request.files:
#         filename = images.save(request.files['image'], folder=None, name=image_id) 
#         user.img = image_id
#     	model.session.commit()
# 	return render_template("gallery.html")

@app.route('/projects', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        file = request.files['image']
        if file and allowed_file(file.filename):
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('uploaded_file',
                                    filename=filename))
    else:
    	return render_template("projects.html")
    return ''

@app.route('/gallery')
def gallery():
	return render_template("gallery.html")

@app.route('/feedback')
def feedback():
	return render_template("feedback.html")

@app.route('/about')
def about():
	return render_template("about.html")



# Stuff to make login easier
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'

#login and logout stuff here
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@app.route('/login')
def login():
	return render_template("login.html")

@app.route("/login", methods=["POST"])
def authenticate(): 
    email = request.form.get('email')
    password = request.form.get('password')
    user = User.query.filter_by(email=email).one()
    if user.authenticate(password):
        session['userId'] = user.id
        return redirect(url_for('projects'))
    else:
        flash("Invalid username or password")
        return redirect(url_for('login')) 


if __name__ == "__main__":
    app.run(debug=True, port=5002)