from typing import Optional, List, Dict

from game_objects.item_event import *
from game_objects.items import *


class Chairs(SceneryItem):
    def __init__(self, description, events):
        super().__init__("chairs", "CHAIRS", description, events=events, article="the")


class Small_Table(SceneryItem):
    def __init__(self, description, events):
        super().__init__("small table", "SMALL TABLE", description, events=events, article="a")

    def take_notepad(self):
        self.description = "The SMALL TABLE is empty"


class Desk(SceneryItem):
    def __init__(self, description, events):
        super().__init__("desk", "DESK", description, events=events, article="a")


def initialize_foyer_scenery(items: list = None):
    chairs = None,
    small_table = None
    desk = None

    if items is None:
        chairs = Chairs("The CHAIRS appear to be normal, waiting room chairs for visitors.  They sit around a SMALL TABLE.")
        small_table = Small_Table("On the SMALL TABLE is a blank NOTEPAD that appears to have had the top page hastily ripped off.")
        desk = Desk("The DESK is relatively bare.  You see a line of walkie talkies and some pens.")
    else:
        for x in range(len(items)):
            if items[x].chairs:
                chairs = Chairs(items[x].chairs.desc, items[x].chairs.events)
            elif items[x].small_table:
                small_table = Small_Table(items[x].small_table.desc, items[x].small_table.events)
            elif items[x].desk:
                desk = Small_Table(items[x].desk.desc, items[x].desk.events)

    return chairs, small_table, desk
