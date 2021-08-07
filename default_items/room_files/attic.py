from typing import List, Dict, Optional
from game_objects.room import *


attic_long_desc: str = "The attic is not what you expected.  You imagined a messy room where memories are sent for storage.  Instead, it could easily be turned into another bedroom.  There’s a circular window that lets in the light from the moon.  The only clutter is a TRUNK in the center of the room and a BOOKCASE against the NORTH wall.\n\nThere is a single door in the SOUTH wall that opens up to an ATTIC CLOSET.  The only other entryway/exit that you see are the stairs you took to enter this room that go back to the UPSTAIRS HALLWAY."

attic_short_desc: str = "You are in the attic. "

attic_items: object = {
    "bookcase": "There is a BOOKCASE on the NORTH wall and ",
    "trunk": "a TRUNK in the middle of the room. ",
}

attic_room_list: list = [{
		"known_to_player": True,
		"narrative_text": "A door in the SOUTH wall opens to an ATTIC CLOSET and ",
		"article": "the",
		"room_name": "attic closet",
		"direction": "SOUTH"
	},{
		"known_to_player": True,
		"narrative_text": "the stairs in the WEST wall go back down to the UPSTAIRS HALLWAY.",
		"article": "the",
		"room_name": "upstairs hallway",
		"direction": "WEST"
	},{
		"known_to_player": False,
		"narrative_text": "The BOOKCASE slides to the side revealing a walk-in SAFE with a KEYPAD and a SLOT for a key as well.",
		"article": "the",
		"room_name": "safe",
		"direction": "NORTH"
	}]


class Attic(Room):
    def __init__(self, long_description, short_description, item_setup_dict, room_list: List[RoomConnector]):
        super().__init__("attic", "ATTIC", "the", long_description, short_description, item_setup_dict=item_setup_dict, room_list=room_list)


def initialize_attic(long_desc: str = attic_long_desc, short_desc: str = attic_short_desc, items: object = attic_items, room_list: list = attic_room_list):
    """Create default attic room for game"""
    return Attic(long_desc, short_desc, items, room_list)
