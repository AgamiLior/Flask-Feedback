from flask import Flask, render_template, redirect, session, flash
from flask_debugtoolbar import DebugToolbarExtension
from models import connect_db, db, User, Feedback
from forms import RegisterForm, LoginForm, UserForm, FeedbackForm
# from sqlalchemy.exc import IntegrityError

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False


connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def home_page():
    """ Shows Home page or User's page"""
    if "username" in session:
        return redirect(f"/users/{session['username']}")
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register_user():
    """ Rgister new user"""
    form = RegisterForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        user = User.register(username, password, email, first_name, last_name)

        db.session.add(user)
        db.session.commit()

        session['username'] = user.username
        flash('Welcome! Successfully Created Your Account!', "success")
        return redirect(f"/users/{user.username}")

    return render_template('register.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login_user():    
    """ User Login to their account"""
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user = User.authenticate(username, password)
        if user:
            flash(f"Welcome Back, {user.username}!", "primary")
            session['username'] = user.username
            return redirect(f"/users/{user.username}")
        else:
            flash('Please Log in first or create a new account', 'danger')
            return render_template("login.html", form=form)

    return render_template('login.html', form=form)


@app.route('/users/<username>')
def user_page(username):
    """ Shows User's Page"""
    if "username" not in session or username != session['username']:
        session.pop('username')
        flash("You can't get to this route, please log in to your account", 'danger')
        return redirect("/")
    user = User.query.get(username)
    form = UserForm()

    return render_template('users/user.html', user = user, form=form)

@app.route('/users/<username>/delete', methods=['POST'])
def delete_user(username):
    """ Delete User Account """
    if "username" not in session or username != session['username']:
        flash("You can't get Delete that account", 'danger')
        return redirect('/')
    user = User.query.get(username)
    db.session.delete(user)
    db.session.commit()
    flash("Your User Account has been deleted", 'danger')
    session.pop("username")
    
    return redirect ('/')
@app.route('/logout')
def logout_user():
    session.pop('username')
    flash("Goodbye!", "info")
    return redirect('/')


@app.route('/users/<username>/feedback/add', methods=['GET','POST'])
def add_feedback(username):
    """ Add Feedback """
    if "username" not in session or username != session['username']:
        session.pop('username')
        flash("You can't get to this route, please log in to your account", 'danger')
        return redirect("/")
    form = FeedbackForm()
    
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data
        
        feedback = Feedback(title=title, content=content, username=username)
        
        db.session.add(feedback)
        db.session.commit()
        user = User.query.get(username)
        return redirect(f"/users/{user.username}")
    else:
        return render_template("feedback/add.html", form=form)

@app.route('/feedback/<int:feedback_id>/edit', methods=['GET','POST'])
def edit_feedback(feedback_id):
    """ Edit Feedback """
    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        session.pop('username')
        flash("You can't get to this route, please log in to your account", 'danger')
        return redirect("/")
    form = FeedbackForm(obj=feedback)
    
    if form.validate_on_submit():
        feedback.title = form.title.data
        feedback.content = form.content.data
        
        db.session.commit()
        return redirect(f"/users/{feedback.username}") 

    return render_template("feedback/edit.html", form=form, feedback=feedback)


@app.route("/feedback/<int:feedback_id>/delete", methods=["POST"])
def delete_feedback(feedback_id):
    """ Delete Feedback """

    feedback = Feedback.query.get(feedback_id)
    if "username" not in session or feedback.username != session['username']:
        session.pop('username')
        flash("You can't get to this route, please log in to your account", 'danger')
        return redirect("/")

    form = UserForm()

    if form.validate_on_submit():
        db.session.delete(feedback)
        db.session.commit()

    return redirect(f"/users/{feedback.username}")