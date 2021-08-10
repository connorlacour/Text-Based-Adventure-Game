from parse_cmd import *
from game_objects.event import *
from game_objects.synonyms import *
from game_objects.global_collections import *


class GameLoop:

    def __init__(self):

        self.player_position = rooms["foyer"]
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

    elif verb in look_synonyms or active_object == "INVENTORY":

        if active_object == "":
            player_location.room.visited = False
            return "You LOOK AROUND."
        elif active_object == "INVENTORY":
            return print_inventory()
        else:
            return look_at_object(active_object)

    elif verb == "HELP":
        str = "GAME COMMANDS:\n" \
              "   LOOK AROUND: check surroundings\n" \
              "   LOOK at [item]: view item description\n" \
              "   GO [direction, room name]: travel to room\n" \
              "   TAKE [item]: add item to inventory\n" \
              "   DROP [item]: remove item from inventory\n" \
              "   CHECK INVENTORY: view held items\n" \
              "   VERB [itemA] on [itemB]: VERB one item on another\n"

        verb_set = f"Other verbs to try: {list(player_location.room.get_item_event_synonym_mapping().keys())}"

        return str + verb_set

    elif active_object == "":
        narration = resolve_itemless_events(verb)
        if narration == "":
            narration = f"You try to {verb} to no avail."
        return narration

    elif verb in take_synonyms:
        return take_item(verb, passive_object, active_object)

    elif verb in drop_synonyms:
        return drop_object(active_object)

    else:
        start_time = time.time()
        narration = resolve_event_item(verb, active_object, passive_object)
        print("Resolve event --- %s seconds ---" % (time.time() - start_time))

        if narration == "":
            narration = f"You try to {verb} to no avail."
        return narration


def take_item(verb,active_object, passive_object) -> str:
    connector_obj = player_location.room.get_connector_item_dict().get(active_object)

    if connector_obj is not None:
        event = connector_obj.get_event_from_verb(verb)
        if event is not None:
            return event.do_event(player_location.room, verb)

    return take_object(verb, active_object)


def look_at_object(obj_name):
    obj = get_item_in_player_scope(obj_name)
    if obj is not None:
        return obj.description
    else:
        return "There is no {obj_name} to look at."


def take_object(verb, object_name):
    narration = ""
    if object_name in player_location.room.item_list or object_name in player_location.room.discarded_items.keys():

        obj = get_item_in_player_scope(object_name)
        if obj.can_take:
            narration = move(f"move {object_name} to player_inventory", player_location.room)
            if narration == "":
                narration = f"You {verb} the {obj.display_name} and put it in your INVENTORY"
        else:
            narration = f"You can't {verb} the {obj.display_name}!"

    if narration == "":
        if object_name in items:
            obj = items[object_name]
            narration = f"You can't {verb} {obj.display_name} !"
        else:
            return f"You can't take that!"
    return narration


def drop_object(object_name):
    return drop(object_name, player_location.room, True)


def resolve_event_item(verb, active, passive):
    in_scope_event_map = in_scope_event_synonym_mapping()

    if verb in in_scope_event_map:  # verb exists in room.items, discard, or inventory.items event lists map
        verb_items = in_scope_event_map[verb]

        if active in verb_items or passive in verb_items:  # active object exists in player scope
            active_item = get_item_in_player_scope(active)

            if active != passive:  # passive item specified

                dict_key = f"{verb},{passive}".upper()
                if active_item is not None:
                    active_event = active_item.get_event_from_verb(dict_key)
                    if active_event is not None:

                        if get_item_in_player_scope(passive) is not None:
                            return active_event.do_event(player_location.room, verb, get_item_in_player_scope(passive).display_name)
                        else:  # passive item not in player scope
                            passive = items[passive]
                            return f"You feel as though {passive.display_name} is out of reach!"

                    else:  # verb exists, active item exists, no event exists involving passive item.
                        passive_item = get_item_in_player_scope(passive)
                        if passive_item is not None:  # Swap passive and active and see if event exists b/c parser error maybe
                            dict_key = f"{verb},{active}".upper()
                            event = passive_item.get_event_from_verb(dict_key)
                            if event is not None:
                                return event.do_event(player_location.room, verb, )
                            else:  # Passive item exists but nothing matched.
                                return f"You try to {verb} with a {passive_item.display_name} and {active}, but nothing happens"

            # If passive item not specified or nothing is found with the passive object, search for active object
            active_event = active_item.get_event_from_verb(verb)
            if active_event is not None:
                return active_item.do_event(verb)
            elif active != passive:
                passive_item = get_item_in_player_scope(passive)
                # If nothing is found with just active object, search for passive object
                if passive_item is not None:
                    passive_event = passive_item.get_event_from_verb(verb)
                    if passive_event is not None:
                        return passive_item.do_event(verb)

                # I have no idea how you would get to this line, logically.
                return f"You can't {verb} with a {active} and {passive}!"

    narration = ""
    # If we get to this point, we havent matched with verb to any item.
    if active == passive: #Only one object specified. Might be a global event matching to a nonexistant item like CLAP hands. HUM song.
        narration = resolve_itemless_events(verb)
    if narration == "":
        return f"{verb} didn't work! You might try rewording your entry or trying a different action."
    else: return narration


def resolve_itemless_events(verb):
    player_room  = player_location.room
    narration = ""
    if verb in list(global_events):
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


# I'm sorry for this method
# will find name for first item in room or connecting item list
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

    for name, item in room.discarded_items.items():
        if active in item.display_name:
            a = name
            if passive == active:
                return a, a
        if passive in item.display_name:
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
        # Check if room name was passed in instead of direction and pull direction for processing
        if dir == "":
            for x in room.connecting_rooms:
                if item.lower() in room.connecting_rooms[x].room_name:
                    dir = x
                    break
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

def main():
    from save_load import start_new_game
    start_new_game()
    while True:
        print(player_location.room.get_room_narration())
        val = input(">>")
        if val == "exit":
            break
        print(get_next_narration(val))


if __name__ == "__main__":
    main()