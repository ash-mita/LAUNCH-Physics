from flask import make_response, render_template, request
from launch_physics import app
from launch_physics.login import login

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
def login_get():
	return render_template("login.html")

@app.route("/login", methods=["POST"])
def login_post():
	username = request.form["username"]
	password = request.form["password"]
	return "TODO: " + login(username, password)

@app.route("/logout")
def logout_get():
	resp = make_response(render_template("redirect.html", url="/"))
	resp.headers["Location"] = "/"
	resp.status_code = 303
	resp.set_cookie("auth", value="", expires=0)
	return resp

@app.route("/register", methods=["GET"])
def register_get():
	return render_template("register.html")

@app.route("/topic/<topic>")
def topic_view(topic):
	modules = ["example_module", "another_module", "a_third_module"]
	return render_template("topic.html", modules=modules, topic=topic)

@app.route("/topic/<topic>/<module>")
def module_view(module, topic):
	return render_template("module.html", module=module, topic=topic)
