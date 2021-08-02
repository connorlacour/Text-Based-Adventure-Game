from typing import List, Dict, Optional
from game_objects.room import *


guest_bed_long_desc: str = "With the absence of the guard, you are finally able to explore the guest bedroom.  The door in the SOUTH wall leads back to the UPSTAIRS HALLWAY.  It is the only door in or out of the room.  The bed that you originally saw the guard resting on is furnished with a simple white plush comforter.  There is a NIGHT STAND against the NORTH wall beside the bed and a WINDOW looking out over the back of the house.  It is a simple room, but it’s comfortable"

guest_bed_short_desc: str = "You are in the guest bedroom. "

guest_bed_items: object = {
    "window": "There is a WINDOW and ",
    "night stand": "a NIGHT STAND beside the bed against the NORTH wall.",
}

guest_bed_room_list: list = [{
		"known_to_player": True,
		"narrative_text": "The only door in or out is in the SOUTH wall back to the UPSTAIRS HALLWAY. ",
		"article": "the",
		"room_name": "upstairs hallway",
		"direction": "SOUTH"
	}]


class Guest_Bedroom(Room):
    def __init__(self, long_description, short_description, item_setup_dict, room_list: List[RoomConnector]):
        super().__init__("guest bedroom", "GUEST BEDROOM", "the", long_description, short_description, item_setup_dict=item_setup_dict, room_list=room_list)
        self.first_entry: bool = True
        self.guest_intro: str = 'As soon as you enter the GUEST ROOM, you spot a guard lying on the bed.  His eyes pop open in surprise at your entrance, and he jumps up from his rest.  You notice his eyes dart sheepishly to the bed before he marches over to you.\n\n“This is private property.  You can’t be here,” he growls, grabbing your arm.  Whether he’s angrier at your intrusion or the fact that you caught him sleeping is unclear.\n\nYou’ve been caught.  As you think of something to get away from this guard, you size up your odds against him.  He’s a large man, and while he doesn’t seem like someone who wants to fight, you can tell there’s strength behind his bulk.  You notice his name badge says, “Tuck Abbot”.'

    def guest_intro_narrative(self):
        if self.first_entry:
            print(self.guest_intro)
            self.first_entry = False


def initialize_guest_bedroom():
    """Create default guest bedroom for game"""
    return Guest_Bedroom(guest_bed_long_desc, guest_bed_short_desc, guest_bed_items, guest_bed_room_list)