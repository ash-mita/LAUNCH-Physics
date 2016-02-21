import bcrypt
import psycopg2
import jwt

conn = psycopg2.connect("dbname=launch_physics user=launch_physics")

# Create the tables needed for the application.
with conn:
	with conn.cursor() as cur:
		cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, passhash TEXT)")
		cur.execute("CREATE TABLE IF NOT EXISTS completions (name TEXT, username TEXT, status INTEGER)")

# Check if the admin user exists; if they don"t, add an admin user.
with conn:
	with conn.cursor() as cur:
		cur.execute("SELECT * FROM users WHERE username = 'admin'")
		if len(cur.fetchall()) == 0:
			cur.execute("INSERT INTO users (username, passhash) VALUES (%s, %s)",
				("admin", "$2a$04$3HkhVmktIx6CoGHmLghhyeeHontS/1cX8.fizQZK5TGJdrzyPBAwS"))

def login(username, password):
	# Get the user from the database.
	with conn:
		with conn.cursor() as cur:
			cur.execute("SELECT * FROM users WHERE username = %s", (username,))
			user_tuple = cur.fetchone()
	# Check if no user exists.
	if user_tuple is None:
		return None
	# Check the passhash.
	password = password.encode("UTF-8")
	passhash = user_tuple[1].encode("UTF-8")
	if bcrypt.hashpw(password, passhash) != passhash:
		return None
	# Issue a token.
	return jwt.encode({"username": username}, passhash)
