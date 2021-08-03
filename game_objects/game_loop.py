from parse_cmd import *
from game_objects.event import *
from game_objects.synonyms import *
from game_objects.global_collections import *

class GameLoop:

    def __init__(self):

        self.player_position = rooms["dining_room"]
        setup_global_collections()



def get_next_narration(user_text) -> str:
    verb, direction, passive_obj, active_object = parse_entry(user_text)
    print(f"v: {verb}, d: {direction}, po: {passive_obj}, ao:{active_object}")

    active_object, passive_object = resolve_noun_to_item_name(active_object, passive_obj)
    import time
    start_time = time.time()
    if verb == "":
        return "Not even you know what you were trying to do."

    elif verb in go_synonyms:
        return do_direction_command(verb, direction, active_object)

    elif verb in look_synonyms:

        if active_object == "":
            return "You LOOK AROUND." #Since the next loop will just print room description, just skip.
        elif active_object == "inventory":
            return print_inventory()
        else:
            return look_at_object()

    elif active_object == "":
        narration = resolve_itemless_events(verb)
        if narration == "":
            narration = f"You try to {verb} to no avail."
        return narration

    elif verb in take_synonyms:
        return take_object(verb, active_object)

    elif verb in drop_synonyms:
        return drop_object(active_object)

    else:
        start_time = time.time()
        narration = resolve_event_item(verb, active_object, passive_object)
        print("Resolve event --- %s seconds ---" % (time.time() - start_time))

        if narration == "":
            narration = f"You try to {verb} to no avail."
        return narration

def look_at_object():

    return "to do"


def print_inventory():
    return "to do"


def take_object(verb, object_name):
    narration = ""
    if object_name in player_location.room.item_list or object_name in player_location.room.discarded_items():

        obj = player_location.room.item_list[object_name]
        if obj.item.can_take:
            narration = move(f"move {object_name} to player_inventory", player_location.room)
            if narration == "":
                narration = f"You {verb} the {obj.item.display_name} and put it in your INVENTORY"
        else:
            narration = f"You can't {verb} the {obj.item.display_name}!"
    return narration


def drop_object(object_name):
    return drop(object_name, player_location.room, True)


def resolve_event_item(verb, active, passive):
    in_scope_event_map = in_scope_event_synonym_mapping()

    if verb in in_scope_event_map:  # verb exists in room, room.items, or inventory.items event lists map
        verb_items = in_scope_event_map[verb]

        if active in verb_items:  # active object exists in player scope
            active_item = get_item_in_player_scope(active)

            if active != passive:  # passive item specified

                dict_key = f"{verb},{passive}".upper()
                if dict_key in active_item.events:
                    if get_item_in_player_scope(passive) is not None:
                        return active_item.do_event(dict_key)
                    else:  # passive item not in player scope
                        passive = items[passive]
                        return f"You feel as though {passive.display_name} is out of reach!"

                else:  # verb exists, active item exists, no event exists involving passive item.
                    passive_item = get_item_in_player_scope(passive)
                    if passive_item is not None:  # Swap passive and active and see if event exists b/c parser error maybe
                        dict_key = f"{verb},{passive}".upper()
                        if dict_key in passive_item.events:
                            return passive_item.do_event(dict_key)
                        else:  # Passive item exists but nothing matched.
                            return f"You try to {verb} with a {active} and {passive}, but nothing happens"

            # If passive item not specified or nothing is found with the passive object, search for active object
            if verb in active_item.events:
                return active_item.do_event(verb)
            elif active != passive:
                passive_item = get_item_in_player_scope(passive)
                # If nothing is found with just active object, search for passive object
                if passive_item is not None and verb in passive_item.events:
                    return passive_item.do_event(verb)

                # I have no idea how you would get to this line, logically.
                return f"You can't {verb} with a {active} and {passive}!"

    narration = ""
    # If we get to this point, we havent matched with verb to any item.
    if active == passive: #Only one object specified. Might be a global event matching to a nonexistant item like CLAP hands. HUM song.
        narration = resolve_itemless_events(verb)
    if narration == "":
        return f"You can't {verb} here!"
    else: return narration


def resolve_itemless_events(verb):
    player_room  = player_location.room
    narration = ""
    if verb in global_events:
        event = global_events[verb]
        narration = event.do_event(player_room, verb)
        if event.repeatable:
            del global_events[verb]
        return narration

    in_scope_event_map = player_location.room.get_room_event_synonym_mapping()
    if verb in in_scope_event_map:
        event = in_scope_event_map[verb]
        narration = event.do_event(player_room, verb)

        if not event.repeatable:
            del player_room.events[verb]
            player_room.update_item_event_mapping_cache()

    return narration


def move_player(direction, verb):
    player_location.room = player_location.room.connecting_rooms[direction].room
    return f"You {verb} {direction} to {player_location.room.display_name}"


#will find name for first item in room or connecting item list
# that contains the noun extracted from the list of display names in room
def resolve_noun_to_item_name(active, passive, room: Room = None) -> (str, str):
    if room is None: room = player_location.room
    if active == "":
        return "", ""

    p, a = "", ""

    for name, item in room.item_list.items():
        if active in item.item.display_name:
            a = name
            if passive == active:
                return a, a
        if passive in item.item.display_name:
            p = name

    if a != "" and p != "": return a, p

    for name, item in player_inventory.items():
        if active in item.display_name:
            a = name
            if passive == active:
                return a, a
        if passive in item.display_name:
            p = name

    if a != "" and p != "": return a, p

    for conn in room.connecting_rooms.values():
        if conn.connector_item is not None:

            if active in conn.connector_item.display_name:
                a = conn.connector_item.name
                if passive == active:
                    return a, a
            if passive in conn.connector_item.display_name:
                p = conn.connector_item.name

    # If item not found, return user typed items for error message
    if a == "": a = active
    if p == "": p = passive

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


def main():
    setup_global_collections()
    while True:
        print(player_location.room.get_room_narration())
        val = input(">>")
        if val == "exit":
            break
        print(get_next_narration(val))

if __name__ == "__main__":
    main()