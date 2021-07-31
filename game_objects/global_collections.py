import os

from game_objects.game_util import *
from game_objects.object_schemas import *
from game_objects.player_location import PlayerLocation
from game_objects.room import Room, RoomItem
from typing import Dict, Optional

player_inventory: Dict[str, Item] = {}
rooms: Dict[str, Room] = {}
items: Dict[str, Item] = {}
player_location = PlayerLocation()
root_dir = os.path.dirname(__file__)

def get_file_name(filename, dir_name = root_dir,):
    return os.path.join(dir_name, f'{filename}')


def setup_rooms_and_items(i: List[Item], r: List[Room], starting_player_location = "dining_room"):

    for item in i:
        items[item.name] = item

    for room in r:
        rooms[room.name] = room

    limbo: Room = Room("limbo", "LIMBO", "the", "You shouldn't be here.", "How did you even get here?")

    for room in rooms.values():
        room.setup_on_start()

    rooms[limbo.name] = limbo

    player_location.set(rooms[starting_player_location])


def setup_global_collections(starting_player_location="dining_room"):

    i: List[Item] = load_items_from_file(get_file_name("templates/items.json"), root_dir)
    r: List[Room] = load_rooms_from_file(get_file_name('templates/rooms.json'), root_dir)

    setup_rooms_and_items(i, r, starting_player_location)


def setup_global_collections_for_test(test_dir: str, starting_player_location="dining_room"):

    i: List[Item] = load_items_from_file(get_file_name("templates/items.json", test_dir))
    r: List[Room] = load_rooms_from_file(get_file_name('templates/rooms.json', test_dir))

    setup_rooms_and_items(i, r, starting_player_location)


def get_room(room_name) -> Optional[Room]:
    room = rooms.get(room_name)
    if room is None: print_warning(f"{room_name} not found in room list")
    return room


def get_item(item_name) -> Optional[Room]:
    item = items.get(item_name)
    if item is None: print_warning(f"{item_name} not found in item list")
    return item

def find_room_item(item_name) -> (Optional[Room], Optional[RoomItem]):
    for room in rooms.values():
        if item_name in room.item_list:
            return room, room.item_list[item_name]
        else:
            print_warning(f"Couldn't find {item_name} in any room item_list.")
        print_warning(f"Couldn't find {room} in any room list.")
    return None, None

