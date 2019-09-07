
import tkinter as tk
from tkinter import messagebox as mb
from lib.interface.widgets import GameItemList, CreateGameForm, MainMenu
from lib.api import APIClient
from lib.models import Game


class GamesView(tk.Frame):
    def __init__(self, master):
        super().__init__(master=master)

        MainMenu(self).pack(fill=tk.X)

        tk.Button(self, text='Create new game', command=lambda: CreateGameForm(master, self.create_game)).pack(fill=tk.X)
        self.__game_list = GameItemList(self, delete_command=self.delete_game)
        self.__game_list.pack()

        self.__response = None

        self.__client = APIClient('http://localhost:8080/api')

        self.after(0, self.update)

    def update(self):

        if self.__response:
            if self.__response.done():
                if 'games' in self.__response.data:
                    raw_games = sort_games(self.__response.data['games'])
                    games = []

                    for game in raw_games:
                        games.append(Game.from_json_dict(game))

                    self.__game_list.update_game_list(games)

        self.__response = self.__client.get_games()
        self.after(1000, self.update)

    def create_game(self, limit, width, height):
        self.__client.create_game(limit, width, height)

    def delete_game(self, game: Game):
        if mb.askyesno("Delete game", "Do you want to delete game {}".format(game.name)):
            self.__client.delete_game(game.id)
            return True
        return False


def sort_games(games):
    empty_games = filter(lambda game: game['count'] == 0, games)
    full_games = filter(lambda game: game['count'] == game['limit'], games)
    relevant_games = filter(lambda game: 0 < game['count'] < game['limit'], games)

    result = []
    result += sorted(relevant_games, key=lambda game: (game['rate'], game['id']))
    result += sorted(empty_games, key=lambda game: (game['limit'], game['id']))
    result += sorted(full_games, key=lambda game: (game['count'], game['id']))

    return result

