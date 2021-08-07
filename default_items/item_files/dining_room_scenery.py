from typing import Optional, List, Dict

from game_objects.item_event import *
from game_objects.items import *

#STILL NEEDS WORK
class China_Cabinet(SceneryItem):
    def __init__(self, description, events):
        super().__init__("microwave", "MICROWAVE", description, events=events, article="a")
        self.locked = True
        self.collectable = True

    def take_pouch(self):
        self.collectable = False

    def lock_unlock(self):
        if self.locked:
            self.locked = False
            if self.collectable:
                self.description = "The China Cabinet is unlocked. You consider the value of the dinnerware, but the risk of breaking it ends that thought. Just as you are turning away from the cabinet, you see a SMALL POUCH jutting out of a hidden corner not easily seen through the glass."
            else:
                self.description = "The CHINA CABINET is unlocked.  You consider the value of the dinnerware, but the risk of breaking it ends that thought."
        else:
            self.locked = True
            if self.collectable:
                self.description = "The CHINA CABINET is locked.  You consider the value of the dinnerware, but the risk of breaking it ends that thought.  Just as you are turning away from the cabinet, you see a SMALL POUCH jutting out of a hidden corner not easily seen through the glass."
            else:
                self.description = "The CHINA CABINET is locked.  You consider the value of the dinnerware, but the risk of breaking it ends that thought."


class Wall_Mount(SceneryItem):
    def __init__(self, description, events):
        super().__init__("island", "ISLAND", description, events=events, article="the")


def initialize_dining_room_scenery(items: list = None):
    cabinet = None,
    mount = None

    if items is None:
        cabinet = China_Cabinet("The CHINA CABINET is locked.  You consider the value of the dinnerware, but the risk of breaking it ends that thought.  Just as you are turning away from the cabinet, you see a SMALL POUCH jutting out of a hidden corner not easily seen through the glass.")
        mount = Wall_Mount("There are various badges hanging from the WALL MOUNT from conferences and meetings.  Hidden amongst those is a SMALL KEY.")
    else:
        for x in range(len(items)):
            if items[x].china_cabinet:
                cabinet = China_Cabinet(items[x].china_cabinet.desc, items[x].china_cabinet.events)
            elif items[x].wall_mount:
                mount = Wall_Mount(items[x].wall_mount.desc, items[x].wall_mount.events)

    return cabinet, mount
    