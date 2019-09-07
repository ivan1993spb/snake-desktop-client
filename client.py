import tkinter as tk
from tkinter import ttk
from lib.interface.widgets import LabelCounter, Article, LabelMapSize, LabelCapacity, Parameter, GameItem, \
    GameItemList, StatusBar, CreateGameForm, ServerRadiobutton, ServerRadiobuttonList
import random
from lib.info import ABOUT, WINDOW_TITLE
from lib.models import rand_game, local_server
from lib.interface.views import GamesView


LARGE_FONT = ("Verdana", 12)


class Application(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)
        tk.Tk.wm_title(self, WINDOW_TITLE)
        self.minsize(600, 420)

        games_view = GamesView(self)
        games_view.pack(fill=tk.BOTH, expand=True)

        status = StatusBar(self)
        status.pack(fill=tk.X)


class SeaofBTCapp(tk.Tk):

    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        # tk.Tk.iconbitmap(self, default='clienticon.ico')
        tk.Tk.wm_title(self, WINDOW_TITLE)

        container = tk.Frame(self)
        container.pack(side="top", fill="both", expand=True)
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for F in (StartPage, PageOne, PageTwo):
            frame = F(container, self)
            self.frames[F] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, cont):
        frame = self.frames[cont]
        frame.tkraise()


class StartPage(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)

        label = ttk.Label(self, text="Start Page", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button = ttk.Button(self, text="Visit Page 1",
                            command=lambda: controller.show_frame(PageOne))
        button.pack()

        button2 = ttk.Button(self, text="Visit Page 2",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()

        lc = LabelCounter(self, "LABEL")
        lc.pack()

        button3 = ttk.Button(self, text="update",
                             command=lambda: lc.update_counter(random.randint(0, 100), random.randint(0, 100)))
        button3.pack()


class PageOne(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page One!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page Two",
                             command=lambda: controller.show_frame(PageTwo))
        button2.pack()


class PageTwo(tk.Frame):

    def __init__(self, parent, controller):
        tk.Frame.__init__(self, parent)
        label = ttk.Label(self, text="Page Two!!!", font=LARGE_FONT)
        label.pack(pady=10, padx=10)

        button1 = ttk.Button(self, text="Back to Home",
                             command=lambda: controller.show_frame(StartPage))
        button1.pack()

        button2 = ttk.Button(self, text="Page One",
                             command=lambda: controller.show_frame(PageOne))
        button2.pack()

        gil = GameItemList(self, [rand_game() for _ in range(0, 0)])
        gil.pack()

        sb = StatusBar(self)
        sb.pack()

        ServerRadiobuttonList(self, servers=[], default=0).pack()


app = Application()

# menu = tk.Menu(app)
# app.config(menu=menu)
#
#
# def callback():
#     CreateGameToplevel(app)
#
#
# filemenu = tk.Menu(menu)
# menu.add_cascade(label="Game", menu=filemenu)
# filemenu.add_command(label="New", command=callback)
# filemenu.add_command(label="Exit", command=callback)
#
# serversmenu = tk.Menu(menu)
# menu.add_cascade(label="Servers", menu=serversmenu)
# serversmenu.add_command(label="Server 1", command=callback)
# serversmenu.add_command(label="Server 2", command=callback)
#
#
# helpmenu = tk.Menu(menu)
# menu.add_cascade(label="Help", menu=helpmenu)
# helpmenu.add_command(label="Rules", command=callback)
# helpmenu.add_command(label="About...", command=callback)

app.mainloop()
