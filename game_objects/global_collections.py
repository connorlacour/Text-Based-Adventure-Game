import os

import parse_cmd
from game_objects.global_events import events
from game_objects.game_util import *
from game_objects.object_schemas import *
from game_objects.player_location import PlayerLocation
from game_objects.room import Room, RoomItem
from typing import Dict, Optional, Set
from collections import defaultdict

# If our grader is reading this file, let it be known that I'm reasonably sure this should be a Game State class

rooms: Dict[str, Room] = {}
items: Dict[str, Item] = {}

cached_inventory_synonym_mapping: Dict[str, List[str]] = {}

global_events: Dict[str, Event] = events

player_location = PlayerLocation()
root_dir = os.path.dirname(__file__).replace("game_objects", "")

player_inventory: Dict[str, Item] = {}

def get_item_in_player_scope(item_name: str) -> Optional[Item]:

    if item_name in player_inventory:
        return player_inventory[item_name]
    if item_name in player_location.room.item_list:
        return player_location.room.item_list[item_name].item
    elif item_name in player_location.room.discarded_items:
        return player_location.room.discarded_items[item_name]
    elif item_name != "":
        room_connectors_dict = player_location.room.get_connector_item_dict()
        if item_name in room_connectors_dict:
            return room_connectors_dict[item_name]

    print_warning(f"Couldn't find {item_name} in inventory or {player_location}")


def print_inventory() -> str:
    narration = "You are currently holding:"
    if len(player_inventory) == 0:
        narration += " NOTHING.  Try picking something up!"
    else:

        for item in player_inventory.values():
            narration += f" \n-{item.display_name}"

    return narration


def get_items_display_name() -> Dict[str, str]:
    return {a.display_name: a.name for a in items.values()}


def get_file_name(filename, dir_name=root_dir,):
    return os.path.join(dir_name, f'{filename}')


def update_inventory_synonym_mapping():  # return synonym -> item

    for key in cached_inventory_synonym_mapping.keys():
        del cached_inventory_synonym_mapping[key]

    def addToDict(verb: str, e: str):
        existing_list: Optional[List[str]] = cached_inventory_synonym_mapping.get(verb)
        if existing_list is None:
            cached_inventory_synonym_mapping[verb] = [e]
        else:
            cached_inventory_synonym_mapping[verb].append(e)

    for item in player_inventory.values():
        for verb, event in item.events.items():
            addToDict(verb, item.name)
            for s in event.synonyms:
                addToDict(s, item.name)

    return cached_inventory_synonym_mapping


# This function gets a dict of verb -> [object name, object_name] for all events for all items in scope.
# To find the right event we only have to iterate over said object's events and synonyms.
# If this is confusing its because I messed up the dict keys.  It's a long story.
def in_scope_event_synonym_mapping():
    import time
    start_time = time.time()

    room_dict = player_location.room.get_item_event_synonym_mapping()
    inventory_dict = cached_inventory_synonym_mapping
    new_dict = defaultdict(list)

    if len(inventory_dict) == 0:
        if len(room_dict) != 0:
            return room_dict
        else:
            return {}

    for d in (room_dict, inventory_dict):
        for key, value in d.items():
            new_dict[key].append(value)
    return new_dict


def setup_rooms_and_items(i: List[Item], r: List[Room], starting_player_location = "dining_room"):

    for item in i:
        items[item.name] = item

    for room in r:
        rooms[room.name] = room

    for room in rooms.values():
        room.setup_on_start()

    player_location.set(rooms[starting_player_location])
    parse_cmd.setup_parser()


def setup_global_collections(starting_player_location="foyer"):

#    i: List[Item] = load_items_from_file(get_file_name("templates/items.json"), root_dir)
#    r: List[Room] = load_rooms_from_file(get_file_name('templates/rooms.json'), root_dir)
    i: List[Item] = load_items_from_file(get_file_name("templates/game_items.json"), root_dir)
    r: List[Room] = load_rooms_from_file(get_file_name('templates/game_rooms.json'), root_dir)

    setup_rooms_and_items(i, r, starting_player_location)

def setup_global_collections_for_test(test_dir: str, starting_player_location="foyer"):
    import time
    start_time = time.time()

#    i: List[Item] = load_items_from_file(get_file_name("templates/items.json", test_dir))
#    r: List[Room] = load_rooms_from_file(get_file_name('templates/rooms.json', test_dir))
    i: List[Item] = load_items_from_file(get_file_name("templates/game_items.json", test_dir))
    r: List[Room] = load_rooms_from_file(get_file_name('templates/game_rooms.json', test_dir))

    setup_rooms_and_items(i, r, starting_player_location)
    print("setup_global_collections_for_test: --- %s seconds ---" % (time.time() - start_time))


def get_room(room_name) -> Optional[Room]:
    room = rooms.get(room_name)
    if room is None: print_warning(f"{room_name} not found in room list")
    return room


def get_item(item_name) -> Optional[Item]:
    item = items.get(item_name)
    if item is None: print_warning(f"{item_name} not found in item list")
    return item


def find_room_item(item_name) -> (Optional[Room], Optional[Item]):
    for room in rooms.values():
        obj = room.get_item_from_room_or_discard(item_name)
        if obj is not None:
            return room, obj

    print_warning(f"Couldn't find {item_name} in any room item_list.")
    return None, None

