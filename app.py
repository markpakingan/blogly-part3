"""Blogly application."""

from flask import Flask, request, render_template,redirect, flash, session
from models import db, connect_db, User
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.app_context().push() 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    return redirect("/users")


##############################################################################

@app.route('/users')
def show_all_users():
    """Show all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('index.html', users = users)


@app.route('/users/new', methods = ["GET"])
def show_user_form():
    """Show the user form"""
    return render_template('user_form.html')


@app.route('/users/new', methods = ["POST"])
def add_new_users():
    """create new users on the form"""
    new_user = User(
    first_name = request.form["first_name"],
    last_name = request.form["last_name"],
    image_url = request.form["image_url"] or None)


    db.session.add(new_user)
    db.session.commit()

    return redirect("/users")


@app.route('/users/<int:user_id>')
def show_unique_user(user_id):
    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_unique_user(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('edit_user.html', user=user)



@app.route('/users/<int:user_id>/edit', methods = ["POST"])
def update_unique_user(user_id):
    """update user's info"""

    user = User.query.get_or_404(user_id)
    user.first_name = request.form["first_name"]
    user.last_name = request.form["last_name"]
    user.image_url = request.form["image_url"]

    db.session.add(user)
    db.session.commit()
    
    return redirect('/users')

@app.route('/users/<int:user_id>/delete', methods = ["POST"])     
def delete_unique_user(user_id):

    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()

    return redirect("/users")