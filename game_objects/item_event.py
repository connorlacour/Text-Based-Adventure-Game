from __future__ import annotations  # Enables forward type hints
from typing import Dict, Optional, List, TYPE_CHECKING
from game_objects.game_util import print_warning, debug_print

if TYPE_CHECKING:
    from game_objects.room import Room


class ItemEvent:

    def __init__(self,
                 events=[],
                 passive_obj: str = ""
                 ):

        self.passive_obj: Optional[str] = passive_obj
        self.events: List[str] = events

    def do_event(self, room: Room) -> str:

        narration = ""
        for event in self.events:
            word_list = event.split(sep=" ")
            verb = word_list[0]

            if verb == "print":
                this_event_narration = do_print(verb, event)
            elif verb == "change":
                this_event_narration = self.change(event)
            elif verb == "drop":
                this_event_narration = self.drop(word_list[1], room)
            elif verb == "move":
                this_event_narration = self.move(event)

            if this_event_narration != "":
                narration += this_event_narration
                narration += "\n"
        return narration

    def change(self, event: str) -> str:
        tic_list = event.split(sep="`")  #designate string with spaces value field with tics
        word_list = event.split(sep=" ")

        if len(tic_list) > 1:   #if true value field is string w/spaces like `Big big dog`
            value = tic_list[1]

        if len(tic_list[0].split(sep=" ")) != 5: #First half of tic list should always be 4. If tics exist
            print_warning(f"Error, not correct length, improperly made action '{event}'")
            return "You get the sense something was supposed to occur, but it didn't.\n"
        else: value = word_list[4]

        field = word_list[2]
        if len(word_list[1].split(sep=".")) == 3:
            room_name = word_list[1].split(sep=".")[0]
            direction = word_list[1].split(sep=".")[2]
            (narration, obj) = get_room_connector(room_name, direction.upper())
            object_name = f"{room_name}.direction.{direction}"

        else:
            object_name = word_list[1]
            (narration, obj) = get_object(object_name)

        change_obj_attr(obj, object_name, field, value)

        return narration

    def drop(self, item_name: str, current_room: Room) -> str:

        return current_room.discard_item(item_name, False)

    #"move player to dining_room"
    #"move pig to dining_room"
    #"move pig to limbo"
    def move(self, event: str, room_to_check: Optional[Room] = None) -> str:
        from game_objects.global_collections import player_location, get_room, find_room_item

        word_list: List[str] = event.split(sep=" ")
        target_name = word_list[1]

        if len(word_list) != 4:
            print_warning(f"'{event}' not a valid move command")
            return "You feel like something was supposed to move, but it didn't."

        destination = get_room(word_list[3])

        if target_name == "player" and destination is not None:
            player_location.set(destination)
            print(f"Setting player location to {destination.name}")
            return ""
        elif destination is not None:
            if room_to_check is not None:
                target_object = room_to_check.get_item_from_room(target_name)
                if target_object is None:
                    return f"You feel like {target_name} was supposed to move from {destination.name} but it couldn't be found."
            else:
                room_to_check, target_object = find_room_item(target_name)

            destination.add_item(target_object)
            room_to_check.delete_item(target_object)
            debug_print(f"Successfully moved {target_object} from {room_to_check} to {destination}")
            return ""

        else:
            return f"You feel like '{target_name}' was supposed to move, but something happened."


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


def do_print(verb: str, to_print: str) -> str:
    if len(to_print.split(sep=" ", maxsplit=2)) < 2:
        print_warning("Tried to split event {to_print} but was wonky}")
        return "You get the feeling narration was supposed to occur, but your head is blank"
    else:
        return to_print.split(sep=" ", maxsplit=1)[1].replace("$$verb", verb.upper())

