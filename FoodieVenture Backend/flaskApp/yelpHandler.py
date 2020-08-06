import json
import urllib.parse
import urllib.request
import random
import requests
import os
from _random import Random
from flaskApp import app
from flaskApp import models as M

apiKey = "**************"
googleMapImgApi = "*************"
yelpApiKey = "*************"

_testing = False # True == does not make any requests (uses static json stored in txt)
_webMode = True # True when starting flask application

if _webMode:
    from flaskApp.appClasses import Restaurant
    from flaskApp.appClasses import RestaurantData
else:
    # from flaskApp import appClasses
    from appClasses import *


def createUrlComponents(location: str):
    # Formatting
    location = location.replace(" ", "+")

    # declaring strings that will make up the url
    url = "https://api.yelp.com/v3/businesses/search"

    headers = {
        'Authorization': 'Bearer %s' % yelpApiKey,
    }

    return url, headers

def extractData(jsonFile):
    listOfRestaurants = []
    
    if "error" in json.dumps(jsonFile):
        print("Error with request! Check JSON file error dump.")
        f = open("JSONErrorDump.txt", "w")
        f.write(json.dumps(jsonFile))
        f.close()
    else:
        for restaurant in jsonFile['businesses']:
            newRestaurant = Restaurant({'name': restaurant['name'], 
                                        'address': restaurant['location']['display_address'], 
                                        'distance': restaurant['distance'], 
                                        'rating': restaurant['rating'], 
                                        'image_url': restaurant['image_url'],
                                        'categories': restaurant['categories'],
                                        'reviewNum': restaurant['review_count'],
                                        'url': restaurant['url']})
            listOfRestaurants.append(newRestaurant)

    return listOfRestaurants

def getResponse(location, searchTerm):
    categories = {}
    radius = 20
    limit = 50
    openNow = True

    url, headers = createUrlComponents(location)
    print("Making a request...")
    response = requests.request('GET', "https://api.yelp.com/v3/businesses/search",
    headers=headers, params={'location': location, 'limit': limit, 'term': searchTerm})
    print("Done making a request!")

    return response

def getRestaurantData(address):
    response = getResponse(address)
    # print(json.dumps(response.json()))
    listOfRestaurants = extractData(response.json())
    restaurantData = RestaurantData(listOfRestaurants)
    # trip.printRestaurantInfo()
    return listOfRestaurants

# fileName is for testing with json text files
def getData(userID, location, searchTerm, fileName = "", savedRestaurantData = ""):
    if not _testing:
        if savedRestaurantData == "":
            response = getResponse(location, searchTerm)
            
            listOfRestaurants = extractData(response.json())

            # Save json in database only if it is not in db
            M.storeJSON(userID, json.dumps(response.json()), searchTerm)

            restaurantData = RestaurantData(listOfRestaurants)
        else:
            listOfRestaurants = extractData(json.loads(savedRestaurantData))

            restaurantData = RestaurantData(listOfRestaurants)

        return restaurantData

    else:
        if fileName != "":
            tempJSON = getTestJSON(fileName)
            listOfRestaurants = extractData(tempJSON)

            # Save json in database only if it is not in db
            M.storeJSON(userID, json.dumps(tempJSON), searchTerm)

            restaurantData = RestaurantData(listOfRestaurants)

            return restaurantData
        else:
            listOfRestaurants = extractData(json.loads(savedRestaurantData))

            restaurantData = RestaurantData(listOfRestaurants)

            return restaurantData

# Modifies sorted restaurants
def sortRestaurants(listOfRestaurants, sortedRestaurants : dict):
    dessertCategories = ["desserts", "icecream", 
                            "bakeries", "cupcakes"]

    for restaurant in listOfRestaurants:
        isBreakfastPlace = False
        isDessertPlace = False
        isCoffeePlace = False
        isMilkTeaPlace = False
        if checkCategory("breakfast_brunch", restaurant.categories): 
            sortedRestaurants["breakfast"].add(restaurant)
        # check if any restaurant category are dessert related
        if len(list(set(getAliasCategories(restaurant.categories)) 
                & set(dessertCategories))) > 0:
            sortedRestaurants["dessert"].add(restaurant)
            isDessertPlace = True
        if checkCategory("coffee", restaurant.categories):
            sortedRestaurants["coffee"].add(restaurant)
            isCoffeePlace = True
        if checkCategory("bubbletea", restaurant.categories):
            sortedRestaurants["milkTea"].add(restaurant)
            isMilkTeaPlace = True
        if not isBreakfastPlace and not isDessertPlace and not isCoffeePlace and not isMilkTeaPlace:
            sortedRestaurants["food"].add(restaurant)
# Finds all restaurant from search term and sorts
# the results into a dictionary
def getSortedRestaurantData(userID, location : str, sortedRestaurants : dict, 
    userSelectedCategories = [], searchTerm = 'food', fileName = "", savedRestaurantData = ""):
    # File name is for testing with json text files
    # Get all restaurant data from search term
    restaurantData : RestaurantData = getData(userID, location, searchTerm, fileName, savedRestaurantData)

    # Sort the restaurants based on category
    sortRestaurants(restaurantData.restaurants, sortedRestaurants)  

