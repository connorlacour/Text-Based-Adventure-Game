from typing import List, Dict, Optional
from game_objects.room import *


up_hall_long_desc: str = "The upstairs hallway extends down the length of the floor with stairs on either side, one set in the EAST wall leading back down to the DOWNSTAIRS HALLWAY ending and another in the WEST wall that go to the ATTIC.   The darkness of the hallway leaves you feeling uneasy.  Unlike the downstairs which had felt almost deserted, you have the feeling you are not entirely alone on this floor.\n\nThe two doors in the NORTH wall lead to a MAIN BEDROOM and a GUEST BEDROOM while the two doors in the SOUTH wall lead to a STUDY and a HOME GYM.  You can hear faint whimpering sounds coming from the STUDY.  Between the doors of the SOUTH wall hangs a LARGE POSTER.  It hangs at eye level and takes up a significant portion of the wall between the doors.  In contrast, a smaller ALARM is set between the two NORTH doors."

up_hall_short_desc: str = "You are in the upstairs hallway, with "

up_hall_room_items: object = {
    "alarm": "An ALARM is positioned on the wall between the bedrooms and ",
    "large poster": "a LARGE POSTER is between the doors in the SOUTH wall.",
}

up_hall_room_list: list = [{
		"known_to_player": True,
		"narrative_text": "stairs in the EAST wall leading down to the DOWNSTAIRS HALLWAY and ",
		"article": "the",
		"room_name": "downstairs hallway",
		"direction": "EAST"
	},{
		"known_to_player": True,
		"narrative_text": "stairs in the WEST wall leading up to the ATTIC. There are four doors total. ",
		"article": "the",
		"room_name": "attic",
		"direction": "WEST"
	},{
		"known_to_player": True,
		"narrative_text": "The two in the NORTH wall go to the MAIN BEDROOM and ",
		"article": "the",
		"room_name": "main bedroom",
		"direction": "NORTH"
	},{
		"known_to_player": True,
		"narrative_text": "the GUEST BEDROOM while ",
		"article": "the",
		"room_name": "guest bedroom",
		"direction": "NORTH"
	},{
		"known_to_player": True,
		"narrative_text": "the two in the SOUTH wall go to the STUDY and ",
		"article": "the",
		"room_name": "study",
		"direction": "SOUTH"
	},{
		"known_to_player": True,
		"narrative_text": "a home gym",
		"article": "a",
		"room_name": "home gym",
		"direction": "SOUTH"
	}]


class Upstairs_Hallway(Room):
    def __init__(self, long_description, short_description, item_setup_dict, room_list: List[RoomConnector]):
        super().__init__("upstairs hallway", "UPSTAIRS HALLWAY", "the", long_description, short_description, item_setup_dict=item_setup_dict, room_list=room_list)


def initialize_upstairs_hallway(long_desc: str = up_hall_long_desc, short_desc: str = up_hall_short_desc, items: object = up_hall_room_items, room_list: list = up_hall_room_list):
    """Create default upstairs hallway for game"""
    return Upstairs_Hallway(long_desc, short_desc, items, room_list)
