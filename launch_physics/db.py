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
		cur.execute("CREATE TABLE IF NOT EXISTS badges (name TEXT PRIMARY KEY, modules INTEGER)")
		cur.execute("CREATE TABLE IF NOT EXISTS topics (name TEXT PRIMARY KEY)")

# Check if data exists; if any given piece doesn't, add it.
with conn:
	with conn.cursor() as cur:
		cur.execute("SELECT * FROM users WHERE username = 'admin'")
		if len(cur.fetchall()) == 0:
			cur.execute("INSERT INTO users (username, passhash) VALUES (%s, %s)",
				("admin", "$2a$04$3HkhVmktIx6CoGHmLghhyeeHontS/1cX8.fizQZK5TGJdrzyPBAwS"))
	with conn.cursor() as cur:
		cur.execute("SELECT * FROM badges")
		badges = cur.fetchall()
		if len(badges) == 0:
			badges = [
				("rookie", 1),
				("physicist", 5),
				("newton", 10),
				("maxwell", 20),
				("muon", 30),
				("higgs", 40)
			]
			cur.executemany("INSERT INTO badges (name, modules) VALUES (%s, %s)", badges)
	with conn.cursor() as cur:
		cur.execute("SELECT * FROM topics")
		topics = cur.fetchall()
		if len(topics) == 0:
			topics = [
				("kinematics",),
				("projectile_motion",),
				("forces",),
				("energy",),
			]
			cur.executemany("INSERT INTO topics (name) VALUES (%s)", topics)
		topics = list(map(lambda x: x[0], topics))
