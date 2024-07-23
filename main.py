
if __name__ == "__main__":
    import tkinter as tk
    import ttkbootstrap as ttk
    from utils import *
    import random
    #Creates Root Window
    window = ttk.Window(themename="darkly")
    window.title("Roblox Interface+") 
    window.geometry("800x500")

    #Notebook and tabs
    nb_tabs = ttk.Notebook(window)
    nb_tabs.pack(expand=1,fill='both')
    home_tab = ttk.Frame(nb_tabs)
    nb_tabs.add(home_tab, text="Populares")
    search_tab = ttk.Frame(nb_tabs)
    nb_tabs.add(search_tab, text="Pesquisa")
    randomize_tab = ttk.Frame(nb_tabs)
    nb_tabs.add(randomize_tab, text="Random")

    #Populars tab
    populars_catalogue = ""
    def get_populars():
        global populars_catalogue
        if populars_catalogue != "":
            populars_catalogue.pack_forget()
        games = query_populars()
        populars_catalogue = GameCatalog(home_tab, games)
        populars_catalogue.pack(padx=20, fill='both', expand=True)

    ttk.Button(home_tab, text="Querry Populars", command=get_populars).pack()
    ttk.Label(home_tab, text="Populares:", font="Calibri, 13").pack(pady=5, padx=5, fill='x')
    
    #Search Tab
    search_catalogue = ""
    def search_button():
        global search_catalogue
        data = []
        querry = search_querry.get()
        if querry == "":
            data += query_main(search_quantity.get())
        else:    
            for i in querry.split(";"):
                data += query_data(i, search_quantity.get())

        blocked = list(block_querry.get().split(";"))
        for i in data:
            for j in blocked:
                if j.lower() in i["name"].lower():
                    data.remove(i)
                    continue
        reversed = False
        if selected_mode.get() == "Descending":
            reversed = True
        match selected_filter.get():
            case "Upvotes":
                data = [[i["totalUpVotes"], i] for i in data]
                data = sort_data(data, reversed)
            case "Player Count":

                data = [[i["playerCount"], i] for i in data]
                data = sort_data(data, reversed)
            case "Downvotes":
                data = [[i["totalDownVotes"], i] for i in data]
                data = sort_data(data, reversed)
            case _:
                pass
        if search_catalogue !="":
            search_catalogue.pack_forget()
        search_catalogue = GameCatalog(search_tab, data)
        search_catalogue.pack(padx=20, fill='both', expand=True)

    #Label Search Frame
    search_frame = ttk.Frame(search_tab)
    search_frame.pack(pady=[10,5])
    ttk.Label(search_frame, text="Search: ").pack(side='left', padx=[0,5])
    search_querry = tk.StringVar(value="Tycoon")
    ttk.Entry(search_frame,textvariable=search_querry, width=50).pack(side='left')
    ttk.Label(search_frame, text="Block: ").pack(side='left', padx=[15,5])
    block_querry = tk.StringVar(value="RP;Obby")
    ttk.Entry(search_frame,textvariable=block_querry, width=50).pack(side='left')
    
    #Options and button from
    options_frame = ttk.Frame(search_tab)
    options_frame.pack(pady=[5,10])
    selected_filter = tk.StringVar(value="Upvotes")
    dropdown = ttk.Combobox(options_frame, textvariable=selected_filter)
    dropdown['values'] = ("Upvotes", "Player Count", "Downvotes")
    dropdown.pack(side="left", padx=[0,10])
    selected_mode = tk.StringVar(value="Descending")
    dropdown_mode = ttk.Combobox(options_frame, textvariable=selected_mode)
    dropdown_mode['values'] = ("Ascending", "Descending")
    dropdown_mode.pack(side="left", padx=[10,10])
    ttk.Label(options_frame, text="Pages:").pack(side="left", padx=3)
    search_quantity = ttk.IntVar(value=1)
    ttk.Spinbox(options_frame, from_=1, to=100, textvariable=search_quantity, width=5).pack(side='left', padx=5)
    ttk.Button(options_frame,text="Search", command=search_button).pack(side="left", padx=[10,0])

    #Randomize:

    randomzie_catalogue = ""
    def random_button():
        global randomzie_catalogue
        data = []
        querry = randomize_search_querry.get()
        if querry == "":
            data += query_main(search_quantity.get())
        else: 
            for i in querry.split(";"):
                data += query_data(i, random_search_page_quantity.get())

        blocked = list(randomize_block_querry.get().split(";"))
        for i in data:
            for j in blocked:
                if j.lower() in i["name"].lower():
                    data.remove(i)
                    continue
        reversed = False
        if random_selected_mode.get() == "Descending":
            reversed = True
        match random_selected_filter.get():
            case "Upvotes":
                data = [[i["totalUpVotes"], i] for i in data]
                data = sort_data(data, reversed)
            case "Player Count":

                data = [[i["playerCount"], i] for i in data]
                data = sort_data(data, reversed)
            case "Downvotes":
                data = [[i["totalDownVotes"], i] for i in data]
                data = sort_data(data, reversed)
            case _:
                pass
        if randomzie_catalogue !="":
            randomzie_catalogue.pack_forget()
        quantity = random_search_quantity.get()
        data = random.choices(data, k=min(quantity, len(data)))
        randomzie_catalogue = GameCatalog(randomize_tab, data)
        randomzie_catalogue.pack(padx=20, fill='both', expand=True)

    randomize_search_frame = ttk.Frame(randomize_tab)
    randomize_search_frame.pack(pady=[10,5])
    ttk.Label(randomize_search_frame, text="Search: ").pack(side='left', padx=[0,5])
    randomize_search_querry = tk.StringVar(value="Tycoon")
    ttk.Entry(randomize_search_frame,textvariable=randomize_search_querry, width=50).pack(side='left')
    ttk.Label(randomize_search_frame, text="Block: ").pack(side='left', padx=[15,5])
    randomize_block_querry = tk.StringVar(value="RP;Obby")
    ttk.Entry(randomize_search_frame,textvariable=randomize_block_querry, width=50).pack(side='left')
    
    randomize_frame = ttk.Frame(randomize_tab)
    randomize_frame.pack(pady=[5,10])
    random_selected_filter = tk.StringVar(value="Upvotes")
    dropdown = ttk.Combobox(randomize_frame, textvariable=random_selected_filter)
    dropdown['values'] = ("Upvotes", "Player Count", "Downvotes")
    dropdown.pack(side="left", padx=[0,10])
    random_selected_mode = tk.StringVar(value="Descending")
    dropdown_mode = ttk.Combobox(randomize_frame, textvariable=random_selected_mode)
    dropdown_mode['values'] = ("Ascending", "Descending")
    dropdown_mode.pack(side="left", padx=[10,10])
    ttk.Label(randomize_frame, text="Pages:").pack(side="left", padx=3)
    random_search_page_quantity = ttk.IntVar(value=1)
    ttk.Spinbox(randomize_frame, from_=1, to=100, textvariable=random_search_page_quantity, width=5).pack(side='left', padx=5)
    ttk.Label(randomize_frame, text="Quantity:").pack(side="left", padx=3)
    random_search_quantity = ttk.IntVar(value=1)
    ttk.Spinbox(randomize_frame, from_=1, to=1000, textvariable=random_search_quantity, width=5).pack(side='left', padx=5)
    ttk.Button(randomize_frame,text="Search", command=random_button).pack(side="left", padx=[10,0])

    ttk.Label(randomize_tab, text="Results:", font="Calibri, 13").pack(pady=5, padx=5, fill='x')

    window.mainloop()