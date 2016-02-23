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
		cur.execute("CREATE TABLE IF NOT EXISTS users (username TEXT PRIMARY KEY, passhash TEXT, modulesCompleted INTEGER)")
		cur.execute("CREATE TABLE IF NOT EXISTS scores (moduleName TEXT, username TEXT, status INTEGER)")
		cur.execute("CREATE TABLE IF NOT EXISTS topics (topicName TEXT PRIMARY KEY)")
		cur.execute("CREATE TABLE IF NOT EXISTS modules (modulesName TEXT PRIMARY KEY, topicName TEXT)")
		cur.execute("CREATE TABLE IF NOT EXISTS badges (badgeName TEXT PRIMARY KEY, modulesNeeded INTEGER)")

# Check if data exists; if any given piece doesn't, add it.
with conn:
	with conn.cursor() as cur:
		cur.execute("SELECT * FROM users WHERE username = 'admin'")
		if len(cur.fetchall()) == 0:
			cur.execute("INSERT INTO users (username, passhash, modulesCompleted) VALUES (%s, %s, %s)",
				("admin", "$2a$04$3HkhVmktIx6CoGHmLghhyeeHontS/1cX8.fizQZK5TGJdrzyPBAwS", 0))
	with conn.cursor() as cur:
		cur.execute("SELECT * FROM badges")
		badges = cur.fetchall()
		if len(badges) == 0:
			badges = [
				("rookie", 1),
				("scientist", 5),
				("newton", 10),
				("maxwell", 20),
				("muon", 30),
				("higgs", 40)
			]
			cur.executemany("INSERT INTO badges (badgeName, modulesNeeded) VALUES (%s, %s)", badges)
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
			cur.executemany("INSERT INTO topics (topicName) VALUES (%s)", topics)
		topics = list(map(lambda x: x[0], topics))
