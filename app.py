"""Blogly application."""

from flask import Flask, request, render_template,redirect, flash, session
from models import db, connect_db, User, Post, PostTag, Tag
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)
app.app_context().push() 

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///blogly'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCH EMY_ECHO'] = True
app.config['SECRET_KEY'] = "SECRET!"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


connect_db(app)
db.create_all()

@app.route('/')
def home_page():
    posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    return render_template("posts/homepage.html", posts=posts)


##############################################################################

@app.route('/users')
def show_all_users():
    """Show all users"""
    users = User.query.order_by(User.last_name, User.first_name).all()
    return render_template('users/index.html', users = users)


@app.route('/users/new', methods = ["GET"])
def show_user_form():
    """Show the user form"""
    return render_template('users/new_user.html')


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
    return render_template('users/show_user.html', user=user)


@app.route('/users/<int:user_id>/edit')
def edit_unique_user(user_id):
    """Show a form to edit an existing user"""

    user = User.query.get_or_404(user_id)
    return render_template('users/edit_user.html', user=user)



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

##############################################################################
 

@app.route('/users/<int:user_id>/posts/new')
def show_post_form(user_id):
    """Show form to add a post for that user."""

    user = User.query.get_or_404(user_id)
    return render_template('posts/add_post.html', user=user)



@app.route('/users/<int:user_id>/posts/new', methods = ["POST"] )
def add_new_post(user_id):
    """Get Data via From for a Specific User."""

    user = User.query.get_or_404(user_id)
    new_post = Post(
        title = request.form["title"],
        content = request.form["content"],
        # user = user
        users_id = user_id
        )


    db.session.add(new_post)
    db.session.commit()
    # flash(f"Post '{new_post.title}' added.")

    return redirect(f"/users/{user_id}")


@app.route('/posts/<int:post_id>')
def show_post(post_id):
    """Show, edit , delete posts"""

    post = Post.query.get_or_404(post_id)
    return render_template('posts/show_post.html', post = post)


@app.route('/posts/<int:post_id>/edit', methods = ["GET"])
def show_edit_post(post_id):
    """Show a form to edit an existing post"""

    post = Post.query.get_or_404(post_id)
    user = post.user
    return render_template('posts/edit_post.html', post = post, user = user)


@app.route('/posts/<int:post_id>/edit', methods = ["POST"])
def edit_post(post_id):
    """Handle editing of a post. Redirect back to the post view."""

    post = Post.query.get_or_404(post_id)
    post.title = request.form['title']
    post.content = request.form['content']

    db.session.add(post)
    db.session.commit()
    
    return redirect(f"/users/{post.users_id}")



@app.route ('/posts/<int:post_id>/delete', methods = ["POST"])
def delete_post(post_id):

    post = Post.query.get_or_404(post_id)

    db.session.delete(post)
    db.session.commit()

    return redirect(f"/users/{post.users_id}")



##############################################################################

@app.route("/tags")
def show_all_tags():
    tags = Tag.query.all()
    return render_template("tags/show_tags.html", tags = tags)

@app.route("/tags/new", methods = ["GET"])
def show_new_tag_form():

    posts = Post.query.all()
    return render_template('tags/tag_form.html', posts=posts)

@app.route("/tags/new", methods = ["POST"])
def create_new_tag():
    """Process add form, adds tag, and redirect to tag list."""
    
    new_tag = Tag(name=request.form['name'])

    db.session.add(new_tag)
    db.session.commit()

    flash(f"Tag '{new_tag.name}' added.")

    return redirect("/tags")


@app.route("/tags/<int:tag_id>")
def show_tag_detail(tag_id):

    tag = Tag.query.get_or_404(tag_id)
    return render_template ("tags/tag_detail.html", tag = tag)

@app.route("/tags/<int:tag_id>/edit", methods = ["GET"])
def edit_tag_detail(tag_id):
    """Show a form to edit an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    posts = Post.query.all()
    return render_template ("tags/tag_edit.html", tag=tag, posts = posts)


@app.route('/tags/<int:tag_id>/edit', methods=["POST"])
def edit_tag_submission(tag_id):
    """Handle form submission for updating an existing tag"""

    tag = Tag.query.get_or_404(tag_id)
    tag.name = request.form['name']
    post_ids = [int(num) for num in request.form.getlist("posts")]
    tag.posts = Post.query.filter(Post.id.in_(post_ids)).all()

    db.session.add(tag)
    db.session.commit()
    flash(f"Tag '{tag.name}' edited.")

    return redirect("/tags")

@app.route("/tags/<int:tag_id>/delete", methods = ["POST"])
def delete_tag(tag_id):

    """Delete a tag"""

    tag = Tag.query.get_or_404(tag_id)

    db.session.delete(tag)
    db.session.commit()

    flash(f"Tag '{tag.name}' deleted.")

    return redirect("/tags")

