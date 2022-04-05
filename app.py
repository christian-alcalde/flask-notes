from flask import Flask, render_template, request, redirect, flash
from models import db, connect_db, User
from forms import RegisterUserForm

"""Note taking app with user authentication using Flask"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'MYPASSWORRD'

connect_db(app)
db.create_all()

@app.get('/')
def get_homepage():
    """Redirect to homepage"""

    return redirect('/register')

@app.route('/register', methods = ["GET","POST"])
def show_register_form():
    """Displays and handles the register form"""

    form = RegisterUserForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User.register(username=username, password=password, email=email, first_name=first_name, last_name=last_name)

        db.session.add(new_user)
        db.session.commit()

        flash(f"Successfully added user: {first_name} {last_name}")
        return redirect("/register")

    else:
        return render_template("addUser.html", form=form)

@app.route('/login', methods = ["GET","POST"])
def show_login_form():
    """Displays and handles login form"""

    form = RegisterUserForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        new_user = User(username = username,
                        password = password)

        db.session.add(new_user)
        db.session.commit()

        flash(f"Successfully added user: {first_name} {last_name}")
        return redirect("/secret")

    else:
        return render_template("addUser.html", form=form)
