import os
import psycopg2
import urllib.parse

def connect():
	dbURL = os.environ.get("DATABASE_URL")
	if dbURL is None:
		return psycopg2.connect("dbname=launch_physics user=launch_physics")
	else:
		url = urllib.parse.urlparse(dbURL)
		return psycopg2.connect(
			database=url.path[1:],
			user=url.username,
			password=url.password,
			host=url.hostname,
			port=url.port
		)

conn = connect()

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
