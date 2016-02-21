from flask import make_response, render_template, request
from launch_physics import app
from launch_physics.login import login
from launch_physics.util import make_redirect

import datetime

@app.route("/")
def index_get():
	print(request.cookies)
	return render_template("index.html")

@app.route("/account")
def account_get():
	return render_template("account.html")

@app.route("/badges")
def badges_get():
	return render_template("badges.html")

@app.route("/login", methods=["GET"])
def login_get(reason=None):
	return render_template("login.html", reason=reason)

@app.route("/login", methods=["POST"])
def login_post():
	username = request.form["username"]
	password = request.form["password"]
	token = login(username, password)
	if token is None:
		# No such user exists, or the password was incorrect.
		resp = make_response(login_get("Invalid username or password."))
		resp.status_code = 403
		return resp
	else:
		# Login succeeded.
		expires = datetime.datetime.now() + datetime.timedelta(days=14)
		resp = make_redirect("/")
		resp.set_cookie("auth", value=token, expires=expires)
		return resp

@app.route("/logout")
def logout_get():
	resp = make_redirect("/")
	resp.set_cookie("auth", value="", expires=0)
	return resp

@app.route("/register", methods=["GET"])
def register_get():
	return render_template("register.html")

@app.route("/topic/<topic>")
def topic_view(topic):
	modules = ["example_module", "another_module", "a_third_module"]
	return render_template("topic.html", modules=modules, topic=topic)
