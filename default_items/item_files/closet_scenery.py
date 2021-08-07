from typing import Optional, List, Dict

from game_objects.item_event import *
from game_objects.items import *

class Coat(SceneryItem):
    def __init__(self, description, events):
        super().__init__("coat", "COAT", description, events=events, article="a")

    def take_note(self):
        self.description = "The COAT pockets are empty."


def initialize_closet_scenery(items: list = None):
    coat = None,

    if items is None:
        coat = Coat("You search the COAT for clues about the owner.  As you dig around, your hand finds a piece of paper with a NOTE written on it.")
    else:
        for x in range(len(items)):
            if items[x].coat:
                coat = Coat(items[x].coat.desc, items[x].coat.events)

    return coat
    