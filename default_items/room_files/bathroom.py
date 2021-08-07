from typing import List, Dict, Optional
from game_objects.room import *


bath_long_desc: str = "You look around the bathroom quickly.  It is a large room with a tub big enough for two or three people, but it is a bathroom nevertheless.  The white tile reflects what little light it catches and makes the room easy to look around.  You notice the BATHROOM MIRROR set in the NORTH wall and a WASTE BASKET against the EAST wall.  The door in the WEST wall leads back to the MAIN BEDROOM."

bath_short_desc: str = "You are in the bathroom. "

bath_items: object = {
    "mirror": "There is a BATHROOM MIRROR above the sink set in the NORTH wall and ",
    "waste basket": "a WASTE BASKET against the EAST wall. ",
}

bath_room_list: list = [{
		"known_to_player": True,
		"narrative_text": "The door in the WEST wall leads back to the MAIN BEDROOM. ",
		"article": "the",
		"room_name": "main bedroom",
		"direction": "WEST"
	}]


class Bathroom(Room):
    def __init__(self, long_description, short_description, item_setup_dict, room_list: List[RoomConnector]):
        super().__init__("bathroom", "BATHROOM", "the", long_description, short_description, item_setup_dict=item_setup_dict, room_list=room_list)


def initialize_bathroom(long_desc: str = bath_long_desc, short_desc: str = bath_short_desc, items: object = bath_items, room_list: list = bath_room_list):
    """Create default bathroom for game"""
    return Bathroom(long_desc, short_desc, items, room_list)
