from flask import Blueprint, render_template, request, jsonify, flash, redirect, url_for
from flask_login import current_user, login_required
from app.models import db, User, Post, load_user
from .blogforms import PostForm

blog = Blueprint('blog', __name__, template_folder='blog_templates', url_prefix='/blog')

@blog.route('/<string:username>', methods=['GET', 'POST'])
def userProfile(username):
    user = User.query.filter_by(username=username).first()
    if user:
        posts = Post.query.filter_by(user_id=user.id).order_by(Post.timestamp.desc()).all()
    else:
        # replace with 404 redirect later
        return render_template('userprofile.html', user=None, posts=None)
    # if we get here, a user exists with this username
    form = PostForm()
    if request.method == 'POST' and current_user.is_authenticated:
        if current_user.id == user.id and form.validate_on_submit():
            # normal post stuff
            newpost = Post()
            newpost.body = form.new_post.data
            newpost.user_id = current_user.id
            db.session.add(newpost)
            db.session.commit()
            flash('New post created :)', 'success')
            return redirect(url_for('blog.userProfile', username=current_user.username))
        else:
            # someone tried to bypass the template, don't let them
            return jsonify({'Come on': 'you shouldnt be here'}), 403
    return render_template('userprofile.html', user=user, posts=posts, form=form)


# pretty common structure for a route for a button that does some interaction with database
# has its own route which does some stuff then redirects back to a route that renders a template
@blog.route('/delete/<int:pid>')
@login_required
def deletePost(pid):
    to_delete = Post.query.get(pid)
    if current_user.id == to_delete.user_id:
        db.session.delete(to_delete)
        db.session.commit()
        flash('Post deleted successfully.', 'info')
        return redirect(url_for('blog.userProfile', username=current_user.username))
    return jsonify({'Come on': 'you shouldnt be here'}), 403

@blog.route('/users')
def users():
    if current_user.is_authenticated:
        users = User.query.filter(User.id!=current_user.id).all()
    else:
        users = User.query.all()
    return render_template('findusers.html', users=users)

@blog.route('/newsfeed')
def newsfeed():
    if current_user.is_authenticated:
        # this will change to a different query when we have our follower system built
        posts = current_user.followed_posts()
        print(current_user.followed)
    else:
        # no one signed in? show all the posts
        posts = Post.query.order_by(Post.timestamp.desc()).all()   
    return render_template('newsfeed.html', posts=posts)

@blog.route('/follow/<string:uid>')
@login_required
def follow(uid):
    u = User.query.get(uid)
    current_user.follow(u)
    flash(f'Followed @{u.username}', 'info')
    return redirect(url_for('blog.userProfile', username=u.username))

@blog.route('/unfollow/<string:uid>')
@login_required
def unfollow(uid):
    u = User.query.get(uid)
    current_user.unfollow(u)
    flash(f'Unfollowed @{u.username}', 'warning')
    return redirect(url_for('blog.userProfile', username=u.username))