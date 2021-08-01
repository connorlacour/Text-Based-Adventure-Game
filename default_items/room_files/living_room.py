from typing import List, Dict, Optional
from game_objects.room import *


living_room_long_desc: str = "The living room is spacious and lined with more art.  Despite the FIREPLACE set in the WEST wall directly across from the EAST HALLWAY door, the room is cold.  Above the FIREPLACE is a curved blade.  It is a traditional KATANA.  The furniture in the room consists of a large sectional and two modern wingback chairs.  A second door leading to the DINING ROOM sits in the NORTH wall.\n\nThe furniture looks rigid and barely used.  It is a living room, but there is not much life in it.  The only sign that anyone had been in the room is a coffee table with coasters and a STRIP OF PAPER."

living_room_short_desc: str = "You are in the living room. "

living_room_items: object = {
    "fireplace": "A FIREPLACE is set in the WEST wall",
    "katana": " with a KATANA above it",
    "strip of paper": ". A coffee table with a STRIP OF PAPER on it rests in the middle of the room."
}

living_room_room_list: list = [{
		"known_to_player": True,
		"narrative_text": "There are two doors, one in the NORTH wall to the DINING ROOM and ",
		"article": "the",
		"room_name": "dining room",
		"direction": "NORTH"
	},{
		"known_to_player": True,
		"narrative_text": "another in the EAST wall to the DOWNSTAIRS HALLWAY. ",
		"article": "the",
		"room_name": "downstairs hallway",
		"direction": "EAST"
	}]


class Living_Room(Room):
    def __init__(self, long_description, short_description, item_setup_dict, room_list: List[RoomConnector]):
        super().__init__("living room", "LIVING ROOM", "the", long_description, short_description, item_setup_dict=item_setup_dict, room_list=room_list)


def initialize_living_room():
    """Create default living room for game"""
    return Living_Room(living_room_long_desc, living_room_short_desc, living_room_items, living_room_room_list)
