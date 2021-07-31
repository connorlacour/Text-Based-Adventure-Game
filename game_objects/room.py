from __future__ import annotations  # Enables forward type hints
from typing import List, Dict, Optional

from game_objects.game_util import print_warning, warning_item_not_found
from game_objects.items import Item, CollectiveItem, InventoryItem


class Room:

    def __init__(self,
                 name,
                 display_name,
                 article,
                 long_description,
                 short_description,
                 item_setup_dict=None,
                 room_list: List[RoomConnector] = None):

        self.name: str = name
        self.display_name = display_name

        self.article = article
        self.visited = False

        self.long_description = long_description
        self.short_description = short_description

        self.item_setup_dict = item_setup_dict if item_setup_dict is not None else {}
        self.room_list = room_list if room_list is not None else []

        self.item_list: Dict[str, RoomItem] = {key: RoomItem(key, value) for (key, value) in
                                               self.item_setup_dict.items()}
        self.discarded_items: List[Item] = []
        self.connecting_rooms: Dict[str, RoomConnector] = {v.direction: v for v in self.room_list}

    # initialize rooms
    def setup_on_start(self):

        for connector in self.connecting_rooms.values():
            connector.setup_on_start()

        for room_item in self.item_list.values():
            room_item.setup_on_start()

            # Separate initializer method for item list to simplify constructor

    def set_item_list(self, item_description_dict: Dict[str, str]):
        self.item_list = {key: RoomItem(key, value) for (key, value) in item_description_dict.items()}

    def add_item(self, item: RoomItem): self.item_list[item.item.name] = item

    def delete_item(self, item: RoomItem):
        if item.item.name in self.item_list:
            del self.item_list[item.item.name]
        else:
            print_warning(f"Couldn't delete {item.item.name} from {self.name}, doesn't exist")

    # Separate initializer method for room list to simplify constructor
    def set_room_map(self, connector_list: List[RoomConnector]):
        self.connecting_rooms = {v.direction: v for v in connector_list}

    def get_item_from_room(self, item_name) -> Optional[RoomItem]:
        item = self.item_list.get(item_name)
        if item is not None:
            return item
        else:
            print_warning(f"{item_name} not found in {self.name}")
            return None

    def get_discarded_item_list(self) -> Dict[str, Item]:
        return {key: value for (key, value) in self.item_list.items() if value.item.discarded}

    # EX:  There are STAIRS heading UPWARDS leading to a BATHROOM. BEHIND you is the FOYER.
    def room_list_narration(self) -> str:
        narration = ""
        for roomConnector in self.connecting_rooms.values():
            narration += roomConnector.get_narration() + ". "
        return narration

    # EX:  CHAIRS litter the ground and PLATES are scattered on the a DINING TABLE.
    def item_list_narration(self) -> str:
        narration = ""
        for i in self.item_list.values():
            narration += i.narration
        return narration

    def get_room_narration(self) -> str:
        if self.visited:
            return self.short_description + " " + self.item_list_narration() + "\n" + self.room_list_narration()

        else:
            self.visited = True
            return self.long_description + "\n" + self.room_list_narration()

    def take_item(self, item_name: str) -> str:
        from game_objects.global_collections import player_inventory

        item_to_take = self.item_list.get(item_name)
        if item_to_take is not None:
            if item_to_take.item.can_take:

                if isinstance(item_to_take.item, CollectiveItem):
                    new_single_item: InventoryItem = item_to_take.item.new_singular_item()
                    player_inventory[new_single_item.name] = new_single_item
                    return f"You grabbed a {new_single_item.display_name} " \
                           f"from the {item_to_take.item.display_name} and added it to your inventory."

                else:
                    player_inventory[item_name] = item_to_take.item.take
                    del self.item_list[item_name]
                    return f"You took the {item_to_take.item.display_name} and added it to your inventory."

            else:
                return f"You cannot take the {item_to_take.item.display_name}"
        else:
            return f"What {item_name} ???"

    def discard_item(self, item_name: str, must_be_in_inventory=True) -> str:
        from game_objects.global_collections import player_inventory, find_room_item

        item_to_discard = player_inventory.get(item_name)
        if item_to_discard is not None:
            self.discarded_items.append(item_to_discard)
            del player_inventory[item_name]
            return f"You dropped the {item_name} to the ground."
        elif must_be_in_inventory:
            return f"You don't have {item_to_discard.article} {item_name}, genius!"
        else:
            room, item_to_discard = find_room_item(item_name)
            room.delete_item(item_to_discard)
            self.discarded_items.append(item_to_discard)
            return f"You dropped {item_to_discard.item.article} {item_to_discard.item.display_name}"

    def __str__(self):
        return self.name

