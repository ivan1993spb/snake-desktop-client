
AUTHOR = "Ivan Pushkin"
VERSION = "v0.0.0"
LICENSE = "MIT"

WINDOW_TITLE = "Snake Online"

CLIENT_SOURCE_CODE_LINK = "https://github.com/ivan1993spb/snake-desktop-client"
CLIENT_ISSUES_LINK = "https://github.com/ivan1993spb/snake-desktop-client/issues"

SERVER_SOURCE_CODE_LINK = "https://github.com/ivan1993spb/snake-server"
SERVER_ISSUES_LINK = "https://github.com/ivan1993spb/snake-server/issues"

RULES_TITLE = "Game rules"

RULES = (
    "A player controls a snake.",
    "The task of the game is to grow the biggest snake.",
    "In order to achieve the goal players may eat apples, watermelons, small snakes and remains of dead "
    "snakes of other players.",
    "If a snake hits a wall the snake dies and the player starts again with a new small snake.",
    "A snake may eat another snake if it's length greater or equal to the square of length of the second one.",
)

ABOUT_TITLE = "About"

ABOUT = (
    "Client version: {}".format(VERSION),
    "License: {}".format(LICENSE),
    "Author: {}".format(AUTHOR),
    "Client source code: {}".format(SERVER_SOURCE_CODE_LINK),
    "Issues: {}".format(SERVER_ISSUES_LINK),
)

CONTROL_TITLE = "Control"

CONTROL = "Use arrows, WASD, IJKL or mouse"

WELCOME_MESSAGE = "Welcome to snake online arcade game!"
