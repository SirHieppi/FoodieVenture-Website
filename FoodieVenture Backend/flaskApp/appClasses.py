class Restaurant:
    def __init__(self, data: dict):
        self.name = data['name']
        self.address = ""
        for item in data['address']:
            self.address += item + " "
        self.distance = data['distance']
        self.rating = data['rating']
        self.imgUrl = data['image_url']
        self.categories = data['categories']
        self.categoryGeneratedFor = ""
        self.reviewNum = data['reviewNum']
        self.url = data['url']

    def getNearbyDessertPlaces(self):
        pass

    def getRestaurantInfo(self):
        return {
            'name': self.name, 
            'rating': self.rating, 
            'distance': self.distance, 
            'location': self.address, 
            'image_url': self.imgUrl,
            'category': self.categoryGeneratedFor,
            'reviewNum':self.reviewNum,
            'url': self.url,
        }

class RestaurantData:
    def __init__(self, restaurants : list):
        self.restaurants = restaurants

    def getRestaurant(self, index):
        return self.restaurants[index]

    def printRestaurantInfo(self):
        for restaurant in self.restaurants:
            print(restaurant.name + " : " + restaurant.address)
            print("\t Rating: " + str(restaurant.rating))

    def setClosestThreePlaces(self):
        self.firstPlace = self.restaurants[0]
        closestIndex = 0
        for restaurant in self.restaurants:
            if restaurant.distance <= closestIndex:
                closestIndex = restaurant.distance
        # for restaurant in self.restaurants:
        #     if restaurant.distance <= closestIndex:
