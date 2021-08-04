from typing import List, Dict, Optional
from game_objects.room import *


down_hall_long_desc: str = "The downstairs hallway appears completely empty at first glance.  The door in the NORTH wall leads to the KITCHEN; the door in the WEST wall to the LIVING ROOM; and finally, the door in the SOUTH wall leads to the FOYER. On the EAST wall, you see a PAINTING hanging directly across from the LIVING ROOM.  Underneath the PAINTING is a PODIUM with a glass case on top of it.  Next to the PODIUM, leading up from the side of the EAST wall, are STAIRS leading to the SECOND FLOOR."

down_hall_short_desc: str = "You are in the downstairs hallway. "

down_hall_items: object = {
    "painting": "A PAINTING and ",
    "podium": "PODIUM are also along the EAST wall.",
}

down_hall_room_list: list = [{
		"known_to_player": True,
		"narrative_text": "The door in the NORTH wall leads to the KITCHEN, ",
		"article": "the",
		"room_name": "kitchen",
		"direction": "NORTH"
	},{
		"known_to_player": True,
		"narrative_text": "the door in the WEST wall leads to the LIVING ROOM, and ",
		"article": "the",
		"room_name": "living room",
		"direction": "WEST"
	},{
		"known_to_player": True,
		"narrative_text": "the door in the SOUTH wall leads to the FOYER. ",
		"article": "the",
		"room_name": "foyer",
		"direction": "SOUTH"
	},{
		"known_to_player": True,
		"narrative_text": "There are STAIRS leading to the UPSTAIRS HALLWAY in the EAST wall. ",
		"article": "the",
		"room_name": "kitchen",
		"direction": "NORTH"
	}]


class Downstairs_Hallway(Room):
    def __init__(self, long_description, short_description, item_setup_dict, room_list: List[RoomConnector]):
        super().__init__("downstairs hallway", "DOWNSTAIRS HALLWAY", "the", long_description, short_description, item_setup_dict=item_setup_dict, room_list=room_list)


def initialize_down_hallway(long_desc: str = down_hall_long_desc, short_desc: str = down_hall_short_desc, items: object = down_hall_items, room_list: list = down_hall_room_list):
    """Create default downstairs hallway room for game"""
    return Downstairs_Hallway(long_desc, short_desc, items, room_list)
