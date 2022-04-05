from flask import Flask, render_template, redirect, flash, session
from models import db, connect_db, User
from forms import OnlyCsrfForm, RegisterUserForm, LoginForm

"""Note taking app with user authentication using Flask"""

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = 'MYPASSWORRD'

connect_db(app)
db.create_all()

SESSION_AUTH_KEY = "username"

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

        new_user = User.register(username=username, password=password,
            email=email, first_name=first_name, last_name=last_name)

        db.session.add(new_user)
        db.session.commit()

        session[SESSION_AUTH_KEY] = new_user.username

        flash(f"Successfully added user: {first_name} {last_name}")
        return redirect(f"/users/{new_user.username}")

    else:
        return render_template("add_user.html", form=form)


@app.route('/login', methods = ["GET","POST"])
def show_login_form():
    """Displays and handles login form"""

    form = LoginForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data

        user = User.authenticate(username=username, password=password)

        if user:
            # on successful login, redirect to secret page
            session[SESSION_AUTH_KEY] = user.username
            return redirect(f"/users/{user.username}")

        else:
            # re-render the login page with an error
            form.username.errors = ["Incorrect name/password"]

    return render_template("login.html", form=form)


@app.get('/users/<username>')
def show_user_page(username):
    """Shows user detail page"""

    form=OnlyCsrfForm()

    if session[SESSION_AUTH_KEY] != username:
        flash("You must be logged in to view!")
        return redirect("/login")

    else:
        msg = "You Made It!"
        return render_template("user_details.html", msg=msg,
            username=username, form=form)


@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = OnlyCsrfForm()

    if form.validate_on_submit():
        # Remove "user_id" if present, but no errors if it wasn't
        session.pop(SESSION_AUTH_KEY, None)
        flash("Successfully Logged Out!")
    return redirect("/login")