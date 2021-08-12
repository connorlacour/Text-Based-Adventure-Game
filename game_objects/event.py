from __future__ import annotations  # Enables forward type hints
from typing import Dict, Optional, List, TYPE_CHECKING
from game_objects.game_util import print_warning, debug_print, pydict
from game_objects.synonyms import synonym_dict

if TYPE_CHECKING:
    from game_objects.room import Room


def get_room_connector(room_name: str, direction_name: str) -> (str, object):
    from game_objects.global_collections import rooms, get_room

    narration = ""
    room = get_room(room_name)
    direction = None

    if room is not None:
        if direction_name in room.connecting_rooms:
            direction = room.connecting_rooms[direction_name]
        else:
            print_warning(f"{direction_name} not found in {room_name}.connecting_rooms")
            narration = f"You get the sense something was supposed to occur to happen in the direction of " \
                        f"{direction_name}, but it was eerily calm."
    return narration, direction


def get_object(object_name: str) -> (str, object):
    from game_objects.global_collections import rooms, items

    obj = rooms.get(object_name)
    narration = ""

    if obj is None:
        obj = items.get(object_name)
        if obj is None:
            print_warning(f"{object_name} not found in rooms or items collections")
            narration = f"You get the sense something was supposed to occur to '{object_name.upper()}', but it remained elusive."

    return narration, obj


def do_print(verb: str, to_print: str, object_name = "") -> str:
    if len(to_print.split(sep=" ", maxsplit=2)) < 2:
        print_warning("Tried to split event {to_print} but was wonky}")
        return "You get the feeling narration was supposed to occur, but your head is blank"
    else:
        return to_print.split(sep=" ", maxsplit=1)[1].replace("$$verb", verb.upper().split(sep=",")[0]).replace("$$this", object_name)


# "change pig display_name to `BIG PIG`",
# "change pig display_name to BOING",
# "change plates max_count to 7",
# "change dining_room.direction.upwards known_to_player to False"
# "change pig narration to `That's one big pig`
def change(event: str) -> str:
    from game_objects.global_collections import find_room_item

    tic_list = event.split(sep="`")  #designate string with spaces value field with tics
    word_list = event.split(sep=" ")

    if len(tic_list) > 1:   #if true value field is string w/spaces like `Big big dog`
        value = tic_list[1]
    else:
        value = word_list[4]

    if len(tic_list[0].split(sep=" ")) != 5: #First half of tic list should always be 4. If tics exist
        print_warning(f"Error, not correct length, improperly made action '{event}'")
        return "You get the sense something was supposed to occur, but it didn't.\n"


    field = word_list[2]

    if len(word_list[1].split(sep=".")) == 3:
        room_name = word_list[1].split(sep=".")[0]
        direction = word_list[1].split(sep=".")[2]
        (narration, obj) = get_room_connector(room_name, direction.upper())
        object_name = f"{room_name}.direction.{direction}"

    elif field == "narration":
        object_name = word_list[1]
        room, obj = find_room_item(object_name)
        if room is not None and object_name in room.item_list:
            obj = room.item_list[object_name]
            narration = ""
        else:
            narration = f"You feel like {object_name} should look differently to you, but it doesn't."
    else:
        object_name = word_list[1]
        (narration, obj) = get_object(object_name)

    change_obj_attr(obj, object_name, field, value)

    return narration


def change_obj_attr(obj, object_name, field, value):
    if obj is not None:
        if not hasattr(obj, field):
            print_warning(f"Couldn't find attribute {obj.name}.{field} for change event.")
        else:
            try:
                v = int(value)
            except ValueError:
                if value.upper() == "TRUE":
                    v = True
                elif value.upper() == "FALSE":
                    v = False
                else:
                    v = value

            former_value = obj.__getattribute__(field)
            obj.__setattr__(field, v)
            print(f"Set {object_name}.{field} from {str(former_value)} to {str(obj.__getattribute__(field))}")


