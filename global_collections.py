from object_schemas import *

player_inventory: Dict[str, Item] = {}
rooms: Dict[str, Room] = {}
items: Dict[str, Item] = {}


def setup_global_collections():

    i: List[Item] = load_items_from_file("items.json")
    r: List[Room] = load_rooms_from_file('rooms.json')

    for item in i:
        items[item.name] = item

    for room in r:
        rooms[room.name] = room

    for room in rooms.values():
        room.setup_on_start()