# Returns randomly selected places based on user's categories
# And all restaurants sorted in a dictionary based on categories
# which will be used to store in the user database to reuse
def getPlaces(userID, location, userSelectedCategories = [], savedRestaurantData = {}) -> dict:
    # path = "./flaskApp/yelpJSONExamples/  (for testing with website)"
    # path = "./yelpJSONExamples/   (for testing on its own)"
    
    if _webMode:
        path = "./flaskApp/yelpJSONExamples/"
    else:
        path = "./yelpJSONExamples/"

    # If sortedRestaurants is empty
    if not savedRestaurantData:
        sortedRestaurants = {"food": set({}), "coffee": set({}), 
                            "breakfast": set({}), "milkTea": set({}), "dessert": set({})}

        # print("user selected categories is " + str(userSelectedCategories))
    
        # Make requests according to categories that the user has selected
        # The food category is composed of lunch and dinner
        if 'lunch' in userSelectedCategories or 'dinner' in userSelectedCategories or 'food' in userSelectedCategories:
            # Gather 50 food places
            getSortedRestaurantData(location, sortedRestaurants, userSelectedCategories, 'food', path + "yelpFoodJson.txt")
        if 'breakfast' in userSelectedCategories:
            # Gather 50 breakfast places
            getSortedRestaurantData(location, sortedRestaurants, userSelectedCategories, 'breakfast', path + "yelpBreakfastJson.txt")
        if 'milkTea' in userSelectedCategories:
            # Gather 50 milk tea places
            getSortedRestaurantData(location, sortedRestaurants, userSelectedCategories, 'milktea', path + "yelpMilkTeaJson.txt")
        if 'coffee' in userSelectedCategories:
            # Gather 50 food places
            getSortedRestaurantData(location, sortedRestaurants, userSelectedCategories, 'coffee', path + "yelpCoffeeJson.txt")
        if 'dessert' in userSelectedCategories:
            # Gather 50 dessert places (using the dessert term)
            getSortedRestaurantData(location, sortedRestaurants, userSelectedCategories, 'dessert', path + "yelpDessertJson.txt")
    else:
        sortedRestaurants = {"food": set({}), "coffee": set({}), 
                            "breakfast": set({}), "milkTea": set({}), "dessert": set({})}
        
        # Check if data needs to be fetched for each category based on data passed to this function
        if 'lunch' in userSelectedCategories:
            if savedRestaurantData['lunch'] == "":
                # fetch from local json text files
                getSortedRestaurantData(userID, location, sortedRestaurants, userSelectedCategories, 'lunch', path + "yelpLunchJson.txt")
            else:
                print("reusing")
                # fetch from database
                getSortedRestaurantData(userID, location, sortedRestaurants, userSelectedCategories, 'lunch', '', savedRestaurantData['lunch'])

        if 'dinner' in userSelectedCategories:
            if savedRestaurantData['dinner'] == "":
                # fetch from local json text files
                getSortedRestaurantData(userID, location, sortedRestaurants, userSelectedCategories, 'dinner', path + "yelpDinnerJson.txt")
            else:
                print("reusing")
                # fetch from database
                getSortedRestaurantData(userID, location, sortedRestaurants, userSelectedCategories, 'dinner', '', savedRestaurantData['dinner'])

        if 'breakfast' in userSelectedCategories:
            if savedRestaurantData['breakfast'] == "":
                # fetch from local json text files
                getSortedRestaurantData(userID, location, sortedRestaurants, userSelectedCategories, 'breakfast', path + "yelpBreakfastJson.txt")
            else:
                print("reusing")
                # fetch from database
                getSortedRestaurantData(userID, location, sortedRestaurants, userSelectedCategories, 'breakfast', '', savedRestaurantData['breakfast'])
        if 'milkTea' in userSelectedCategories:
            if savedRestaurantData['milkTea'] == "":
                # fetch from local json text files
                getSortedRestaurantData(userID, location, sortedRestaurants, userSelectedCategories, 'milkTea', path + "yelpMilkTeaJson.txt")
            else:
                print("reusing")
                # fetch from database
                getSortedRestaurantData(userID, location, sortedRestaurants, userSelectedCategories, 'milkTea', '', savedRestaurantData['milkTea'])
        if 'coffee' in userSelectedCategories:
            if savedRestaurantData['coffee'] == "":
                # fetch from local json text files
                getSortedRestaurantData(userID, location, sortedRestaurants, userSelectedCategories, 'coffee', path + "yelpCoffeeJson.txt")
            else:
                print("reusing")
                # fetch from database
                getSortedRestaurantData(userID, location, sortedRestaurants, userSelectedCategories, 'coffee', '', savedRestaurantData['coffee'])
        if 'dessert' in userSelectedCategories:
            if savedRestaurantData['dessert'] == "":
                # fetch from local json text files
                getSortedRestaurantData(userID, location, sortedRestaurants, userSelectedCategories, 'dessert', path + "yelpDessertJson.txt")
            else:
                print("reusing")
                # fetch from database
                getSortedRestaurantData(userID, location, sortedRestaurants, userSelectedCategories, 'dessert', '', savedRestaurantData['dessert'])

    # printSortedRestaurants(sortedRestaurants)

    return getRandomPlaces(sortedRestaurants, userSelectedCategories)

