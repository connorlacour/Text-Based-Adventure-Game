from typing import List, Dict, Optional
from game_objects.room import *


kitchen_long_desc: str = "You’re not surprised to find the kitchen full of state of the art appliances.  Surrounded by the shining silver appliances feels akin to being in a wall of mirrors in its own way.  There’s a door in the WEST wall leading to the DINING ROOM and a second one in the SOUTH wall to the DOWNSTAIRS HALLWAY.  There’s an occasional beep from the MICROWAVE, which is embedded in the EAST wall above the countertop.  A brown paper bag is on the counter underneath it.\n\nA few feet in front of the EAST wall is an ISLAND counter.  There’s a bowl of fruit and a bright blue jar on the ISLAND.  These are the only pop of color in the otherwise white and silver room."

kitchen_short_desc: str = "You are in the kitchen. "

kitchen_items: object = {
    "microwave": "A MICROWAVE is embedded in the EAST wall over a countertop and ",
    "island": "an ISLAND counter with ",
    "fruit": "fruit and ",
    "jar": "a bright blue jar sit a few feet away from the wall."
}

kitchen_room_list: list = [{
		"known_to_player": True,
		"narrative_text": "There are two doors, one in the WEST wall to the DINING ROOM and ",
		"article": "the",
		"room_name": "dining room",
		"direction": "WEST"
	},{
		"known_to_player": True,
		"narrative_text": "another in the SOUTH wall to the DOWNSTAIRS HALLWAY. ",
		"article": "the",
		"room_name": "downstairs hallway",
		"direction": "SOUTH"
	}]


class Kitchen(Room):
    def __init__(self, long_description, short_description, item_setup_dict, room_list: List[RoomConnector]):
        super().__init__("kitchen", "KITCHEN", "the", long_description, short_description, item_setup_dict=item_setup_dict, room_list=room_list)


def initialize_kitchen(long_desc: str = kitchen_long_desc, short_desc: str = kitchen_short_desc, items: object = kitchen_items, room_list: list = kitchen_room_list):
    """Create default kitchen room for game"""
    return Kitchen(long_desc, short_desc, items, room_list)
