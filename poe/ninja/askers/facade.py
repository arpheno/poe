from constants import LEAGUE
from .curr import ask_ninja_curr
from .item import ask_ninja_item


def asker(type):
    if type in ["Fragment", "Currency"]:
        return ask_ninja_curr(type,league=LEAGUE)
    else:
        return ask_ninja_item(type,league=LEAGUE)
