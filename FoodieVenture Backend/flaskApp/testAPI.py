import json
import os
import requests

def testDeleteUser():
    # User exists
    r = requests.post("http://127.0.0.1:5000/accounts/user/howarl3/delete")
    # print(r.json())
    assert ("error" not in r.json())

    # User does not exist
    r = requests.post("http://127.0.0.1:5000/accounts/user/99/delete")
    # print(r.json())
    assert ("error" in r.json())

    print("testDeleteUser() == PASS")

def testResetUserChoices():
    # User exists
    r = requests.post("http://127.0.0.1:5000/user/howardlam546/categories/reset")
    # print(r.json())
    assert ("error" not in r.json())

    # User does not exist
    r = requests.post("http://127.0.0.1:5000/user/99/categories/reset")
    # print(r.json())
    assert ("error" in r.json())

    print("testResetUserData() == PASS")

def testGetUserData():
    # User exists
    r = requests.get("http://127.0.0.1:5000/user/howardlam546/")
    assert ("error" not in r.json())

    # User does not exist
    r = requests.get("http://127.0.0.1:5000/user/99/")
    # print(r.json())
    assert ("error" in r.json())

    print("tesGetUserData() == PASS")

def testModifyUserData():
    # User exists
    r = requests.post("http://127.0.0.1:5000/user/howardlam546/categories/Breakfast/")
    # print(r.json())
    assert ("error" not in r.json())

    # User does not exist
    r = requests.post("http://127.0.0.1:5000/user/99/categories/Breakfast/")
    # print(r.json())
    assert ("error" in r.json())

    print("testModifyUserData() == PASS")

def testCreateUser(username):
    data = {
        "username": username,
        "password": "abc123",
    }

    r = requests.post("http://127.0.0.1:5000/accounts/", json=data)
    # print(r.json())

    r = requests.get("http://127.0.0.1:5000/user/{}/".format(username))
    assert ("error" not in r.json())

def printUserData(username):
    r = requests.get("http://127.0.0.1:5000/user/" + str(username) + "/")
    # print(r.json())

class customClass:
    errorMsg = "error!!!"

def test():
    j = {
    "businesses": [
            {
                "id": "yM6wFvTwL8S4pAysfKZxBw",
                "alias": "scramblz-san-jose",
                "name": "Scrambl'z",
                "image_url": "https:\/\/s3-media4.fl.yelpcdn.com\/bphoto\/TyGS_dVHTBsxcl-btv-c2A\/o.jpg",
                "is_closed": False,
                "url": "https:\/\/www.yelp.com\/biz\/scramblz-san-jose?adjust_creative=5a1jm8VuhczsXD4fPOyDaA&utm_campaign=yelp_api_v3&utm_medium=api_v3_business_search&utm_source=5a1jm8VuhczsXD4fPOyDaA",
                "review_count": 1711,
                "categories": [
                    {
                    "alias": "breakfast_brunch",
                    "title": "Breakfast & Brunch"
                    }
                ]
            }
        ]
    }

    f = open("test.txt", "w")

    # f.write(str(json.dumps(j)))
    json.dump(j, f, indent=4)

    f.close()

def main():
    # Test assumes howardlam546 is an existing user
    # testCreateUser("howarl3")
    # testModifyUserData()
    # testResetUserChoices()
    # testGetUserData()
    # testDeleteUser()
    test()

if __name__ == '__main__':
    main()