# "move player to dining_room"
# "move pig to dining_room"
# "move pig to limbo"
# "move pig to player_inventory
def move(event: str, room_to_check: Optional[Room] = None) -> str:
    from game_objects.global_collections import player_location, get_room, find_room_item, player_inventory, update_inventory_synonym_mapping

    word_list: List[str] = event.split(sep=" ")
    target_name = word_list[1]

    if len(word_list) != 4:
        print_warning(f"'{event}' not a valid move command")
        return "You feel like something was supposed to move, but it didn't."

    # check if destination to move is player inventory or a room
    destination_name = word_list[3]
    if destination_name == "player_inventory":
        destination = player_inventory
    else:
        if destination_name == "player_room":
            destination = player_location.room
        else:
            destination = get_room(destination_name)

        if destination is None:
            return f"You feel like '{target_name}' was supposed to move, but something happened."
        else:
            if target_name == "player":
                player_location.set(destination)
                print(f"Setting player location to {destination_name}")
                return ""
            else:
                destination = destination.item_list

    if room_to_check is not None: # If a room is specified, will fail if not in room's item list
        target_object = room_to_check.get_item_from_room_or_discard(target_name)
        if target_object is None:
            return f"You feel like {target_name} was supposed to move from {destination_name} but it couldn't be found."
    else:
        room_to_check, target_object = find_room_item(target_name)

    if room_to_check is not None and destination_name == "player_inventory":
        destination[target_name] = target_object
        update_inventory_synonym_mapping()
        room_to_check.delete_item(target_name)

    elif room_to_check is not None:
        target_object = room_to_check.get_item_from_room(target_name)
        destination[target_name] = target_object
        room_to_check.delete_item(target_name)

    else:
        if destination_name != "player_inventory":
            destination[target_name] = target_object
            del player_inventory[target_name]

    debug_print(f"Successfully moved {target_object} from {room_to_check} to {destination_name}")

    return ""


def drop(item_name: str, current_room: Room, in_inventory = False) -> str:

    return current_room.discard_item(item_name, in_inventory)

class Event:

    def __init__(self,
                 events: List[str] = [],
                 syn_list="",
                 repeatable=True
    ):
        self.passive_obj: str = ""
        self.events: List[str] = events
        self.verb = ""
        self.repeatable = repeatable

        if syn_list in synonym_dict:
            self.synonyms = synonym_dict[syn_list],
        else:
            self.synonyms = []

    def __str__(self):
        if self.verb != "":
            return str(self.events)
        else: return self.verb

    def set_verb_and_synonyms(self, verb_obj_dict_key: str = ""):
        from game_objects.synonyms import synonym_dict
        hi = verb_obj_dict_key.split(",")
        if len(hi) > 1:
            self.verb = hi[0]
            self.passive_obj = hi[1]
        else: self.verb = verb_obj_dict_key

        if self.verb in synonym_dict:
            self.synonyms = synonym_dict[self.verb]
        elif len(self.synonyms) == 0:
            if len(self.verb.split(" ")) == 1:
                self.synonyms = []
            else:
                print_warning(f"Custom Synonym not found for multi-word verb {self.verb}")

    def do_event(self, room: Room, user_verb = "", item_name="", ) -> str:

        if user_verb == "": user_verb = self.verb
        narration = ""
        for event in self.events:
            word_list = event.split(sep=" ")
            verb = word_list[0]
            this_event_narration = ""

            if verb == "print":
                this_event_narration = do_print(user_verb, event, item_name)
            elif verb == "change":
                this_event_narration = change(event)
            elif verb == "drop":
                this_event_narration = drop(word_list[1], room)
            elif verb == "move":
                this_event_narration = move(event)
            elif event == "game over":
                this_event_narration = "_game_over_"
            elif event == "game win":
                this_event_narration = "_game_win_"
            else:
                print_warning(f"Event {event} seems to be improperly formatted")

            if this_event_narration != "":
                narration += f"{this_event_narration}\n"

        return narration
