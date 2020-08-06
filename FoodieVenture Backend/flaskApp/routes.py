from flask import render_template, request, url_for
from flaskApp import app
from flaskApp.models import *
from flask import abort, jsonify

from flaskApp import yelpHandler as YelpHandler

import requests
import json
import os

# Flask app stuff (moving from flask app to flask API instead, WIP)
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == 'POST':
        userID = 1

        if 'breakfast' in request.form:
            updateUserChoices(userID, "Breakfast")
        if 'lunch' in request.form:
            updateUserChoices(userID, "Lunch")
        if 'dinner' in request.form:
            updateUserChoices(userID, "Dinner")
        if 'milkTea' in request.form:
            updateUserChoices(userID, "Milk Tea")
        if 'coffee' in request.form:
            updateUserChoices(userID, "Coffee")
        if 'dessert' in request.form:
            updateUserChoices(userID, "Dessert")

        # return redirect(url_for('index'))
        return render_template('index.html', userChoices = getUserChoices(1), canGenerateResults = getCanGenerateResults(1))
    elif request.method == 'GET':
        return render_template('index.html', userChoices = getUserChoices(1), canGenerateResults = getCanGenerateResults(1))

@app.route('/trip')
def trip():
    return render_template('trip.html')

@app.route('/results', methods = ['GET', 'POST'])
def results():
    print("Generating results")
    if request.method == 'POST':
        location = request.form['Location']
        return render_template('results.html',
        	posts=[{'name': 'First Restaurant', 'rating': 10, 'distance': 10, 'location': "3900 Parkview Ln Irvine, CA 92612",
            'image_url': "https://s3-media2.fl.yelpcdn.com/bphoto/2UFELlVHZsYj__uUBBxsGA/o.jpg"},
            {'name': 'Second Restaurant', 'rating': 10, 'distance': 10,'location': "3900 Parkview Ln Irvine, CA 92612",
            'image_url': "https://s3-media4.fl.yelpcdn.com/bphoto/34IT-RpTu2JEhmcmuw3q3g/o.jpg"}], userChoices = getUserChoices(1))
    return render_template('results.html', userChoices = getUserChoices(1))

# RESTful API for React

#   ToDo:
#       Simplify code with User.query.filter_by(username=username).first_or_404()
#       change userID to username

# URL parameters = "?location=..."
#                  "?selectedCategory=&selectedCategory&..."
# use curl -X GET http://127.0.0.1:5000/...           
@app.route('/user/<username>/categories/<categories>/', methods = ['POST'])
def modifyUserCategories(username, categories):
    try:
        # Return user data after modifying user's selected categories
        updateUserChoices(username, categories)
        return getUserDataFromDB(username)
    except UserDoesNotExistError:
        return jsonify(error=UserDoesNotExistError.getErrorMsg(username)), 404

@app.route('/user/<username>/categories/reset', methods = ['POST'])
def resetUserCategories(username):
    try:
        # Return user data after resetting user's selected categories
        resetUserChoices(username)
        return getUserDataFromDB(username)
    except UserDoesNotExistError:
        return jsonify(error=UserDoesNotExistError.getErrorMsg(username)), 404

@app.route('/user/<username>/', methods = ['GET'])
def getUserData(username):
    if request.method == 'GET':
        try:
            # Retrieve user data from existing userID
            return getUserDataFromDB(username)
        except UserDoesNotExistError:
            return jsonify(error=UserDoesNotExistError.getErrorMsg(username)), 404

@app.route('/accounts/', methods = ['POST'])
def createUser():
    try:
        createUserDB(request.json['username'])
        j = {
            "status": "okay",
            "action": "Created account {}".format(request.json['username'])
        }

        return json.dumps(j)
    except UserAlreadyExistsError:
        return jsonify(error=UserAlreadyExistsError.getErrorMsg(request.json['username'])), 404

@app.route('/accounts/id/<username>/delete', methods = ['POST'])
def deleteUser(username):
    try:
        deleteUserFromDB(username)

        j = {
            "status": "okay",
            "action": "Deleted account {}".format(username)
        }

        return json.dumps(j)
    except UserAlreadyExistsError:
        return jsonify(error=UserAlreadyExistsError.getErrorMsg(username)), 404
    except UserDoesNotExistError:
        return jsonify(error=UserDoesNotExistError.getErrorMsg(username)), 404

@app.route('/results/id/<id>', methods = ['POST'])
def testing(id = 0):
    requestJSON = json.loads(request.data)
    # print(requestJSON)
    j = YelpHandler.getPlaces(id, requestJSON['location'], requestJSON['selectedFoodCategories'], getStoredData(id))
    
    # j = [
    #         {   
    #         'name': 'First Restaurant', 'rating': 10, 'distance': 10, 'location': "3900 Parkview Ln Irvine, CA 92612",
    #         'image_url': "https://s3-media2.fl.yelpcdn.com/bphoto/2UFELlVHZsYj__uUBBxsGA/o.jpg"
    #         },
    #         {
    #             'name': 'Second Restaurant', 'rating': 10, 'distance': 10,'location': "3900 Parkview Ln Irvine, CA 92612",
    #         'image_url': "https://s3-media4.fl.yelpcdn.com/bphoto/34IT-RpTu2JEhmcmuw3q3g/o.jpg"
    #         }
    # ]

    return json.dumps(j)


@app.route('/guest/new', methods = ['POST'])
def createNewGuest():

    guestID = createGuest()

    return json.dumps({'guestID': guestID})

@app.route('/guest/id/<id>/remove', methods = ['POST'])
def removeGuest(id):

    deleteGuestFromDB(id)

    j = {
        "status": "okay",
        "action": "Deleted guest {}".format(id)
    }

    return json.dumps(j)

@app.route('/guest/id/<id>', methods = ['POST'])
def getGuestData(id):
    # print(getStoredData(1))

    return json.dumps({'Sorted Restaurants': getStoredData(id)})

