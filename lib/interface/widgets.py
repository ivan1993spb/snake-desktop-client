import re
import webbrowser
import functools
import typing
import math

import tkinter as tk
from tkinter import messagebox as mb

from lib.interface.managers import HyperlinkManager
from lib.models import Game, zero_game, Server


class LabelIntValue(tk.Label):

    def __init__(self, master, text: str, value=0, width=None):
        self.__value = value
        self.__text = text
        super().__init__(master=master, text=self.__format(), width=width)

    def __format(self):
        return '{}: {}'.format(self.__text, self.__value)

    def update_value(self, value: int):
        self.__value = value
        self.config(text=self.__format())


class LabelCounter(tk.Label):

    def __init__(self, master, text: str, count=0, limit=0):
        self.__count = count
        self.__limit = limit
        self.__text = text
        super().__init__(master=master,
                         text=self.__format(),
                         foreground=self.__color(),
                         width=15)

    def __format(self):
        if self.__text is None:
            return '{}/{}'.format(self.__count, self.__limit)
        return '{}: {}/{}'.format(self.__text, self.__count, self.__limit)

    def __color(self):
        return 'green' if self.__count < self.__limit else 'red'

    def update_counter(self, count: int, limit: int):
        self.__count = count
        self.__limit = limit
        self.config(foreground=self.__color(), text=self.__format())


class LabelMapSize(tk.Label):
    def __init__(self, master, width=0, height=0):
        self.__width = width
        self.__height = height
        super().__init__(master=master,
                         text=self.__format(),
                         background='#bbb',
                         width=12)

    def __format(self):
        return 'Map: {}x{}'.format(self.__width, self.__height)

    def update_size(self, width: int, height: int):
        self.__width = width
        self.__height = height
        self.config(text=self.__format())


class Article(tk.LabelFrame):
    def __init__(self, master, title: str, height, width, text: str):
        super().__init__(master, text=title, padx=10, pady=10, font='Arial 20')
        self.__text = tk.Text(self, height=height, width=width, font='Arial 14', wrap=tk.WORD, background='#cecece')
        self.__hyperlink_manager = HyperlinkManager(self.__text)
        self.__text.pack()
        self.update_text(text)

    @staticmethod
    def __handle_link_click(url):
        webbrowser.open(url)

    def update_text(self, text: str):
        self.__text.configure(state=tk.NORMAL)

        cursor = 0
        expr = re.compile(r'https?://[^\s]+')

        for m in expr.finditer(text):
            start, end = m.span()
            if cursor < start:
                self.__text.insert(tk.END, text[cursor:start])
            url = text[start:end]
            action = functools.partial(self.__handle_link_click, url)
            self.__text.insert(tk.END, url, self.__hyperlink_manager.add(action))
            cursor = end

        self.__text.insert(tk.END, text[cursor:])

        self.__text.configure(state=tk.DISABLED)


class LabelCapacity(tk.Label):
    def __init__(self, master, **kw):
        self.__capacity = 0.0
        super().__init__(master=master, text=self.__format(), **kw)

    def __format(self):
        if 0 < self.__capacity < 1:
            return "Server capacity {0:.2f} %".format(self.__capacity)
        return "Server capacity {} %".format(int(self.__capacity))

    def update_capacity(self, capacity: float):
        self.__capacity = capacity
        self.config(text=self.__format())


class Parameter(tk.Frame):
    def __init__(self, master, text: str, from_: int, to: int):
        super().__init__(master=master)

        self.__var = tk.IntVar(value=from_)

        self.__label = tk.Label(master=self, text=text)
        self.__label.pack(side=tk.LEFT)

        self.__scale = tk.Scale(master=self, from_=from_, to=to, orient=tk.HORIZONTAL, showvalue=0, variable=self.__var)
        self.__scale.pack(side=tk.LEFT)

        self.__entry = tk.Entry(master=self, textvariable=self.__var)
        self.__entry.pack(side=tk.LEFT)

    def get_value(self) -> int:
        return self.__var.get()


class HyperlinkButton(tk.Label):
    def __init__(self, master, text: str, func: callable = None, width=None):
        super().__init__(master=master, text=text, fg="blue", cursor="hand2", width=width)
        if func:
            self.bind("<Button-1>", func)

    def update_hyperlink(self, text: str, func: callable = None):
        self.config(text=text)
        if func:
            self.unbind("<Button-1>")
            self.bind("<Button-1>", func)


