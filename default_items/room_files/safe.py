from typing import List, Dict, Optional
from game_objects.room import *


safe_long_desc: str = "Congratulations!  You made it to the SAFE.  The hidden door you came through in the South Door provides your escape back through the house.  There is GOLD, CASH, and JEWELS as your reward for your mission.  Take it back to your town and use it to give back to your community.  You succeeded in becoming a modern-day Robin Hood."

safe_short_desc: str = "You are in the safe! "

safe_items: object = {
    "gold": "GOLD ",
    "cash": "CASH ",
    "jewels": "JEWELS"
}

safe_room_list: list = [{
		"known_to_player": True,
		"narrative_text": " The door in the SOUTH wall goes back to the ATTIC. Fill your coffers with ",
		"article": "the",
		"room_name": "attic",
		"direction": "SOUTH"
	}]


class Safe(Room):
    def __init__(self, long_description, short_description, item_setup_dict, room_list: List[RoomConnector]):
        super().__init__("safe", "SAFE", "the", long_description, short_description, item_setup_dict=item_setup_dict, room_list=room_list)


def initialize_safe():
    """Create default safe for game"""
    return Safe(safe_long_desc, safe_short_desc, safe_items, safe_room_list)
