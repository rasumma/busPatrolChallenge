

from flask import Flask, jsonify, request, json
import sqlite3 as sqlite
import sys


app = Flask(__name__)


#if no name is specified in paramaters, list all names for the user to choose by 
#connecting to the sqlite database and converting the names into json strings

@app.route('/users', methods=['GET'])
def listNames():
	jsonText = ""
	connection = sqlite.connect('buspatrol.db')
	with connection:	
		
		cursor = connection.cursor()
		cursor.execute("SELECT * FROM users")
		rows = cursor.fetchall()

		for row in rows:
			jsonText += json.dumps(row[1])

	return jsonify(jsonText) 
		

#if a name extension is specified, we check to see if the name is in the database and then get the jobID from the users database
#we then create a new connection to the jobs database and, using the jobID, we get the title and description of the job and then
#convert those into json strings

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

		jobID = usersRows[1]

	with jobsConnection:

		jobsCursor = jobsConnection.cursor()
		jobsCursor.execute("SELECT id, title, description FROM jobs WHERE id=:id", {"id" : jobID})
		jobsRows = jobsCursor.fetchone()

		jsonText += "{ job_title: " + json.dumps(jobsRows[1])
		jsonText += "   job_description: " + json.dumps(jobsRows[2]) + "}"

		


	return jsonify(jsonText)