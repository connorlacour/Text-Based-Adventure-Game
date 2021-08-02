from game_objects.global_collections import *
from parse_cmd import *
from typing import Dict, Optional
from game_objects.event import *
from game_objects.synonyms import *


class GameLoop:

    def __init__(self):

        self.player_position = rooms["dining_room"]
        setup_global_collections()


def get_next_narration(user_text) -> str:

    verb, direction, passive_obj, active_object = parse_entry(user_text)

    active_object, passive_object = resolve_noun_to_item_name(active_object, passive_obj)
    if verb == "":
        return "Not even you know what you were trying to do."

    elif verb in go_synonyms:
        narration = do_direction_command(verb, direction, active_object)

    elif verb in look_synonyms:

        if active_object == "":
            return "You LOOK AROUND."
        elif active_object == "inventory":
            return print_inventory()
        else:
            return look_at_object()

    elif verb in take_synonyms:
        return take_object(verb, active_object)

    elif verb in drop_synonyms:
        return drop_object(active_object)

    else:
        narration = resolve_event_item(verb, active_object, passive_object)
        if narration == "":
            narration = f"You try to {verb} to no avail."

    return narration


def look_at_object():

    return "to do"


def print_inventory():
    return "to do"


def take_object(verb, object_name):
    narration = ""
    if object_name in player_location.room.item_list:
        obj = player_location.room.item_list[object_name]
        if obj.item.can_take:
            narration = move(f"move {object_name} to player_inventory", player_location.room)
            if narration == "":
                narration = f"You {verb} the {obj.item.display_name} and put it in your INVENTORY"
        else:
            narration = f"You can't {verb} the {obj.item.display_name}"
    return narration


def drop_object(object_name):
    return drop(object_name, player_location.room, True)


def resolve_event_item(verb, active, passive):
    player_room = player_location.room
    room_verb_event_map = player_room.get_item_event_synonym_mapping()

    if verb in room_verb_event_map: #verb exists in room items
        verb_items = room_verb_event_map[verb]

        if active in verb_items: #active object exists in room items
            active_item = player_room.item_list[active]

            if active != passive: #passive item exists
                dict_key = f"{verb},{passive}".upper()
                if dict_key in active_item.item.events:
                    return active_item.item.events[dict_key].do_event(player_room)
                else:
                    #verb exists, active item exists, passive item specified,
                    # but no passive item in specified verb event
                    return f"You can't {verb}  '{passive}' with '{active_item}'"

            else:
                active_item.item.events.get(verb)
                return active_item.item.events[verb].do_event(player_room)
        else:
            return f"You can't {verb} with a {active}"
    else:
        return f"You can't {verb} here."


def resolve_itemless_events(verb):
    player_room  = player_location.room

    if verb in global_events:
        return global_events[verb].do_event(player_room)

    room_verb_event_map = player_room.get_item_event_synonym_mapping()
    if verb in room_verb_event_map:
        event = room_verb_event_map[verb]
        if not event.repeatable:
            del player_room[verb]
        return room_verb_event_map[verb].do_event(player_room)

    return ""


def move_player(direction, verb):
    player_location.room = player_location.room.connecting_rooms[direction].room
    return f"You {verb} {direction} to {player_location.room.display_name}"


#will find name for first item in room or connecting item list
# that contains the noun extracted from the list of display names in room
def resolve_noun_to_item_name(active, passive, room: Room = None) -> (str, str):
    if room is None: room =  player_location.room
    p, a = passive, active

    for name, item in room.item_list.items():
        if a in item.item.display_name:
            a = name
            if passive == active:
                return a, a
        if passive in item.item.display_name:
            p = name

    for name, item in player_inventory.items():
        if a in item.display_name:
            a = name
            if passive == active:
                return a, a
        if passive in item.item.display_name:
            p = name

    for conn in room.connecting_rooms.values():
        if conn.connector_item is not None:

            if a in conn.connector_item.display_name:
                a = conn.connector_item.name
                if passive == active:
                    return a, a
            if passive in conn.connector_item.display_name:
                p = conn.connector_item.name

    return a, p

#go direction
#go through directional item
def do_direction_command(verb: str, direction: str, item: str = "", room: Room = None) -> str:
    if room is None: room = player_location.room
    dir = ""
    if item != "":
        for conn in room.connecting_rooms.values():
            if conn.connector_item_name == item:
                if conn.traversable:
                    dir = conn.direction
                else:
                    return f"You try to {verb} through the" \
                           f" {conn.connector_item.display_name} but you can't. "
    else:
        if direction in room.connecting_rooms.keys():
            dir = direction

    if dir != "":
        return move_player(dir, verb)
    else:
        if direction == "":
            return f"{verb} where exactly?"
        else:
            return f"You can't {verb} {direction}!"


def do_look():
    return "hi"



