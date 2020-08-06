from flaskApp import db
from flaskApp import User
from flaskApp import Guest
from flaskApp import yelpHandler
from sqlalchemy import func
import json

# Database Errors
class UserDoesNotExistError(Exception):
    def getErrorMsg(userID):
        return "User ID " + "\'" + userID + "\'" + " does not exist in the database."

class UserAlreadyExistsError(Exception):
    def getErrorMsg(username):
        return "User " + "\'" + username+ "\'" + " already exists in the database."

# Database helper functions
def initializeUserChoices(userID):
    print("initializing user " + str(userID) + " choices")
    tempUser = User.query.filter_by(id = userID).first()
    tempUser.choices = '{"choices": []}'

    db.session.commit()

# User

def createUserDB(usernameArg, idArg = -1):
    idArg = getNextAvailableID(idArg, User)

    # Check if user id or username already exists in database
    if (User.query.filter_by(id = idArg).first() 
        or User.query.filter_by(username = usernameArg).first()):
            raise UserAlreadyExistsError

    print("Creating new user " + str(idArg))
    tempUser = User(id=idArg, username=usernameArg, choices='{"choices": []}', canGenerateResults="false")
    db.session.add(tempUser)
    db.session.commit()
    return tempUser

def deleteUserFromDB(username):
    # Check if user id or username already exists in database
    if (not User.query.filter_by(username = username).first()):
        raise UserDoesNotExistError

    userToDelete = User.query.filter_by(username = username).first()
    print("Removing user " + username)
    
    db.session.delete(userToDelete)
    db.session.commit()

def updateUserChoices(username, choice):
    tempUser = User.query.filter_by(username = username).first()

    if not tempUser:
        raise UserDoesNotExistError
    else:
        if tempUser.choices == '':
            initializeUserChoices(1)

        tempUserChoices = json.loads(tempUser.choices)
        if not choice in tempUserChoices['choices']:
            print("Adding " + choice + " to " + tempUser.username + "'s choices")
            tempUserChoices['choices'].append(choice)
        else:
            print("Removing " + choice + " from " + tempUser.username + "'s choices")
            tempUserChoices['choices'].remove(choice)

        tempUser.choices = json.dumps(tempUserChoices)
        
        db.session.commit()

def removeChoice(userID, choice):
    tempUser = User.query.filter_by(id = userID).first()

    if not tempUser:
        raise Exception("User was not found in the database.")

    if tempUser.choices == '':
        initializeUserChoices(userID)

    tempUserChoices = json.loads(tempUser.choices)
    tempUserChoices['choices'].remove(choice)
    tempUser.choices = json.dumps(tempUserChoices)

    db.session.commit()

def resetUserChoices(username):
    tempUser = User.query.filter_by(username = username).first()

    if not tempUser:
        # print("Raising user does not exist error from resetUserChoices")
        raise UserDoesNotExistError

    tempUser.choices = '{"choices": []}'

    db.session.commit()

def getUserChoices(userID):
    tempUser = User.query.filter_by(id = userID).first()
    if tempUser:
        tempUserChoices = json.loads(tempUser.choices)
        return tempUserChoices
    else:
        raise UserDoesNotExistError

def getCanGenerateResults(userID):
    tempUser = User.query.filter_by(id = userID).first()
    if tempUser:
        return tempUser.canGenerateResults
    else:
        return []

# Guest
def createGuest():
    idArg = getNextAvailableID(-1, Guest)

    print("Creating new guest " + str(idArg))
    tempUser = Guest(id=idArg, username=("Guest " + str(idArg)))
    db.session.add(tempUser)
    db.session.commit()
    return idArg

def deleteGuestFromDB(idArg):
    if Guest.query.filter_by(id = idArg).first():
        guest= Guest.query.filter_by(id = idArg).first()

        print("Removing guest " + idArg)
        
        db.session.delete(guest)
        db.session.commit()

# Database Modification

# Returns user data in json form
def getUserDataFromDB(username):
    tempUser = User.query.filter_by(username = username).first()
    if tempUser:

        userDataJson = {
            "username": tempUser.username,
            "choices": tempUser.choices,
            "canGenerateResults": tempUser.canGenerateResults
        }

        return json.dumps(userDataJson)
    else:
        # print("Raising user does not exist error from getUserDataFromDB")
        raise UserDoesNotExistError

def resetDB():
    db.drop_all()
    db.create_all()
    createUserDB("User 1", 1)
    createGuest()
    db.session.commit()

# Helper functions
def getNextAvailableID(idArg, dbClass):
    # if there are no users in database
    if not db.session.query(func.max(dbClass.id)).scalar():
        return 1
    # if no idArg is supplied then retrieve next available id
    elif idArg == -1:
        return db.session.query(func.max(dbClass.id)).scalar() + 1

# Testing
def storeJSON(idArg, jsonArg, category):
    guest = Guest.query.filter_by(id = idArg).first()
    print("saving " + category + " to guest " + str(idArg))
    
    # Only store if category in database is empty
    if (category == "breakfast" and guest.breakfast == ""):
        guest.breakfast = jsonArg
    elif (category == "lunch" and guest.lunch == ""):
        guest.lunch = jsonArg
    elif (category == "dinner" and guest.dinner == ""):
        guest.dinner = jsonArg
    elif (category == "dessert" and guest.dessert == ""):
        guest.dessert = jsonArg
    elif (category == "coffee" and guest.coffee == ""):
        guest.coffee = jsonArg
    elif (category == "milkTea" and guest.milkTea == ""):
        guest.milkTea = jsonArg

    db.session.commit()

def getStoredData(idArg):
    guest = Guest.query.filter_by(id = idArg).first()

    data = {"food": "", "coffee": guest.coffee, 
            "breakfast": guest.breakfast, "milkTea": guest.milkTea, 
            "dessert": guest.dessert, "lunch": guest.lunch,
            "dinner": guest.dinner}
    
    return data

def clearStoredJSON(idArg):
    guest = Guest.query.filter_by(id = idArg).first()

    guest.breakfast = ""
    guest.lunch = ""
    guest.dinner = ""
    guest.dessert = ""
    guest.coffee = ""
    guest.milkTea = ""

    db.session.commit()

def storeJSONFromLocalData(idArg):
    guest = Guest.query.filter_by(id = idArg).first()
    f = open("flaskApp/yelpJSONExamples/yelpBreakfastJson.txt")
    guest.breakfast = json.dumps(f.read())
    f.close()
    guest = Guest.query.filter_by(id = idArg).first()
    f = open("flaskApp/yelpJSONExamples/yelpLunchJson.txt")
    guest.lunch = json.dumps(f.read())
    f.close()
    guest = Guest.query.filter_by(id = idArg).first()
    f = open("flaskApp/yelpJSONExamples/yelpDinnerJson.txt")
    guest.dinner = json.dumps(f.read())
    f.close()
    guest = Guest.query.filter_by(id = idArg).first()
    f = open("flaskApp/yelpJSONExamples/yelpDessertJson.txt")
    guest.dessert = json.dumps(f.read())
    f.close()
    guest = Guest.query.filter_by(id = idArg).first()
    f = open("flaskApp/yelpJSONExamples/yelpCoffeeJson.txt")
    guest.coffee = json.dumps(f.read())
    f.close()
    guest = Guest.query.filter_by(id = idArg).first()
    f = open("flaskApp/yelpJSONExamples/yelpMilkTeaJson.txt")
    guest.milkTea = json.dumps(f.read())
    f.close()
    db.session.commit()

resetDB()
# storeJSON(1)
# clearStoredJSON(1)