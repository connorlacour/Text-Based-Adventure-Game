from typing import Optional, List, Dict

from game_objects.item_event import *
from game_objects.items import *


class Microwave(SceneryItem):
    def __init__(self, description, events):
        super().__init__("microwave", "MICROWAVE", description, events=events, article="a")

    def take_fast_food(self):
        self.description = "The MICROWAVE is cold and empty."


class Island(SceneryItem):
    def __init__(self, description, events):
        super().__init__("island", "ISLAND", description, events=events, article="the")


class Blue_Jar(SceneryItem):
    def __init__(self, description, events):
        super().__init__("blue jar", "BLUE JAR", description, events=events, article="a")


def initialize_kitchen_scenery(items: list = None):
    microwave = None,
    island = None
    jar = None

    if items is None:
        microwave = Microwave("The MICROWAVE emits an occasional beep.  You try to peer in the dark door, seeing a small container of FAST FOOD sitting in the middle for reheating.  You put your hand on the door.  It is cool to the touch.")
        island = Island("Going over to the ISLAND, you see a bowl of fruit with vibrant red APPLES and a BLUE JAR with a paw print on it.")
        jar = Blue_Jar("You pull back the lid on the BLUE JAR to find DOG TREATS that smell strongly of bacon.")
    else:
        for x in range(len(items)):
            if items[x].microwave:
                microwave = Microwave(items[x].microwave.desc, items[x].microwave.events)
            elif items[x].island:
                island = Island(items[x].island.desc, items[x].island.events)
            elif items[x].blue_jar:
                jar = Blue_Jar(items[x].blue_jar.desc, items[x].blue_jar.events)

    return microwave, island, jar
    