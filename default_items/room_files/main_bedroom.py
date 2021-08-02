from typing import List, Dict, Optional
from game_objects.room import *


main_bed_long_desc: str = "The main bedroom is spacious and decorated in vibrant greens.  A large canopy BED takes up a majority of the room, and a WINDOW facing the front of the house.  There are heavy drapes covering the WINDOW to block out light when sleeping.  While this may be a smaller house for the owner, no expense was spared with making this bedroom comfortable for the occupant.  There is a BATHROOM off to the side beyond a door in the EAST wall.  The other door in the room, in the SOUTH wall, goes back to the UPSTAIRS HALLWAY."

main_bed_short_desc: str = "You are in the main bedroom. "

main_bed_items: object = {
    "bed": "There is a canopy BED against the far wall and ",
    "window": "a WINDOW to the side of it. ",
}

main_bed_room_list: list = [{
		"known_to_player": True,
		"narrative_text": "There are two doors, one in the SOUTH wall that goes back to the UPSTAIRS HALLWAY and ",
		"article": "the",
		"room_name": "upstairs hallway",
		"direction": "SOUTH"
	},{
		"known_to_player": True,
		"narrative_text": "another in the EAST wall that leads to a BATHROOM. ",
		"article": "the",
		"room_name": "bathroom",
		"direction": "EAST"
	}]


class Main_Bedroom(Room):
    def __init__(self, long_description, short_description, item_setup_dict, room_list: List[RoomConnector]):
        super().__init__("main bedroom", "MAIN BEDROOM", "the", long_description, short_description, item_setup_dict=item_setup_dict, room_list=room_list)


def initialize_main_bedroom(long_desc: str = main_bed_long_desc, short_desc: str = main_bed_short_desc, items: object = main_bed_items, room_list: list = main_bed_room_list):
    """Create default main bedroom for game"""
    return Main_Bedroom(long_desc, short_desc, items, room_list)
