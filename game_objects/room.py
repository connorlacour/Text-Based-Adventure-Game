from __future__ import annotations  # Enables forward type hints
from typing import List, Dict, Optional

from game_objects.game_util import print_warning, warning_item_not_found
from game_objects.items import Item, CollectiveItem, InventoryItem
from game_objects.event import Event


class Room:

    def __init__(self,
                 name,
                 display_name,
                 article,
                 long_description,
                 short_description,
                 item_setup_dict=None,
                 room_list: List[RoomConnector] = [],
                 events: Dict[str, Event] = {},
                 setup_discard_list: List[str] = [],
                 intro: bool = False):

        self.name: str = name
        self.display_name = display_name

        self.article = article
        self.visited = False

        self.long_description = long_description
        self.short_description = short_description

        self.item_setup_dict = item_setup_dict if item_setup_dict is not None else {}

        self.item_list: Dict[str, RoomItem] = {key: RoomItem(key, value) for (key, value) in
                                               self.item_setup_dict.items()}
        self.room_list = room_list
        self.discarded_items: Dict[str, Item] = {}
        self.connecting_rooms: Dict[str, RoomConnector] = {v.direction: v for v in room_list}
        self.events = events
        self.cached_item_event_synonym_mapping: Dict[str, str] = {}
        self.setup_discard_list = setup_discard_list
        self.special_intro = intro  # For Foyer and Guest Bedroom special intros

    # initialize rooms
    def setup_on_start(self):
        from game_objects.global_collections import get_item

        for connector in self.connecting_rooms.values():
            connector.setup_on_start()

        for room_item in self.item_list.values():
            room_item.setup_on_start()

        for verb in self.events.keys():
            self.events[verb].set_verb_and_synonyms(verb)

        for item in self.setup_discard_list:
            self.discarded_items[item] = get_item(item)

        self.cached_item_event_synonym_mapping = self.item_event_synonym_mapping()

    def get_item_event_synonym_mapping(self):
        return self.cached_item_event_synonym_mapping

    def add_to_discard(self, item:Item):
        self.discarded_items[item.name] = item
        self.setup_discard_list = list(self.discarded_items.keys())

    def update_item_event_mapping_cache(self):
        self.cached_item_event_synonym_mapping = self.item_event_synonym_mapping()

    def item_event_synonym_mapping(self) -> Dict[str, str]: # return synonym -> item_name
        room_verb_dict: [str, str] = {}

        def addToDict(verb: str, e: str):
            existing_list: Optional[List[Item]] = room_verb_dict.get(verb)
            if existing_list is None:
                room_verb_dict[verb] = [e]
            else:
                room_verb_dict[verb].append(e)

        for item in self.item_list.values():
            if item.item is None:
                print(f"BAD BAD VERY BAD. {item.item_name} not found game officially set up WRONG!! CRASH IMMINENT")
            
            if item.item is not None and item.item.events is not None:
                for verb, event in item.item.events.items():
                    addToDict(event.verb, item.item.name)
                    for s in event.synonyms:
                        addToDict(s, item.item.name)

        for item in self.discarded_items.values():
            for verb, event in item.events.items():
                addToDict(event.verb, item.name)

                for s in event.synonyms:
                    addToDict(s, item.name)

        return room_verb_dict

    def get_room_event_synonym_mapping(self) -> Dict[str, Event]:
        return_dict = {}
        for x in self.events.values():
            return_dict[x.verb] = x
            for syn in x.synonyms:
                return_dict[syn] = x

        return return_dict

    # Separate initializer method for item list to simplify constructor
    def set_item_list(self, item_description_dict: Dict[str, str]):
        self.item_list = {key: RoomItem(key, value) for (key, value) in item_description_dict.items()}


    def delete_item(self, item_name: str):
        if item_name in self.item_list:
            del self.item_list[item_name]
            self.update_item_event_mapping_cache()
        elif item_name in self.discarded_items:
            del self.discarded_items[item_name]
            self.update_item_event_mapping_cache()

        else:
            print_warning(f"Couldn't delete {item_name} from {self.name}, doesn't exist")

    # Separate initializer method for room list to simplify constructor
    def set_room_map(self, connector_list: List[RoomConnector]):
        self.connecting_rooms = {v.direction: v for v in connector_list}

    def get_connector_item_dict(self) -> Dict[str, Item]:
        from game_objects.global_collections import player_location
        return {x.connector_item_name: x.connector_item for x in player_location.room.connecting_rooms.values()}

    def get_item_from_room(self, item_name) -> Optional[RoomItem]:
        item = self.item_list.get(item_name)
        if item is not None:
            return item
        else:
            print_warning(f"{item_name} not found in {self.name}")
            return None

    def get_item_from_room_or_discard(self, item_name) -> Optional[Item]:
        item = self.item_list.get(item_name)
        if item is not None:
            return item.item
        else:
            if item_name in self.discarded_items:
                return self.discarded_items.get(item_name)
        print_warning(f"{item_name} not found in {self.name}")
        return None

    # EX:  There are STAIRS heading UPWARDS leading to a BATHROOM. BEHIND you is the FOYER.
    def room_list_narration(self) -> str:
        narration = ""
        for roomConnector in self.connecting_rooms.values():
            narration += roomConnector.get_narration()
        return narration

    # EX:  CHAIRS litter the ground and PLATES are scattered on the a DINING TABLE.
    def item_list_narration(self) -> str:
        narration = ""
        for i in self.item_list.values():
            narration += i.narration
        return narration

    def get_room_narration(self) -> str:
        # Special intros used once and defined in below variables:
        foyer_intro = "You enter Chateau Prime in the dead of night.  Friends, family, and neighbors have all suffered at the hands of corporate greed.  This is the home of one of the men who profited from their loss.  Not his primary residence, you scoff to yourself.  But you're sure there's enough money in there to change the lives of your friends and family.\n\nYour mission: Find the safe to retrieve enough money to return to the people in your town."
        guest_bed_intro = "As soon as you enter the GUEST BEDROOM, you spot a guard lying on the bed.  His eyes pop open in surprise at your entrance, and he jumps up from his rest.  You notice his eyes dart sheepishly to the bed before he marches over to you.\n\n 'This is private property.  You can't be here,' he growls, grabbing your arm.  Whether he's angrier at your intrusion or the fact that you caught him sleeping is unclear.\n\nYou've been caught.  As you think of something to get away from this guard, you size up your odds against him.  He's a large man, and while he doesn't seem like someone who wants to fight, you can tell there's strength behind his bulk.  You notice his name badge says, 'Tuck Abbot'."

        if self.visited:
            narration = f"{self.short_description} {self.item_list_narration()}{self.get_discard_narration()}\n{self.       room_list_narration()}"
            return narration
        else:
            if self.special_intro:
                # Show special intro on game start
                if self.display_name == "FOYER":
                    self.special_intro = False
                    self.visited = True
                    return foyer_intro + "\n\n" + self.long_description
                # Show special intro until user gets past guard.  Guard event will trigger special_intro setting change
                elif self.display_name == "GUEST BEDROOM":
                    return guest_bed_intro + "\n\n" + self.room_list_narration()
            else:
                self.visited = True
                return self.long_description

    def get_discard_narration(self) -> str:
        discarded_count = len(self.discarded_items)
        if discarded_count == 0:
            return ""
        elif discarded_count == 1:
            be = "is"
        else:
            be = "are"

        narration = f" Dropped on the ground {be} the"

        for i in self.discarded_items.values():
            narration += " " + i.display_name + ","
        narration = narration.strip(",") + "."
        return narration

    #not in use
    def take_item(self, item_name: str) -> str:
        from game_objects.global_collections import player_inventory, update_inventory_synonym_mapping

        item_to_take = self.item_list.get(item_name)
        if item_to_take is not None:
            if item_to_take.item.can_take:

                if isinstance(item_to_take.item, CollectiveItem):
                    new_single_item: InventoryItem = item_to_take.item.new_singular_item()
                    player_inventory[new_single_item.name] = new_single_item
                    update_inventory_synonym_mapping()
                    return f"You grabbed a {new_single_item.display_name} " \
                           f"from the {item_to_take.item.display_name} and added it to your inventory."

                else:
                    player_inventory[item_name] = item_to_take.item
                    update_inventory_synonym_mapping()
                    del self.item_list[item_name]
                    return f"You took the {item_to_take.item.display_name} and added it to your inventory."

            else:
                return f"You cannot take the {item_to_take.item.display_name}"
        else:
            return f"What {item_name} ???"

    def discard_item(self, item_name: str, must_be_in_inventory=True) -> str:
        from game_objects.global_collections import player_inventory, find_room_item, update_inventory_synonym_mapping

        item_to_discard = player_inventory.get(item_name)
        if item_to_discard is not None:
            self.add_to_discard(item_to_discard)
            del player_inventory[item_name]
            update_inventory_synonym_mapping()
            return f"You drop the {item_name} to the ground."
        elif must_be_in_inventory:
            return f"You don't have any {item_name}, genius!"
        else:
            room, item_to_discard = find_room_item(item_name)
            room.delete_item(item_to_discard.name)
            self.add_to_discard(item_to_discard)
            return f"You drop {item_to_discard.get_article} {item_to_discard.display_name}"

    def __str__(self):
        return self.name


