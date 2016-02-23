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
		cur.execute("CREATE TABLE IF NOT EXISTS topics (topicName TEXT PRIMARY KEY, moduleCount INTEGER)")
		cur.execute("CREATE TABLE IF NOT EXISTS quizzes (topicName TEXT, num INTEGER, question TEXT, answer INTEGER, q1 TEXT, q2 TEXT, q3 TEXT, q4 TEXT)")
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
				("kinematics", 3),
				("projectile_motion", 0),
				("forces", 0),
				("momentum", 0),
			]
			cur.executemany("INSERT INTO topics (topicName, moduleCount) VALUES (%s, %s)", topics)
		topics = list(map(lambda x: x[0], topics))
	with conn.cursor() as cur:
		cur.execute("SELECT * FROM quizzes")
		quizzes = cur.fetchall()
		if len(quizzes) == 0:
			quizzes = [
				# kinematics
				("kinematics", 1, "Which is the displacement of the object’s motion, and what is the distance that the object traveled?", 2, "1. Distance, 2. Displacement", "1. Displacement, 2. Distance", "", ""),
				("kinematics", 2, "Velocity is a vector.", 1, "True", "False", "", ""),
				("kinematics", 3, "Displacement is a vector.", 1, "True", "False", "", ""),
				("kinematics", 4, "Acceleration is the change in position over the change in time.", 2, "True", "False", "", ""),
				("kinematics", 5, "If a ball is dropped from a height of 5 meters, how long will it take for the ball to reach the ground?", 1, "Less than 1 second", "2 Seconds", "3 Seconds", "4 Seconds"),
				("kinematics", 6, "How far will an object travel if it moves at 10 meters per second for 15 seconds?", 2, "100 meters", "150 meters", "200 meters", "50 meters"),
				# TODO
			]
			cur.executemany("INSERT INTO quizzes (topicName, num, question, answer, q1, q2, q3, q4) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", quizzes)
