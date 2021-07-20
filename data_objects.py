import sys
from global_collections import *
from typing import Dict, Optional


class Item:

    def __init__(self, name, display_name, description, narrative_text):
        self.name: str = name
        self.display_name: str = display_name
        self.description: str = description
        self.narrative_text: str = narrative_text
        self.takeable: bool = True

    def take(self):
        return self


class Room:

    def __init__(self, name, display_name, article, long_description, short_description, ):

        self.name: str = name
        self.display_name = display_name

        self.article = article

        self.visited = False

        self.long_description = long_description
        self.short_escription = short_description

        self.item_list: Dict[str, Item] = {}
        self.roomConnects: RoomConnectorMap

    def add_items(self, item_list: [Item]):
        self.item_list = item_list

    def get_description(self) -> str:
        if self.visited:
            description_str = ""
            for i in self.item_list.values():
                description_str += i.narrative_text + " "

            description_str += self.short_description
            return description_str
        else:
            self.visited = True
            return self.long_description

    # def createRoomConnectorMap(self):

    def take_item(self, item_name: str) -> str:
        if item_name in self.item_list:
            i = self.item_list.get(item_name)
            if i.takeable:
                self.item_list.pop[item_name]
                player_inventory[item_name] = i
                return f"You took the {i.display_name} and added it to your inventory."
            else:
                return f"You cannot take the {i.display_name}"
        else:
            return f"What {item_name} ???"


class ConnectorItem:
    def __init__(self,
                 room_name,
                 connector_item_name="",
                 article: str = "the"):

        self.connector_item: Optional[Item] = items.get(connector_item_name)
        self.room: Room = rooms.get(room_name)
        self.article: str = article

    def get_display_name(self) -> str:
        if self.connector_item is None:
            return self.room.display_name
        else:
            return self.connector_item.display_name


class RoomConnectorMap:

    def __init__(self,
                 north=None,
                 south=None,
                 east=None,
                 west=None,
                 up=None,
                 down=None):

        self.north: Optional[ConnectorItem] = north
        self.east: Optional[ConnectorItem] = east
        self.south: Optional[ConnectorItem] = south
        self.west: Optional[ConnectorItem] = west
        self.up: Optional[ConnectorItem] = rooms.get(up)
        self.down: Optional[ConnectorItem] = rooms.get(down)

    def printNarrative(self) -> str:
        narration = ""
        if self.north is not None: narration += f"to the NORTH is {self.north.connector_item.article} {self.north.connector_item.display_name},"
        if self.east is not None: narration += f"to the EAST is {self.east.connector_item.article} {self.east.connector_item.display_name},"
        if self.south is not None: narration += f"to the SOUTH is {self.south.connector_item.article} {self.south.connector_item.display_name},"
        if self.west is not None: narration += f"to the WEST is {self.west.connector_item.article} {self.west.connector_item.display_name},"
        if self.up is not None: narration += f"ABOVE you is {self.up.connector_item.article} {self.up.connector_item.display_name},"
        if self.down is not None: narration += f"BELOW you is {self.down.connector_item.article} {self.down.connector_item.display_name},"

        narration.rstrip(',')
        narration.capitalize()
        return narration

# class CollectiveItem(Item):
#     takenCount: int = 0
#
#     def __init__(self,
#                  name: str,
#                  display_name: str,
#                  description: str,
#                  narrative_text: str,
#                  singulardisplay_name: str,
#                  maxCount: int):
#
#         super().__init__(name, display_name, description, narrative_text)
#         self.singulardisplay_name = singulardisplay_name
#         self.maxCount = maxCount
#
#     def take(self):
#         if self.takenCount < self.maxCount:
#             returnItem = Item(self.name + str(self.takenCount), self.singulardisplay_name, sel)
#             self.takenCount += 1
#             return
#
# class Scenery(Item):
#
#     def __init__(self, name, display_name, description, narrative_text):
#         super().__init__(name, display_name, description, narrative_text)
#         self.takeable = False
