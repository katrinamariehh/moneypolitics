from flask import Flask, render_template, redirect, request, g, session, url_for, flash
# from model import User, Post
# from flask.ext.login import LoginManager, login_required, login_user, current_user
# from flaskext.markdown import Markdown
# import config
# import forms
import model
import json

app = Flask(__name__)
# app.config.from_object(config)

@app.route("/member/<opensecrets_id>/chart")
def make_bubbles(opensecrets_id):
    json_dump = json.dumps(model.make_json(opensecrets_id))
    return render_template('bubble.html', opensecrets_id=opensecrets_id)

@app.route("/")
def index():
    # display all legislators
    legislator_list = model.get_all_current()
    return render_template('index.html', legislator_list=legislator_list)

@app.route("/member/<opensecrets_id>/contributions") #need to pick id to use
def table_sector_breakdown(opensecrets_id):
    # display sector contribution breakdown
    sectors = model.get_sectors(opensecrets_id)
    return render_template('legislator.html', sectors=sectors, \
        opensecrets_id=opensecrets_id)

@app.route("/member/<opensecrets_id>/contributions/json")
def view_sector_breakdown(opensecrets_id):
    # display sector contribution breakdown
    # sectors = model.get_sectors(opensecrets_id)
    # return render_template('legislator.html', sectors=sectors)
    sectors = model.make_json2(opensecrets_id)
    json_dump = json.dumps(sectors)
    return json_dump

@app.route("/member/<member_id>/votes")
def view_vote_breakdown(member_id):
    # display votes by subject of bill
    return render_template('template_name')



# this is all the stuff that was just there

# @app.route("/")
# def index():
#     posts = Post.query.all()
#     return render_template("index.html", posts=posts)

# @app.route("/post/<int:id>")
# def view_post(id):
#     post = Post.query.get(id)
#     return render_template("post.html", post=post)

# @app.route("/post/new")
# @login_required
# def new_post():
#     return render_template("new_post.html")

# @app.route("/post/new", methods=["POST"])
# @login_required
# def create_post():
#     form = forms.NewPostForm(request.form)
#     if not form.validate():
#         flash("Error, all fields are required")
#         return render_template("new_post.html")

#     post = Post(title=form.title.data, body=form.body.data)
#     current_user.posts.append(post) 
    
#     model.session.commit()
#     model.session.refresh(post)

#     return redirect(url_for("view_post", id=post.id))

# @app.route("/login")
# def login():
#     return render_template("login.html")

# @app.route("/login", methods=["POST"])
# def authenticate():
#     form = forms.LoginForm(request.form)
#     if not form.validate():
#         flash("Incorrect username or password") 
#         return render_template("login.html")

#     email = form.email.data
#     password = form.password.data

#     user = User.query.filter_by(email=email).first()

#     if not user or not user.authenticate(password):
#         flash("Incorrect username or password") 
#         return render_template("login.html")

#     login_user(user)
#     return redirect(request.args.get("next", url_for("index")))


if __name__ == "__main__":
    app.run(debug=True)
