from typing import List, Dict, Optional
from game_objects.room import *


gym_long_desc: str = "The home gym that you are standing in is equipped with a state of the art treadmill and weights scattered around the room.  A SHELF on the EAST wall is lined with various electronics.  Across from this, a floor length MIRROR hangs on the WEST wall.  The door in the NORTH wall leads back to the UPSTAIRS HALLWAY."

gym_short_desc: str = "You are in the home gym. "

gym_items: object = {
    "shelf": "There's a SHELF on the EAST wall and ",
    "mirror": " a MIRROR hangs on the WEST wall.",
}

gym_room_list: list = [{
		"known_to_player": True,
		"narrative_text": "The only door in or out is in the NORTH wall back to the UPSTAIRS HALLWAY.",
		"article": "the",
		"room_name": "upstairs hallway",
		"direction": "NORTH"
	}]


class Home_Gym(Room):
    def __init__(self, long_description, short_description, item_setup_dict, room_list: List[RoomConnector]):
        super().__init__("home gym", "HOME GYM", "a", long_description, short_description, item_setup_dict=item_setup_dict, room_list=room_list)


def initialize_home_gym():
    """Create default home gym room for game"""
    return Home_Gym(gym_long_desc, gym_short_desc, gym_items, gym_room_list)
