from typing import Optional, List, Dict

from game_objects.item_event import *
from game_objects.items import *


class Fireplace(SceneryItem):
    def __init__(self, description, events):
        super().__init__("fireplace", "FIREPLACE", description, events=events, article="the")

    def take_burnt_note(self):
        self.description = "The FIREPLACE has a thin line of ash around the bottom that makes you think it has been used recently but the lack of warmth indicates that whoever used it is probably gone by now."


class Strip_of_Paper(SceneryItem):
    def __init__(self, description, events):
        super().__init__("strip of paper", "STRIP OF PAPER", description, events=events, article="a")


def initialize_living_room_scenery(items: list = None):
    fireplace = None,
    paper = None

    if items is None:
        fireplace = Fireplace("The FIREPLACE has a thin line of ash around the bottom that makes you think it has been used recently but the lack of warmth indicates that whoever used it is probably gone by now.  You are just about to turn away from the FIREPLACE when you see a BURNT NOTE stuck between the bottom logs.")
        paper = Strip_of_Paper("As you look closer at the STRIP OF PAPER, you notice that it is a receipt from John Little’s Lock & Key.")
    else:
        for x in range(len(items)):
            if items[x].fireplace:
                fireplace = Fireplace(items[x].fireplace.desc, items[x].fireplace.events)
            elif items[x].strip_of_paper:
                paper = Strip_of_Paper(items[x].strip_of_paper.desc, items[x].strip_of_paper.events)

    return fireplace, paper
