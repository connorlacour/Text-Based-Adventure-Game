from typing import List, Dict, Optional
from game_objects.room import *


attic_closet_long_desc: str = "The attic closet resembles the clutter attic you had imagined.  BOXES are stacked and line the walls around the closet and ELECTRONICS are scattered around in piles. This is where items go to be stored for years.  The only door is the one you entered through in the NORTH wall that leads back to the ATTIC."

attic_closet_short_desc: str = "You are in the attic closet. "

attic_closet_items: object = {
    "boxes": "BOXES are stacked against the walls and ",
    "electronics": "ELECTRONICS sit in piles around the closet. ",
}

attic_closet_room_list: list = [{
		"known_to_player": True,
		"narrative_text": " The door in the NORTH wall goes back to the ATTIC. ",
		"article": "the",
		"room_name": "attic",
		"direction": "NORTH"
	}]


class Attic_Closet(Room):
    def __init__(self, long_description, short_description, item_setup_dict, room_list: List[RoomConnector]):
        super().__init__("attic closet", "ATTIC CLOSET", "the", long_description, short_description, item_setup_dict=item_setup_dict, room_list=room_list)


def initialize_attic_closet():
    """Create default attic closet room for game"""
    return Attic_Closet(attic_closet_long_desc, attic_closet_short_desc, attic_closet_items, attic_closet_room_list)