def getRandomPlaces(sortedRestaurants: dict, userSelectedCategories = []):
    randomPlaces = {}

    for category in userSelectedCategories:
        if (category == 'lunch' or category == 'dinner') and len(sortedRestaurants['food']) > 0:
            randomIndex = random.randrange(0, len(sortedRestaurants['food']))
            randomPlaces[category] = list(sortedRestaurants['food'])[randomIndex]
            randomPlaces[category].categoryGeneratedFor = category
        elif len(sortedRestaurants[category]) > 0 and not category == 'food':
            randomIndex = random.randrange(0, len(sortedRestaurants[category]))
            randomPlaces[category] = list(sortedRestaurants[category])[randomIndex]
            if category == "milkTea":
                randomPlaces[category].categoryGeneratedFor = "milk tea"
            else:
                randomPlaces[category].categoryGeneratedFor = category

    # print("\n\n")
    # printRandomlyPickedPlaces(randomPlaces)

    return createJSONFromRandomPlaces(randomPlaces)

# Helper functions
def createJSONFromRandomPlaces(randomPlaces):
    j = []

    for place in randomPlaces.values():
        # j[place.name] = place.getRestaurantInfo()
        j.append(place.getRestaurantInfo())

    return j

def combineDicts(dict1, dict2):
    for key in dict2.keys():
        if key in dict1:
            dict1[key] += dict2[key]
        else:
            dict1[key] = dict2[key]
    
    return dict1

def getAliasCategories(categories):
    aliasCategories = []
    for category in categories:
        aliasCategories.append(category['alias'])
    return aliasCategories

def checkCategory(categoryToCheck, restaurantCategories):
    for category in restaurantCategories:
        if categoryToCheck == category['alias']:
            return True
    return False

def printSortedRestaurants(sortedRestaurants):
    print("Sorted restaurants: ")
    for key in sortedRestaurants.keys():
        print("\t" + key)
        print("\t\t", end="")
        for restaurant in sortedRestaurants[key]:
            print(restaurant.name, end=", ")
        print("")
    
def printRandomlyPickedPlaces(randomPlaces: dict):    
    for key in randomPlaces.keys():
        print(key + ": ")
        print("\t" + randomPlaces[key].name)

def createRandomlyPickedPlacesPost(randomPlaces: dict):
    post = []

    for category in randomPlaces:
        post.append(randomPlaces[category].getRestaurantInfo())

    print("post is " + str(post))

    return post


#------------------------------------------------------------------#

# testing

def runTestingStuff():
    if _testing:
        print(json.dumps(getPlaces("", ['breakfast'], {"food": {"hello"}, "coffee": {}, 
                            "breakfast": {}, "milkTea": {}, "dessert": {}})))
        # sortedRestaurants, randomPlaces = getPlaces("", ['milkTea'])
        
        # getPlaces("", ['milkTea'], {'milkTea': set({
        #     Restaurant({'name': 'pekoe', 'distance': 0, 'address': "", 'rating': 0, 'image_url': "", 'categories': [{'alias': 'bubbletea'}]}),
        #     Restaurant({'name': 'happy lemon', 'distance': 0, 'address': "", 'rating': 0, 'image_url': "", 'categories': [{'alias': 'bubbletea'}]}),        
        # })})

        # getPlaces("", ['milkTea'])

def getTestJSON(fileName):
    f = open(fileName)
    j = json.loads(f.read())
    f.close()
    return j
    
def createTestJsonFile(fileName, location, searchTerm):
    f = open(fileName, "w")
    # f.write(str(json.dumps(getResponse(location, searchTerm).json())))
    json.dump(getResponse(location, searchTerm).json(), f, indent=4)
    f.close()   

def createTestJsonFiles():
    location = "5507 Don Rodolfo Ct"
    createTestJsonFile("./yelpJSONExamples/yelpBreakfastJson.txt", location, "breakfast")
    createTestJsonFile("./yelpJSONExamples/yelpLunchJson.txt", location, "lunch")
    createTestJsonFile("./yelpJSONExamples/yelpDinnerJson.txt", location, "dinner")
    createTestJsonFile("./yelpJSONExamples/yelpDessertJson.txt", location, "dessert")
    createTestJsonFile("./yelpJSONExamples/yelpCoffeeJson.txt", location, "coffee")
    createTestJsonFile("./yelpJSONExamples/yelpMilkTeaJson.txt", location, "milk tea")
    createTestJsonFile("./yelpJSONExamples/yelpFoodJson.txt", location, "food")
    
    print("Done generating test json text files") 



# runTestingStuff()
# createTestJsonFiles()
