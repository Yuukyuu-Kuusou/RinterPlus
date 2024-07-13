import requests
import json

def query_data(query_item : str, pages_ammount : int):
    token = ""
    pages = []
    for i in range(pages_ammount):
        response = requests.get(f"https://apis.roblox.com/search-api/omni-search?searchQuery={query_item}&pageToken={token}&sessionId=d&pageType=all")
        response_data = json.loads(response.content)
        token = response_data["nextPageToken"]
        pages.append(response_data["searchResults"])
    return pages

def query_populars():
    response = requests.get("https://apis.roblox.com/explore-api/v1/get-sort-content?sessionId=d&sortId=Top_Trending_V2")
    response_data = json.loads(response.content)
    return response_data["games"]

def query_main():
    response = requests.get("https://apis.roblox.com/explore-api/v1/get-sorts?sessionId=d")
    response_data = json.loads(response.content)
    data = []
    for i in response_data["sorts"]:
        data.append(i["games"])
    return data


def query_placeInfo(root_id):
    response = requests.get(f"https://games.roblox.com/v1/games/multiget-place-details?placeIds={root_id}")
    response_data = json.loads(response.content)
    return response_data

def get_thumbnail(universe_id):
    response = requests.get(f"https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds={universe_id}&defaults=true&size=768x432&format=Png&isCircular=false")
    response_data = json.loads(response.content)
    return response_data['data'][0]["thumbnails"][0]["imageUrl"]

