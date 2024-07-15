
if __name__ == "__main__":
    import tkinter as tk
    import ttkbootstrap as ttk
    from utils import *
    #Creates Root Window
    window = ttk.Window(themename="darkly")
    window.title("Roblox Interface+") 
    window.geometry("800x500")

    nb_tabs = ttk.Notebook(window)
    nb_tabs.pack(expand=1,fill='both')
    home_tab = ttk.Frame(nb_tabs)
    nb_tabs.add(home_tab, text="Populares")
    search_tab = ttk.Frame(nb_tabs)
    nb_tabs.add(search_tab, text="Pesquisa")
    randomize_tab = ttk.Frame(nb_tabs)
    nb_tabs.add(randomize_tab, text="Random")


    ttk.Label(home_tab, text="Populares:", font="Calibri, 13").pack(pady=5, padx=5, fill='x')
    games = query_populars()
    game_catalog = GameCatalog(home_tab, games)
    game_catalog.pack(padx=20, fill='both', expand=True)

    


    window.mainloop()