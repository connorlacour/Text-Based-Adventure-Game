from typing import Optional, List, Dict

from game_objects.item_event import *
from game_objects.items import *


class Alarm(SceneryItem):
    def __init__(self, description, events):
        super().__init__("china cabinet", "CHINA CABINET", description, events=events, article="a")


class Large_Poster(SceneryItem):
    def __init__(self, description, events):
        super().__init__("wall mount", "WALL MOUNT", description, events=events, article="a")


class Red_Button(SceneryItem):
    def __init__(self, description, events):
        super().__init__("wall mount", "WALL MOUNT", description, events=events, article="a")


def initialize_up_hallway_scenery(items: list = None):
    alarm = None
    poster = None
    button = None

    if items is None:
        alarm = Alarm("The alarm appears to be quite old and outdated.  You are not even sure it’s fully mounted into the wall or whether it is simply hanging like a photo would be.  There is a RED BUTTON on the alarm.  Should you press it?")
        poster = Large_Poster("You see a poster of the night sky.  You search the poster trying to figure out what its meaning is when you recognize the bright star Vega, and from there, you trace the constellation Lyra in your mind.")
        button = Red_Button("A big shiny RED BUTTON", [{"press": "You stand frozen in place waiting for something to happen after pressing the button.  Finally after several seconds of holding your breath in anticipation, you let out a sigh of relief that nothing happened.  No good comes from pressing red buttons, you remind yourself.  And yet, when presented with one, it’s hard to resist the temptation."}])
    else:
        for x in range(len(items)):
            if items[x].alarm:
                alarm = Alarm(items[x].alarm.desc, items[x].alarm.events)
            elif items[x].large_poster:
                poster = Large_Poster(items[x].large_poster.desc, items[x].large_poster.events)
            elif items[x].red_button:
                button = Red_Button(items[x].red_button.desc, items[x].red_button.events)

    return alarm, poster, button
