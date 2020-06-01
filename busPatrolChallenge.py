

from flask import Flask, jsonify, request, json
import sqlite3 as sqlite
import sys


app = Flask(__name__)

#attempt connection to busPatrol database



#if no name is specified in paramaters, list all names for the user to choose.
@app.route('/users', methods=['GET'])
def listNames():
	jsonText = ""
	connection = sqlite.connect('buspatrol.db')
	with connection:	
		
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM users")
		rows = cursor.fetchall()

		for row in rows:
			jsonText += row[1] + "  " 

	return jsonify(users=jsonText) 
		


@app.route('/users/<string:name>', methods=['GET'])
def listUserDescription(name):
	jsonText = ""
	jobID = 0

	jobsConnection = sqlite.connect('buspatrol.db')
	usersConnection = sqlite.connect('buspatrol.db')
	with usersConnection:

		usersCursor = usersConnection.cursor()
		usersCursor.execute("SELECT name, job  FROM users WHERE name=:name", {"name" : name})
		usersRows = usersCursor.fetchone()
		if usersRows is None:
			jsonText = "Not a valid user. Please check /users for valid users."
			return jsonify(jsonText)
		else:
			jobID = usersRows[1]

	with jobsConnection:

		jobsCursor = jobsConnection.cursor()
		jobsCursor.execute("SELECT id, title, description FROM jobs WHERE id=:id", {"id" : jobID})
		jobsRows = jobsCursor.fetchone()

	
	return jsonify(job_title=jobsRows[1],
			job_description=jobsRows[2])
		