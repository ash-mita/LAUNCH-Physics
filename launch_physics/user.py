import bcrypt
import jwt

from flask import request
from launch_physics.db import conn
from launch_physics.util import make_redirect

def auth():
	token = request.cookies.get("auth")
	if token is None:
		return None
	else:
		return User(token)

def login(username, password):
	"""Takes a username and password, returns an authentication token."""

	# Get the user from the database.
	with conn:
		with conn.cursor() as cur:
			cur.execute("SELECT passhash FROM users WHERE username = %s", (username,))
			user_tuple = cur.fetchone()
	# Check if no user exists.
	if user_tuple is None:
		return None
	# Check the passhash.
	password = password.encode("UTF-8")
	passhash = user_tuple[0].encode("UTF-8")
	if bcrypt.hashpw(password, passhash) != passhash:
		return None
	# Issue a token.
	return jwt.encode({"username": username}, passhash)

def require_auth(func):
	def inner(**kwargs):
		if auth() is None:
			return make_redirect("/login")
		else:
			return func(**kwargs)
	inner.__name__ = func.__name__
	return inner

class User:
	"""Represents a user's account."""
	def __init__(self, token):
		# Get the username from the token,
		username = jwt.decode(token, verify=False)["username"]
		# Query the database for the passhash associated with the user.
		# (We're using the passhashes as HMAC keys)
		with conn:
			with conn.cursor() as cur:
				cur.execute("SELECT passhash FROM users WHERE username = %s", (username,))
				passhash = cur.fetchone()[0]
		# This'll raise an error if the token signature is invalid.
		data = jwt.decode(token, passhash)
		self.username = data["username"]
