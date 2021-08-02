from typing import List, Dict, Optional
from game_objects.room import *


dining_room_long_desc: str = "The dining room is furnished with a table large enough to fit twelve people and a large CHINA CABINET full of delicate, ornate dinnerware against the WEST wall. To the side of the cabinet, you see a 4 hook WALL MOUNT.  You imagine stuffy business meetings are the most common dinner parties, but it would be a lovely room for family and friends to share a meal.  There’s a door in the SOUTH wall to the LIVING ROOM and another in the EAST wall goes to the KITCHEN."

dining_room_short_desc: str = "You are in the dining room. "

dining_room_items: object = {
    "china cabinet": "A CHINA CABINET and ",
    "wall mount": "WALL MOUNT are along the WEST wall",
}

dining_room_room_list: list = [{
		"known_to_player": True,
		"narrative_text": "There are two doors, one in the SOUTH wall to the LIVING ROOM and ",
		"article": "the",
		"room_name": "living room",
		"direction": "SOUTH"
	},{
		"known_to_player": True,
		"narrative_text": "another in the EAST wall to the KITCHEN.",
		"article": "the",
		"room_name": "kitchen",
		"direction": "EAST"
	}]


class Dining_Room(Room):
    def __init__(self, long_description, short_description, item_setup_dict, room_list: List[RoomConnector]):
        super().__init__("dining room", "DINING ROOM", "the", long_description, short_description, item_setup_dict=item_setup_dict, room_list=room_list)


def initialize_dining_room(long_desc: str = dining_room_long_desc, short_desc: str = dining_room_short_desc, items: object = dining_room_items, room_list: list = dining_room_room_list):
    """Create default dining room for game"""
    return Dining_Room(long_desc, short_desc, items, room_list)
