import requests
import json
import tkinter as tk
import ttkbootstrap as ttk
from PIL import Image, ImageTk
from io import BytesIO
import multiprocessing
import webbrowser

class GameCard(ttk.Frame):
    def __init__(self, parent, game_data, image):
        super().__init__(parent)
        self.game_data = game_data
        self.image = image
        self.create_widgets()
        

    def create_widgets(self):
        # Load image

        image = self.image
        image = image.resize((210, 100))
        photo = ImageTk.PhotoImage(image)

        # Image widget
        image_label = ttk.Label(self, image=photo)
        image_label.image = photo
        image_label.grid(row=0, column=0, pady=3, rowspan=2, columnspan=2)

        # Title label
        title_label = ttk.Label(self, text=self.game_data['name'][:20], font=('Arial', 12, 'bold'))
        title_label.grid(row=2, column=0,  padx=5, columnspan=3)

        # Likes label
        likes_label = ttk.Label(self, text=f'UpVotes: {int(self.game_data["totalUpVotes"])/1000:.1f}K', font=('Arial', 10))
        likes_label.grid(row=3, column=1, padx=2)

        # Dislikes label
        dislikes_label = ttk.Label(self, text=f'DownVotes: {int(self.game_data["totalDownVotes"])/1000:.1f}K', font=('Arial', 10))
        dislikes_label.grid(row=3, column=0)

        # Current players label
        players_label = ttk.Label(self, text=f'Current Players: {self.game_data["playerCount"]}', font=('Arial', 10))
        players_label.grid(row=4, column=0, sticky='w',columnspan=2)

        # Play now button
        play_button = ttk.Button(self, text='Play Now', command=lambda: webbrowser.open(f"https://www.roblox.com/games/{self.game_data['rootPlaceId']}"))
        play_button.grid(row=5, column=0, pady=(0, 10), columnspan=2)
        play_button.config(width=32)


class GameCatalog(ttk.Frame):
    def __init__(self, parent, games):
        super().__init__(parent)
        self.games = games
        self.cards = []
        self.create_widgets()

    def create_widgets(self):
        canvas = ttk.Canvas(self)
        scrollbar = ttk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollable_frame = ttk.Frame(canvas)

        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        # Calculate number of columns based on window width and card size
        card_width = 210
        num_columns = max(1, (self.winfo_width()-30) // card_width)

        # Create game cards
        image_uid = []
        for game_data in self.games:
            image_uid.append(game_data["universeId"])

        with multiprocessing.Pool(processes=10) as pool:
            result = pool.map(get_thumbnail, image_uid)
            result = pool.map(get_image, result)

        for game_data, image in zip(self.games, result):
            game_card = GameCard(scrollable_frame, game_data, image)
            self.cards.append(game_card)

        # Place game cards in a grid layout
        for i, card in enumerate(self.cards):
            row = i // num_columns
            column = i % num_columns
            card.grid(row=row, column=column, padx=10, pady=10, sticky='nsew')

        # Configure resizing behavior
        for column in range(num_columns):
            scrollable_frame.grid_columnconfigure(column, weight=1)
        for row in range((len(self.cards) - 1) // num_columns + 1):
            scrollable_frame.grid_rowconfigure(row, weight=1)

        # Pack the canvas and scrollbar
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        # Configure frame to resize with the window
        self.bind('<Configure>', self.on_resize)

    def on_resize(self, event):
        # Recalculate number of columns and adjust card positions on window resize
        card_width = 210
        num_columns = max(1, (event.width-120) // card_width)

        for i, card in enumerate(self.cards):
            row = i // num_columns
            column = i % num_columns
            card.grid(row=row, column=column, padx=10, pady=10, sticky='nsew')

        # Update column and row weights for resizing
        for column in range(num_columns):
            self.grid_columnconfigure(column, weight=1)
        for row in range((len(self.cards) - 1) // num_columns + 1):
            self.grid_rowconfigure(row, weight=1)

def query_data(query_item : str, pages_ammount : int):
    token = ""
    pages = []
    for i in range(pages_ammount):
        response = requests.get(f"https://apis.roblox.com/search-api/omni-search?searchQuery={query_item}&pageToken={token}&sessionId=d&pageType=all")
        response_data = json.loads(response.content)
        token = response_data["nextPageToken"]
        pages += response_data["searchResults"]
    result = []
    for i in pages:
        result.append(i["contents"][0])
    return result

def query_populars():
    response = requests.get("https://apis.roblox.com/explore-api/v1/get-sort-content?sessionId=d&sortId=Top_Trending_V2")
    response_data = json.loads(response.content)
    return response_data["games"]

def query_main(pages_ammount):
    token = ""
    pages = []
    for i in range(pages_ammount):
        response = requests.get(f"https://apis.roblox.com/explore-api/v1/get-sorts?sessionId=d&sortsPageToken={token}")
        response_data = json.loads(response.content)
        token = response_data["nextSortsPageToken"]
        pages += response_data["sorts"]
    result = []
    for i in pages:
        result += i["games"]
    return result


def query_placeInfo(root_id):
    response = requests.get(f"https://games.roblox.com/v1/games/multiget-place-details?placeIds={root_id}")
    response_data = json.loads(response.content)
    return response_data

def get_thumbnail(universe_id):
    response = requests.get(f"https://thumbnails.roblox.com/v1/games/multiget/thumbnails?universeIds={universe_id}&defaults=true&size=768x432&format=Png&isCircular=false")
    response_data = json.loads(response.content)
    return response_data['data'][0]["thumbnails"][0]["imageUrl"]

def get_image(url):
    return Image.open(requests.get(url, stream=True).raw)

def sort_data(data, reversed):
        data = sorted(data, key=lambda x: x[0], reverse=reversed)
        return [i[1] for i in data]

if __name__ == '__main__':
    multiprocessing.freeze_support()