class GameItem(tk.Frame):
    def __init__(self, master, game=zero_game(), delete_command: callable = None):
        super().__init__(master=master)

        self.__delete_command = delete_command

        self.__hyperlink = HyperlinkButton(self, text=game.name, width=20)
        self.__hyperlink.pack(side=tk.LEFT)
        # self.__hyperlink.grid(row=0, column=1)

        self.__map_size = LabelMapSize(self, game.width, game.height)
        self.__map_size.pack(side=tk.LEFT)
        # self.__map_size.grid(row=0, column=2)

        self.__player_count = LabelCounter(self, "Players", game.count, game.limit)
        self.__player_count.pack(side=tk.LEFT)
        # self.__player_count.grid(row=0, column=3)

        self.__rate = LabelIntValue(self, text="Rate", value=game.rate, width=15)
        self.__rate.pack(side=tk.LEFT)
        # self.__rate.grid(row=0, column=4)

        self.__delete_button = tk.Button(self,
                                         text="Delete",
                                         state=tk.NORMAL if game.deletable() else tk.DISABLED,
                                         command=self.__command)
        self.__delete_button.pack(side=tk.RIGHT)
        # self.__delete_button.grid(row=0, column=5)

        self.__game = game

    def update_game(self, game: Game):
        self.__hyperlink.update_hyperlink(game.name)
        self.__map_size.update_size(game.width, game.height)
        self.__player_count.update_counter(game.count, game.limit)
        self.__rate.update_value(game.rate)
        self.__delete_button.config(state=tk.NORMAL if game.deletable() else tk.DISABLED)
        self.__game = game

    def __command(self):
        if self.__delete_command:
            self.__delete_command(self.__game)


class GameItemList(tk.Frame):
    BUTTON_TEXT_PREV = 'Prev'
    BUTTON_TEXT_NEXT = 'Next'

    GAME_ITEMS_PER_PAGE = 10

    EMPTY_MESSAGE = "Empty"

    def __init__(self, master, games: typing.List[Game] = None, delete_command: callable = None):
        super().__init__(master=master)

        if games is None:
            games = []

        self.__current_page = 0
        self.__games = []
        self.__game_items = []
        self.__delete_command = delete_command

        self.__list_frame = tk.Frame(self)
        self.__list_frame.pack()

        self.__buttons_frame = tk.Frame(self)
        self.__buttons_frame.pack()

        self.__page_counter = LabelCounter(self.__buttons_frame, "Page")
        self.__page_counter.pack(side=tk.LEFT)
        self.__button_prev = tk.Button(self.__buttons_frame, text=self.BUTTON_TEXT_PREV, command=self.__click_prev)
        self.__button_prev.pack(side=tk.LEFT)
        self.__button_next = tk.Button(self.__buttons_frame, text=self.BUTTON_TEXT_NEXT, command=self.__click_next)
        self.__button_next.pack(side=tk.LEFT)

        self.__empty_message = None

        self.update_game_list(games)

    def update_game_list(self, games: typing.List[Game]):
        games_number_changed = len(games) != len(self.__games)

        if games_number_changed:
            self.__current_page = 0

        self.__games = games
        self.__draw_list()
        self.__update_buttons_frame()

    def __draw_list(self):
        pages = tuple(self.__get_pages())

        if self.__current_page >= len(pages):
            self.__current_page = 0

        if not self.__games:
            while self.__game_items:
                self.__game_items.pop().destroy()
            if not self.__empty_message:
                self.__empty_message = tk.Label(self.__list_frame, text=self.EMPTY_MESSAGE)
                self.__empty_message.pack(anchor='center')
            return
        elif self.__empty_message:
            self.__empty_message.destroy()
            self.__empty_message = None

        try:
            games = tuple(self.__games[i] for i in pages[self.__current_page])

            while len(self.__game_items) < len(games):
                game_item = GameItem(self.__list_frame, delete_command=self.__command)
                game_item.pack(fill=tk.X)
                self.__game_items.append(game_item)

            while len(self.__game_items) > len(games):
                game_item = self.__game_items.pop()
                game_item.destroy()

            for game, game_item in zip(games, self.__game_items):
                game_item.update_game(game)
        except IndexError as e:
            self.__current_page = 0
            self.__game_items = []
            print(e)

    def __click_next(self):
        pages_count = self.__get_pages_count()
        self.__current_page = self.__current_page + 1 if self.__current_page < pages_count else pages_count
        self.__update_buttons_frame()
        self.__draw_list()

    def __click_prev(self):
        self.__current_page = self.__current_page - 1 if self.__current_page > 0 else 0
        self.__update_buttons_frame()
        self.__draw_list()

    def __update_buttons_frame(self):
        pages_count = self.__get_pages_count()
        current_page_number = 0 if not self.__games else self.__current_page + 1
        self.__page_counter.update_counter(current_page_number, pages_count)

        if self.__current_page == 0:
            self.__button_prev.config(state=tk.DISABLED)
        else:
            self.__button_prev.config(state=tk.NORMAL)

        if self.__current_page + 1 < pages_count:
            self.__button_next.config(state=tk.NORMAL)
        else:
            self.__button_next.config(state=tk.DISABLED)

    def __get_pages_count(self):
        return math.ceil(len(self.__games)/self.GAME_ITEMS_PER_PAGE)

    def __get_pages(self):
        count = len(self.__games)
        per_page = self.GAME_ITEMS_PER_PAGE

        for start in range(0, count, per_page):
            yield tuple(range(start, min(start + per_page, count)))

    def __command(self, game: Game):
        if self.__delete_command:
            flag = self.__delete_command(game)
            if flag:
                games = filter(lambda g: g.id != game.id, self.__games)
                self.update_game_list(list(games))


