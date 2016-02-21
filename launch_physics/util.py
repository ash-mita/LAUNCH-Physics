from flask import make_response, render_template

def make_redirect(url):
	resp = make_response(render_template("redirect.html", url=url))
	resp.headers["Location"] = url
	resp.status_code = 303
	return resp
