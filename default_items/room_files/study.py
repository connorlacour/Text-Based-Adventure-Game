from typing import List, Dict, Optional
from game_objects.room import *


study_long_desc: str = "The first thing you notice in the study is a CRATE with a DOG that you assume is an Australian Shepherd.  It watches you warily with its head lowered, a soft growl coming from it.  The crate is across from the door in the NORTH wall that goes back to the UPSTAIRS HALLWAY."

study_short_desc: str = "You are in the study. "

study_items: object = {
    "crate": "A CRATE with a ",
    "dog": "DOG is across the room from the door.",
}

study_room_list: list = [{
		"known_to_player": True,
		"narrative_text": "The only door in or out is in the NORTH wall back to the UPSTAIRS HALLWAY. ",
		"article": "the",
		"room_name": "upstairs hallway",
		"direction": "NORTH"
	}]


class Study(Room):
    def __init__(self, long_description, short_description, item_setup_dict, room_list: List[RoomConnector]):
        super().__init__("study", "STUDY", "a", long_description, short_description, item_setup_dict=item_setup_dict, room_list=room_list)


def initialize_study():
    """Create default study room for game"""
    return Study(study_long_desc, study_short_desc, study_items, study_room_list)