# Data object to bundle an item name and item narration together allowing us to more
#   intuitively initialize room descriptions
class RoomItem:

    def __init__(self, item_name, narration):
        self.item = None
        self.item_name = item_name
        self.narration = narration

    def setup_on_start(self):
        from game_objects.global_collections import items
        self.item = items.get(self.item_name)
        if self.item is None:
            print_warning(f"{self.item_name} not found in item list")

    def narration(self):
        return self.narration

    def __str__(self):
        return f"{self.item_name}"

# Data object to facilitate the user being able to move around with both
#       Directions: Go DOWN
#       Item: Take STAIRS
class RoomConnector:
    def __init__(self,
                 direction,                 # Direction player must specify to advance to this room
                 room_name,
                 connector_item_name="",    # Optional connecting item that may connect two rooms
                 narrative_text="To your",  # Narrative text to be shown when presenting directions to the user
                 known_to_player=False,     # If this is true and a connector item is used, will specify where the room leads
                 article="the"):

        self.connector_item_name = connector_item_name
        self.direction: str = direction
        self.narrative_text = narrative_text
        self.article: str = article

        self.room_name = room_name
        self.room: Room
        self.connector_item: Optional[Item] = None
        self.known_to_player = known_to_player

    def __str__(self): return f"{self.room_name}.direction.{self.direction}"

    # initialize rooms
    def setup_on_start(self):
        from game_objects.global_collections import rooms, items
        self.room = rooms[self.room_name]
        self.connector_item = items.get(self.connector_item_name)

        if self.connector_item is None:
            if self.connector_item_name != "": warning_item_not_found(self.connector_item_name)
            self.known_to_player = True

    # To facilitate saying "There are stairs" or "There is a door"
    def get_article_with_existential_connector(self, article) -> str:
        if article == "some" or article == "":
            return "are " + article
        else:
            return "is " + article

    # The display name for narrative descriptions will the item's if it exists, and room's if not.
    def get_display_name(self) -> str:
        if self.connector_item is None:
            return self.room.display_name
        else:
            return self.connector_item.display_name

    # Print narration, ex: To your LEFT is a CLOSED DOOR
    def get_narration(self):
        if self.is_default_narrative():
            narrative_text = self.get_default_narration()
        else:
            narrative_text = self.get_interp_narration()

        return narrative_text + self.known_to_player_text()

    def is_default_narrative(self):
        return self.narrative_text == "To your"

    def get_default_narration(self):
        article_plus_connector = self.get_article_with_existential_connector(self.article)
        if self.connector_item is None:
            return f"{self.narrative_text} {self.direction} {article_plus_connector} {self.room.display_name}"
        else:
            return f"{self.narrative_text} {self.direction} {article_plus_connector} {self.connector_item.display_name}"

    def get_interp_narration(self):
        return self.narrative_text.replace("$$this", self.get_display_name()).replace("$$direction", self.direction)

    # For item_setup_dict with items, will print the connecting room if known to player.
    def known_to_player_text(self):
        if self.connector_item is not None and self.known_to_player:
            return f" leading to {self.room.article} {self.room.display_name}"
        else:
            return ""