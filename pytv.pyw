import vlc
import tkinter
import json
import time


def stretch(bild, row, column):
    bild.grid_rowconfigure(row, weight=1)
    bild.grid_columnconfigure(column, weight=1)


def Player(videopanel, url):
    global player
    main.update()
    Instance = vlc.Instance('--network-caching=2000')
    player = Instance.media_player_new()
    player.set_mrl(url)
    player.set_hwnd(videopanel.winfo_id())
    player.audio_set_volume(100)
    player.play()


def gui(name, url):
    global player
    screen = tkinter.Toplevel(main)
    screen.title(name)
    screen.lift(aboveThis=main)
    screen.attributes('-fullscreen', True)
    screen.configure(background='black')
    stretch(screen, 0, 0)
    videopanel = tkinter.Frame(screen, bg="black")
    stretch(videopanel, 0, 0)
    panel_canvas = tkinter.Canvas(videopanel, bg="black", highlightbackground="black")
    panel_canvas.grid(row=0, column=0, rowspan=2)
    stretch(panel_canvas, 0, 0)
    videopanel.grid(row=0, column=0, rowspan=2, sticky="nwse")
    menupanel = tkinter.Frame(screen, bg="#252626", height="1")
    menupanel.grid(row=1, column=0, sticky="nwse")
    menupanel.grid_columnconfigure(3, weight=1)
    bilder_pfad = ["play_white.png", "pause_white.png",
                   "forward_white.png", "backward_white.png", "cross_white.png"]
    bilder_gui = []
    for i in range(1, (len(bilder_pfad)+1)):
        bilder_gui.append(tkinter.PhotoImage(file=bilder_pfad[i-1]))
        bilder_gui[i-1] = bilder_gui[i-1].subsample(12, 12)

    def media_control(control):
        if str(control) == "1":
            if player.is_playing():
                player.stop()
                media_buttons[0]["image"] = bilder_gui[0]
            else:
                player.play()
                media_buttons[0]["image"] = bilder_gui[1]
        elif str(control) == "2":
            print("2")
        elif str(control) == "3":
            print("3")
        elif str(control) == "4":
            player.stop()
            screen.destroy()
        else:
            print("Fehler")

    media_control_images = [bilder_gui[1], bilder_gui[3], bilder_gui[2], bilder_gui[4]]
    media_buttons = []
    for i in range(1, len(media_control_images)+1):
        media_buttons.append(tkinter.Button(menupanel, image=media_control_images[i-1],
                                            text="", activebackground="#252626",
                                            bg="#252626", border="0", width="50",
                                            command=lambda i=i: media_control(str(i))))

    def hover(e):
        zeit = 0.001
        for i in range(40):
            while menupanel["height"] < 40:
                menupanel["height"] = menupanel["height"] + 1
                main.update()
                zeit = float(zeit) + 0.0002
                time.sleep(float(zeit))
        if player.is_playing():
            media_buttons[0]["image"] = bilder_gui[1]
        else:
            media_buttons[0]["image"] = bilder_gui[0]
        media_buttons[1]["image"] = bilder_gui[3]
        media_buttons[2]["image"] = bilder_gui[2]
        media_buttons[3]["image"] = bilder_gui[4]
        for i in range(1, len(media_buttons)):
            media_buttons[i-1].grid(row=0, column=i-1, sticky="w")
        media_buttons[3].grid(row=0, column=3, sticky="e")

    def no_hover(e):
        time.sleep(1)
        for i in range(1, len(media_buttons)+1):
            media_buttons[i-1].grid_forget()
        zeit = 0.001
        for i in range(40):
            while menupanel["height"] > 1:
                menupanel["height"] = menupanel["height"] - 1
                main.update()
                zeit = float(zeit) + 0.0002
                time.sleep(float(zeit))

    menupanel.bind("<Enter>", hover)
    menupanel.bind("<Leave>", no_hover)
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
stretch(main, 1, 0)
main.bind("<MouseWheel>", scroll)

menu = tkinter.Frame(main, bg="#252626")
menu.grid(row=0, column=0, sticky="nwe")
menu_buttons = []
menu_items = ["Einstellungen", "Hilfe", "Über", "Beenden"]
for i in range(1, len(menu_items)+1):
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
