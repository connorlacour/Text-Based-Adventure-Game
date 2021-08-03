from typing import Optional, List, Dict

from game_objects.item_event import *
from game_objects.items import *


class China_Cabinet(SceneryItem):
    def __init__(self, description, events):
        super().__init__("china cabinet", "CHINA CABINET", description, events=events, article="a")
        self.locked = True
        self.collectable = True

    def take_pouch(self):
        self.collectable = False
        self.update_description()

    def lock_unlock(self):
        if self.locked:
            self.locked = False
        else:
            self.locked = True
        self.update_description()

    def update_description(self):
        self.description = "The China Cabinet is "
        if self.locked:
            self.description += "locked. You consider the value of the dinnerware, but the risk of breaking it ends that thought. "
        else:
            self.description += "unlocked. You consider the value of the dinnerware, but the risk of breaking it ends that thought."

        if self.collectable:
            self.description += " Just as you are turning away from the cabinet, you see a SMALL POUCH jutting out of a hidden corner not easily seen through the glass."


class Wall_Mount(SceneryItem):
    def __init__(self, description, events):
        super().__init__("wall mount", "WALL MOUNT", description, events=events, article="a")

    def take_key(self):
        self.collectable = False
        self.description = "There are various badges hanging from the WALL MOUNT from conferences and meetings."


def initialize_dining_room_scenery(items: list = None):
    cabinet = None
    mount = None

    if items is None:
        cabinet = China_Cabinet("The CHINA CABINET is locked.  You consider the value of the dinnerware, but the risk of breaking it ends that thought.  Just as you are turning away from the cabinet, you see a SMALL POUCH jutting out of a hidden corner not easily seen through the glass.", [{"unlock": "You unlock the china cabinet."}, {"lock": "You lock the china cabinet."}])
        mount = Wall_Mount("There are various badges hanging from the WALL MOUNT from conferences and meetings.  Hidden amongst those is a SMALL KEY.")
    else:
        for x in range(len(items)):
            if items[x].china_cabinet:
                cabinet = China_Cabinet(items[x].china_cabinet.desc, items[x].china_cabinet.events)
            elif items[x].wall_mount:
                mount = Wall_Mount(items[x].wall_mount.desc, items[x].wall_mount.events)

    return cabinet, mount
