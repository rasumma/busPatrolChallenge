#Created by Rocco Summa
#6/1/2020
#rasumma@me.com
#Intern Challenge for buspatrol which seeks to utilize a sqlite database and flask in order to display
#users and job titles/descriptions in json within a web server route

from flask import Flask, jsonify, request, json
import sqlite3 as sqlite
import sys

app = Flask(__name__)

#if no name is specified in paramaters, list all valid names for the user to choose from by creating a cursor
#to fetch all of the the data from the users table and appending them all to a string to be jsonify'd
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
	
#if a name is specified, then we use whatever name they give us and check the users table for the given name.
#if it is a valid name then it will set the jobID variable to whatever jobID that user has in the table,
#otherwise the userRows object will be set as None, so I handle that error by returning a fairly generic error statement
#with information on how to search for valid names. We then use the jobID to search through the jobs table and we get the title
#and description from the table and jsonify them.	
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

