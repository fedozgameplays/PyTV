import vlc
import tkinter
import json


def Player(videopanel, url):
    main.update()
    Instance = vlc.Instance('--network-caching=2000')
    player = Instance.media_player_new()
    player.set_mrl(url)
    player.set_hwnd(videopanel.winfo_id())
    player.audio_set_volume(100)
    player.play()


def gui(name, url):
    screen = tkinter.Toplevel(main)
    screen.title(name)
    screen.lift(aboveThis=main)
    screen.attributes('-fullscreen', True)
    screen.configure(background='black')
    videopanel = tkinter.Frame(screen, bg="black")
    tkinter.Canvas(videopanel, bg="black").pack(fill=tkinter.BOTH, expand=1)
    videopanel.pack(fill=tkinter.BOTH, expand=1)
    title = ("Lade {}...".format(name))
    l1 = tkinter.Label(videopanel, text=title, font=("Courier", 44), fg="white", bg="black")
    l1.pack()
    Player(videopanel, url)


def sender(nummer):
    global sender_json
    name = sender_json["sender"][nummer]["name"]
    url = sender_json["sender"][nummer]["url"]
    gui(name, url)


def menu_option(nummer):
    if nummer == "1":
        print("Einstellungen")
    elif nummer == "2":
        print("Hilfe")
    elif nummer == "3":
        print("Über")
    else:
        main.destroy()


def scroll(e):
    auswahl_canvas.configure(scrollregion=auswahl_canvas.bbox("all"))
    auswahl_canvas.yview_scroll(int(-1*(e.delta/120)), "units")


main = tkinter.Tk()
main.title("PyTV")
main.geometry("1280x720")
main.configure(background="#252626")
main.grid_rowconfigure(1, weight=1)
main.grid_columnconfigure(0, weight=1)
main.bind("<MouseWheel>", scroll)

menu = tkinter.Frame(main, bg="#252626")
menu.grid(row=0, column=0, sticky="nwe")
menu_buttons = []
menu_items = ["Einstellungen", "Hilfe", "Über", "Beenden"]
for i in range(1, 5):
    menu_buttons.append(tkinter.Button(menu, text=menu_items[i-1], relief="flat", bg="#252626",
                                       fg="white", padx="20", command=lambda i=i: menu_option(i)))
    menu_buttons[i-1].grid(row=0, column=i-1)


with open("sender.json") as file:
    sender_json = json.load(file)
länge = len(sender_json["sender"])
namen = []
for tv_sender in sender_json["sender"]:
    namen.append(tv_sender["name"])

auswahl_canvas = tkinter.Canvas(main, highlightbackground="#252626")
auswahl_canvas.grid(row=1, column=0, sticky="nswe")
auswahl = tkinter.Frame(auswahl_canvas, highlightbackground="#252626",
                        highlightcolor="#0e7bf7", highlightthickness="1")
auswahl.grid(row=1, column=0, sticky="nwse")
auswahl.grid_columnconfigure(0, weight=1)
auswahl_canvas.create_window(0, 0, window=auswahl, anchor="nw", width="1280")
button = []
bilder = []

for i in range(1, länge+1):
    bilder.append(tkinter.PhotoImage(file="images/{}.png".format(i-1)))
    button.append(tkinter.Button(auswahl, text=namen[i-1], image=bilder[i-1], anchor="w",
                                 padx="20", bg="#252626", compound="left", relief="flat",
                                 fg="white", command=lambda i=i: sender(i-1)))
    if i % 2 == 0:
        button[i-1]["bg"] = "#252626"
    else:
        button[i-1]["bg"] = "#3e4242"
    bilder[i-1] = bilder[i-1].subsample(2, 2)
    button[i-1].grid(row=(i), column=0, sticky="wse")
    button[i-1]["image"] = bilder[i-1]

    def hover(nummer):
        button[nummer]["bg"] = "#446284"

    def no_hover(nummer):
        if (nummer+1) % 2 == 0:
            button[nummer]["bg"] = "#252626"
        else:
            button[nummer]["bg"] = "#3e4242"
    button[i-1].bind("<Enter>", lambda event, i=i: hover(i-1))
    button[i-1].bind("<Leave>", lambda event, i=i: no_hover(i-1))

main.mainloop()
