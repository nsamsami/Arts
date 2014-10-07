import os
from flask import Flask, render_template, redirect, request, g, session, url_for, flash, send_from_directory
from flask.ext.login import LoginManager, login_required, login_user, current_user, logout_user
from flask.ext.markdown import Markdown
from flask.ext.uploads import UploadSet, configure_uploads, IMAGES
from flask.ext.admin import Admin
from model import Admin, User, Image
import model
import forms
import string
import config


app = Flask(__name__)
app.config.from_object(config)


images = UploadSet('images', IMAGES)
configure_uploads(app, (images))

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
def upload_file(user=None):
    if not session.get('user_id'):
        flash("Please sign in to create a campaign")
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    print user
    if request.method == 'POST' and 'image' in request.files:
        image_id = "129.jpg"
        filename = images.save(request.files['image'], folder=None, name=image_id) 
        print filename
        title = request.form['title'] 
        description = request.form['description']
        print title 
        # user.image_1 = image_id 
        image = Image(image_id=filename, title=title, user_id=user_id)
        model.session.add(image)
        model.session.commit()
        return redirect(url_for('gallery'))
    else:
    	return render_template("projects.html")
    return ''

@app.route('/gallery')
def gallery():
    user_list = User.query.limit(100).all()
    image_list = Image.query.filter_by(approved=True).all()
    return render_template("gallery.html", user_list=user_list, image_list=image_list)

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

@app.route("/logout")
@login_required
def logout():
    logout_user()
    session.clear()
    return redirect(url_for("hello"))

@app.route("/login", methods=["POST"])
def authenticate(): 
    email = request.form.get('email')
    password = request.form.get('password')
    print email
    print password
    user = User.query.filter_by(email=email).one()
    print user
    if user.authenticate(password):
        login_user(user)
        session['userId'] = user.id
        print "authed"
        return redirect(url_for('upload_file', user=user))
    else:
        print "not-authed"
        return redirect(url_for('login')) 
    return ""

@app.route("/register")
def register():
    return render_template("register.html")

@app.route("/register", methods=["POST"])
def registerUser():
    email = request.form.get('email')
    password = request.form.get('password')
    first_name = request.form.get('first_name')
    last_name = request.form.get('last_name')
    verify = request.form.get('verify')
    if User.query.filter_by(email=email).all():
        flash("Email already exists")
        return redirect(url_for("register"))
    if password != verify:
        flash("Passwords do not match")
        return redirect(url_for("register"))
    #creates user row and also starter tasks
    user = User(email=email, first_name=first_name, last_name=last_name)
    user.set_password(password)
    model.session.add(user)
    model.session.commit()
    # model.createUser(email, password)
    return redirect(url_for("login"))

@app.route("/admin")
def admin():
    if not session.get('user_id'):
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user.admin == True:
        return redirect(url_for('hello'))
    print "is admin"
    image_list = Image.query.all()
    return render_template("admin.html", image_list=image_list)


@app.route("/admin/<int:id>/approve", methods=["POST"])
def give_approval(id):
    if not session.get('user_id'):
        return redirect(url_for('login'))
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user.admin == True:
        return redirect(url_for('hello'))
    print "is admin"
    image = Image.query.get(id)
    action = request.form.get("approve_button")
    if action == "Approve":
            image.approved = 1
    if action == "Disapprove":
            image.approved = 0
    model.session.commit()
        # action = request.form.get("kudos_button")
        # if applicationion == "Give Kudos":
        #     campaign.addKudos(session['user_id'])
        # else:
        #     campaign.removeKudos(session['user_id'])
        # model.session.commit()
    return redirect(url_for("admin", id=id))




if __name__ == "__main__":
    app.run(debug=True, port=5002)