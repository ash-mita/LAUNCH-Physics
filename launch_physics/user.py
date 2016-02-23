import bcrypt
import jwt

from flask import request
from launch_physics.db import conn
from launch_physics.util import make_redirect

def auth():
	try:
		token = request.cookies.get("auth")
		if token is None:
			return None
		else:
			return User.find(token)
	except:
		return False

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

	def __init__(self, username, modulesCompleted):
		self.username = username
		self.modulesCompleted = modulesCompleted
	@classmethod
	def exists(cls, username):
		"""Takes a username, returns whether it's in the database or not."""
		with conn:
			with conn.cursor() as cur:
				cur.execute("SELECT username FROM users WHERE username = %s", (username,))
				return cur.fetchone() is not None
	@classmethod
	def find(cls, token):
		# Get the username from the token,
		username = jwt.decode(token, verify=False)["username"]
		# Query the database for the passhash associated with the user.
		# (We're using the passhashes as HMAC keys)
		with conn:
			with conn.cursor() as cur:
				cur.execute("SELECT (passhash, modulesCompleted) FROM users WHERE username = %s", (username,))
				user_tuple = cur.fetchone()
				print(user_tuple)
				passhash = user_tuple[0]
		# This'll raise an error if the token signature is invalid.
		return User(jwt.decode(token, passhash)["username"], modulesCompleted)
	@classmethod
	def new(cls, username, password):
		"""Registers and returns a user with a given username and password."""
		with conn:
			with conn.cursor() as cur:
				cur.execute("INSERT INTO users (username, modulesCompleted) VALUES (%s, %s)",
					(username, 0))
		user = User(username, 0)
		user.change_password(password)
		return user
	def change_password(self, password):
		"""Changes the user's password."""
		passhash = bcrypt.hashpw(password.encode("UTF-8"), bcrypt.gensalt())
		print("==============>", passhash)
		with conn:
			with conn.cursor() as cur:
				cur.execute("UPDATE users SET passhash=%s WHERE username=%s",
					(passhash.decode("UTF-8"), self.username))