# Data object to bundle an item name and item narration together allowing us to more
#   intuitively initialize room descriptions
class RoomItem:

    def __init__(self, item_name, narration):
        self.item: Optional[Item] = None
        self.item_name = item_name
        self.narration = narration

    def setup_on_start(self):
        from game_objects.global_collections import items
        self.item = items.get(self.item_name)
        if self.item is None:
            print_warning(f"{self.item_name} not found in item list")

    def __str__(self):
        return f"{self.item_name}"


# Data object to facilitate the user being able to move around with both
#       Directions: Go DOWN
#       Item: Take STAIRS
class RoomConnector:
    def __init__(self,
                 direction,  # Direction player must specify to advance to this room
                 room_name,
                 connector_item_name="",  # Optional connecting item that may connect two rooms
                 traversable: bool = True,
                 narrative_text="To your",  # Narrative text to be shown when presenting directions to the user
                 known_to_player=False,
                 # If this is true and a connector item is used, will specify where the room leads
                 article="the"):

        self.connector_item_name = connector_item_name
        self.direction: str = direction
        self.narrative_text = narrative_text
        self.article: str = article

        self.room_name = room_name
        self.room: Room
        self.connector_item: Optional[Item] = None
        self.known_to_player = known_to_player
        self.traversable = traversable

    def __str__(self):
        return f"{self.room_name}.direction.{self.direction}"

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
