from typing import List, Dict, Optional
from game_objects.room import *


closet_long_desc: str = "The closet is empty save for a solitary COAT and a single GLOVE that appears to have been dropped beside the only door, the one in the WESTERN wall you entered through.  You wonder who the coat might have belonged to since it is the only one left in the closet.  Did the owner leave it intentionally?  Are they coming back?"

closet_short_desc: str = "You are in the closet. "

closet_items: object = {
    "glove": "Next to the door is a single GLOVE.",
    "coat": " A COAT hangs to the side.",
}

closet_room_list: list = [{
		"known_to_player": True,
		"narrative_text": "The lone door in the WESTERN wall leads back to the FOYER.",
		"article": "the",
		"room_name": "foyer",
		"direction": "WEST"
	}]


class Closet(Room):
    def __init__(self, long_description, short_description, item_setup_dict, room_list: List[RoomConnector]):
        super().__init__("closet", "CLOSET", "a", long_description, short_description, item_setup_dict=item_setup_dict, room_list=room_list)


def initialize_closet(long_desc: str = closet_long_desc, short_desc: str = closet_short_desc, items: object = closet_items, room_list: list = closet_room_list):
    """Create default closet room for game"""
    return Closet(long_desc, short_desc, items, room_list)
