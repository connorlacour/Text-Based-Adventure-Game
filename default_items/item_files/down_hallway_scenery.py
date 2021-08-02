from typing import Optional, List, Dict

from game_objects.item_event import *
from game_objects.items import *

class Painting(SceneryItem):
    def __init__(self, description, events):
        super().__init__("painting", "PAINTING", description, events=events, article="a")


class Podium(SceneryItem):
    def __init__(self, description, events):
        super().__init__("podium", "PODIUM", description, events=events, article="a")


class Guest_Book(SceneryItem):
    def __init__(self, description, events):
        super().__init__("guest book", "GUEST BOOK", description, events=events, article="a")


def initialize_down_hallway_scenery(items: list = None):
    painting = None,
    podium = None
    guest_book = None

    if items is None:
        painting = Painting("The PAINTING depicts a cave.  Through the mouth of the cave is a brilliant light.  Inside is a man, with his back to the mouth of the cave, staring at the shadows cast by the jagged rocks reaching from the floor and the ceiling behind him.")
        podium = Podium("Looking in the glass case on the PODIUM, you see a GUEST BOOK.")
        guest_book = Guest_Book("The last name entered in the GUEST BOOK you see is John Little.")
    else:
        for x in range(len(items)):
            if items[x].painting:
                painting = Painting(items[x].painting.desc, items[x].painting.events)
            elif items[x].podium:
                podium = Podium(items[x].podium.desc, items[x].podium.events)
            elif items[x].guest_book:
                guest_book = Guest_Book(items[x].guest_book.desc, items[x].guest_book.events)

    return painting, podium, guest_book
    