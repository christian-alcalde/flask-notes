from flask import Flask, render_template, redirect, flash, session
from models import db, connect_db, User, Note
from forms import OnlyCsrfForm, RegisterUserForm, LoginForm, AddNoteForm, EditNoteForm

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

    if SESSION_AUTH_KEY in session:
        return redirect(f"/users/{session['username']}")

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

    if SESSION_AUTH_KEY not in session:
        flash("You must be logged in!")
        return redirect("/login")

    elif session[SESSION_AUTH_KEY] != username:
        flash("Stop Being Malicious!")
        return redirect(f"/login")

    else:
        user = User.query.get_or_404(username)
        return render_template("user_details.html", user=user, form=form)


@app.post("/logout")
def logout():
    """Logs user out and redirects to homepage."""

    form = OnlyCsrfForm()

    if form.validate_on_submit():
        # Remove "user_id" if present, but no errors if it wasn't
        session.pop(SESSION_AUTH_KEY, None)
        flash("Successfully Logged Out!")
    return redirect("/login")


@app.post('/users/<username>/delete')
def delete_user(username):
    """Deletes all user posts and then the user from the database"""

    form = OnlyCsrfForm()

    #need to validate csrf token
    if form.validate_on_submit():
        user = User.query.get_or_404(username)
        Note.query.filter_by(owner = username).delete()

        db.session.commit()

        db.session.delete(user)
        db.session.commit()

        session.pop(SESSION_AUTH_KEY, None)
        flash("User Successfully Deleted!")

    return redirect("/")

@app.route('/users/<username>/notes/add', methods = ["GET", "POST"])
def add_new_note(username):
    """ Displays and handles new note form """

    if SESSION_AUTH_KEY not in session:
            flash("You must be logged in to view!")
            return redirect("/login")

    elif session[SESSION_AUTH_KEY] != username:
        flash("Stop being malicious!")
        return redirect("/login")

    else:

        form = AddNoteForm()

        if form.validate_on_submit():

            title = form.title.data
            content = form.content.data

            new_note = Note(title=title, content=content, owner=username)

            db.session.add(new_note)
            db.session.commit()

            session[SESSION_AUTH_KEY] = username

            flash(f"Successfully added new note!")
            return redirect(f"/users/{username}")

        else:
            return render_template("add_note.html", form=form)


@app.route('/notes/<int:note_id>/update', methods = ["GET", "POST"])
def edit_note(note_id):
    """Displays and handles edit note form"""

    note = Note.query.get(note_id)

    if SESSION_AUTH_KEY not in session:
            flash("You must be logged in to view!")
            return redirect("/login")

    elif session[SESSION_AUTH_KEY] != note.owner:
        flash("You must be logged in to view!")
        return redirect("/login")

    else:
        form = EditNoteForm(obj=note)

        if form.validate_on_submit():

            note.title = form.title.data
            note.content = form.content.data

            db.session.commit()

            session[SESSION_AUTH_KEY] = note.owner

            flash(f"Successfully added new note!")
            return redirect(f"/users/{note.owner}")

        else:
            return render_template("add_note.html", form=form)

@app.post('/notes/<int:note_id>/delete')
def delete_note(note_id):
    """Deletes note from database and redirects to user page"""
    form = OnlyCsrfForm()

    #need to validate csrf token
    if form.validate_on_submit():

        note = Note.query.filter_by(id=note_id).one_or_none()
        owner = note.owner
        db.session.delete(note)
        db.session.commit()

        flash("Note Successfully Deleted!")
        return redirect(f"/users/{owner}")

    else:
        return render_template(f"/users/{owner}")