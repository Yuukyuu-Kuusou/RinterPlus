import requests
from bs4 import BeautifulSoup
import json

"""
main: https://apis.roblox.com/explore-api/v1/get-sorts?sessionId=d
populares: https://apis.roblox.com/explore-api/v1/get-sort-content?sessionId=d&sortId=Top_Trending_V2 
search:https://apis.roblox.com/search-api/omni-search?searchQuery={query}&pageToken={token}&sessionId=d&pageType=all
place-info: https://games.roblox.com/v1/games/multiget-place-details?placeIds={}
"""

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




with open("teste.json", 'w') as file:
    for i in query_data("tycoon", 2):
        file.write(json.dumps(i))