class StatusBar(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.label = LabelCapacity(self, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.label.pack(fill=tk.X)

    def set(self, capacity):
        self.label.update_capacity(capacity)


class CreateGameForm(tk.Frame):
    FORM_TITLE_MAP = "Map size"
    FORM_TITLE_PLAYERS = "Players"

    LABEL_WIDTH_TEXT = "Width"
    LABEL_HEIGHT_TEXT = "Height"
    LABEL_PLAYERS_TEXT = "Limit"

    SUBMIT_TEXT = "Submit"

    MAP_SIZE_MIN_WIDTH = 8
    MAP_SIZE_MAX_WIDTH = 255
    MAP_SIZE_MIN_HEIGHT = 8
    MAP_SIZE_MAX_HEIGHT = 255

    PLAYERS_MIN = 1
    PLAYERS_MAX = 100

    def __init__(self, master, func: callable = None):
        super().__init__(master, takefocus=True)

        self.__func = func

        frame_map = tk.LabelFrame(self, text=self.FORM_TITLE_MAP)
        frame_map.pack(fill=tk.X)

        self.__param_width = Parameter(frame_map,
                                       self.LABEL_WIDTH_TEXT,
                                       self.MAP_SIZE_MIN_WIDTH,
                                       self.MAP_SIZE_MAX_WIDTH)
        self.__param_width.pack()
        self.__param_height = Parameter(frame_map,
                                        self.LABEL_HEIGHT_TEXT,
                                        self.MAP_SIZE_MIN_HEIGHT,
                                        self.MAP_SIZE_MAX_HEIGHT)
        self.__param_height.pack()

        frame_players = tk.LabelFrame(self, text=self.FORM_TITLE_PLAYERS)
        frame_players.pack(fill=tk.X)
        self.__param_players_limit = Parameter(frame_players,
                                               self.LABEL_PLAYERS_TEXT,
                                               self.PLAYERS_MIN,
                                               self.PLAYERS_MAX)
        self.__param_players_limit.pack()

        button = tk.Button(self, text=self.SUBMIT_TEXT, command=self.submit)
        button.pack(fill=tk.X)

    def submit(self):
        if self.__func:
            limit = self.__param_players_limit.get_value()
            width = self.__param_width.get_value()
            height = self.__param_height.get_value()
            self.__func(limit, width, height)

        self.destroy()


class ServerRadiobutton(tk.Frame):
    def __init__(self, master, server: Server, variable, value):
        super().__init__(master=master)

        self.__radio = tk.Radiobutton(self, variable=variable, value=value)
        self.__radio.pack(side=tk.LEFT)

        self.__name = HyperlinkButton(self, text=server.name, func=lambda _: self.__radio.select())
        self.__name.pack(side=tk.LEFT)

        self.__address = HyperlinkButton(self, text=server.address, func=lambda _: self.__radio.select())
        self.__address.pack(side=tk.LEFT)

        self.__server = server


class ServerRadiobuttonList(tk.Frame):
    EMPTY_SERVER_LIST_TEXT = "Empty server list"

    def __init__(self, master, servers: typing.List[Server], default: int):
        super().__init__(master=master)

        self.__servers = servers
        self.__var = tk.IntVar(value=default)

        if self.__servers:
            for i, server in enumerate(servers):
                radio = ServerRadiobutton(self, server, self.__var, i)
                radio.pack()
        else:
            tk.Label(self, text=self.EMPTY_SERVER_LIST_TEXT).pack()

    def selected(self) -> Server:
        return self.__servers[self.__var.get()] if self.__servers else None


class MenuButton(tk.Button):
    PADDING = 12

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs,
                         padx=self.PADDING,
                         pady=self.PADDING,
                         background='#666',
                         activebackground='#aaa',
                         foreground='#ddd',
                         activeforeground='#fff',
                         font=("Helvetica", 14, "bold"))


class MainMenu(tk.Frame):

    BUTTONS = (
        "Games",
        "Rules",
        "About",
        "Server",
    )

    def __init__(self, master):
        super().__init__(master=master)

        for i, button_text in enumerate(self.BUTTONS):
            tk.Grid.columnconfigure(self, i, weight=1)
            MenuButton(self, text=button_text).grid(row=0, column=i, sticky=tk.N+tk.S+tk.E+tk.W)


todo = r"""
TODO:
- Welcome message widget (or tab man title)
- Menu
"""
