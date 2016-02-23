from launch_physics.db import conn
import os.path

def introduction(topicName):
	"""Returns the introduction associated with the topic."""
	path = os.path.join(os.path.dirname(__file__), "data", topicName, "introduction.html")
	try:
		return open(path).read()
	except:
		return None

def modules(topicName):
	"""Returns all the modules associated with the topic."""
	with conn:
		with conn.cursor() as cur:
			cur.execute("SELECT moduleCount FROM topics WHERE topicName=%s", (topicName,))
			moduleCount = cur.fetchone()[0]
	if moduleCount is None:
		return None
	def loadModule(i):
		path = os.path.join(os.path.dirname(__file__), "data", topicName, "modules", str(i+1) + ".html")
		return open(path).read()
	return map(loadModule, range(moduleCount))

def quizzes(topicName):
	"""Returns all quiz questions associated with the topic."""
	with conn:
		with conn.cursor() as cur:
			cur.execute("SELECT * FROM quizzes WHERE topicName=%s ORDER BY num ASC", (topicName,))
			return cur.fetchall()
