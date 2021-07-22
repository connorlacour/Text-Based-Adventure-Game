from data_objects import Item, SceneryItem, Room, CollectiveItem, RoomConnector , InventoryItem
from typing import Dict, List


player_inventory: Dict[str, Item] = {}
rooms: Dict[str, Room] = {}
items: Dict[str, Item] = {}

def setup_global_collections():

    r = [dining_room, foyer, kitchen, bathroom]
    i: List[Item] = [door, stairs, dining_table, pig, scroll, plates, chairs]

    for item in i:
        items[item.name] = item

    for room in r:
        rooms[room.name] = room

    dining_room.set_room_map([
        RoomConnector(direction="RIGHT", room_name="kitchen", connector_item="door_to_kitchen", article="a"),
        RoomConnector(direction="UPWARDS", room_name="bathroom", connector_item="stairs_to_foyer", narrative_text="There are $$this heading $$direction", known_to_player=True),
        RoomConnector(direction="BEHIND", room_name="foyer", narrative_text="$$direction you is the $$this")
    ])


    dining_room.add_items({
        "chairs": "CHAIRS litter the ground and ",
        "plates": "PLATES are scattered on the a DINING TABLE. ",
        "dining_table": "In the center of the DINING_TABLE there is a ",
        "pig": "PIG",
        "scroll": " with a ROLLED-UP-SCROLL wedged in it's mouth. "
    })



dining_room = Room(
    name="dining_room",
    display_name="DINING ROOM",
    article="the",
    long_description="You walk briskly in to the dining room with a grand DINING TABLE.  At once you notice that the former occupants must have left in great haste, for there are the blackened remnants of food on the PLATES, and the CHAIRS have been pushed away with little regard. Rats skitter away form the putrid remains of the forsaken dinner as you enter \nThe rats haven't seemed to have touched the main dish - a fully intact PIG lies upon the table, and a ROLLED UP SCROLL has been wedged in its mouth.",
    short_description="You are in the dining room."
)

foyer = Room(
    name="foyer",
    display_name="FOYER",
    article="the",
    long_description="Idk long descr whatever",
    short_description="Idk short descr whatever"
)

kitchen = Room(
    name="kitchen",
    display_name="KITCHEN",
    article="a",
    long_description="Idk long descr whatever",
    short_description="Idk short descr whatever"
)

bathroom = Room(
    name="bathroom",
    display_name="BATHROOM",
    article="a",
    long_description="Idk long descr whatever",
    short_description="Idk short descr whatever"
)

door = SceneryItem(
    name="door_to_kitchen",
    display_name="CLOSED DOOR",
    description="It's a closed door. You don't live in a barn."
)

stairs = SceneryItem(
    name="stairs_to_foyer",
    display_name="STAIRS",
    description="I warned you bro, I warned you about the STAIRS..."
)


dining_table = SceneryItem(
    name="dining_table",
    display_name="DINING TABLE",
    description="Strewn with rotting food and even a stuffed pig. Who could have left it in such a state?"
)

pig = SceneryItem(
    name="pig",
    display_name="PIG",
    description="A stuffed pig.  It seems in bad taste."
)

scroll = InventoryItem(
    name="scroll",
    display_name="ROLLED-UP SCROLL",
    description="You grab the scroll, unroll it and see that there is only one words, written in blood: \"YEET\""
)

plates = CollectiveItem(
    name="plates",
    display_name="PLATES",
    description="Dirty, nasty plates. You'd have these cleaned in a jiffy if you hadn't "
                "already eaten all the Tide Pods.",
    singular_display_name="PLATE",
    singular_description="A grody PLATE you grabbed from the DINING TABLE.  You probably wouldn't eat on it.",
    max_count=5
)

chairs = CollectiveItem(
    name="chairs",
    display_name="CHAIRS",
    description="Fine wooden chairs with attached seat cushions.",
    singular_display_name="CHAIR",
    singular_description="A fine CHAIR. Should come in handy if you get in a wrestling match.",
    max_count=5
)

