from typing import List, Dict, Optional
from game_objects.room import *


foyer_long_desc: str = "The only light in the foyer is from the two large windows in the southern wall.  Not wanting anyone outside to see you in the building, you let your eyes adjust to the dim light and take in your surroundings.  Looking around the room, you see a sitting area with CHAIRS and a SMALL TABLE in one corner.  The vacant greeter’s DESK is positioned just to the side of the entrance to the house.  A door in the NORTH wall leads the DOWNSTAIRS HALLWAY while a door in the EAST wall contains a door leading to a CLOSET visitor’s can hang their coats."

foyer_short_desc: str = "You are in the foyer. "

foyer_items: object = {
    "chairs": "There is a sitting area with CHAIRS and ",
    "table": "a SMALL TABLE in one corner, and ",
    "desk": "there is a DESK along the SOUTH wall by the main entrance. ",
    "doors": "Two doors lead out of the room and further into the building: "
}

foyer_room_list: list = [{
		"known_to_player": True,
		"narrative_text": "one in the NORTH wall that goes to the DOWNSTAIRS HALLWAY and ",
		"article": "the",
		"room_name": "downstairs hallway",
		"direction": "NORTH"
	}, {
		"known_to_player": True,
		"narrative_text": "one in the EAST wall leading to a CLOSET.",
		"article": "a",
		"room_name": "closet",
		"direction": "EAST"
	}]


class Foyer(Room):
    def __init__(self, long_description, short_description, item_setup_dict, room_list: List[RoomConnector]):
        super().__init__("foyer", "FOYER", "the", long_description, short_description, item_setup_dict=item_setup_dict, room_list=room_list)
        self.new_game_intro: bool = True
        self.foyer_intro: str = "You enter Chateau Prime in the dead of night.  Friends, family, and neighbors have all suffered at the hands of corporate greed.  This is the home of one of the men who profited from their loss.  Not his primary residence, you scoff to yourself.  But you’re sure there’s enough money in there to change the lives of your friends and family.\n\nYour mission: Find the safe to retrieve enough money to return to the people in your town."

    def game_intro_narrative(self):
        if self.new_game_intro:
            print(self.foyer_intro)
            self.new_game_intro = False


def initialize_foyer():
    """Create default foyer room for game"""
    return Foyer(foyer_long_desc, foyer_short_desc, foyer_items, foyer_room_list)