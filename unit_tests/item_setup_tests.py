import unittest
from global_collections import setup_global_collections, rooms, items
from pprint import pprint
from object_schemas import *

class ItemSetupTests(unittest.TestCase):

    def testItemSerialization(self):
        setup_global_collections()
        test_json = """[{"name": "door_to_kitchen", "display_name": "CLOSED DOOR", "article": "the", "description": "It's a closed door. You don't live in a barn.", "type": "Scenery"}, {"name": "stairs_to_foyer", "display_name": "STAIRS", "article": "the", "description": "I warned you bro, I warned you about the STAIRS...", "type": "Scenery"}, {"name": "dining_table", "display_name": "DINING TABLE", "article": "the", "description": "Strewn with rotting food and even a stuffed pig. Who could have left it in such a state?", "type": "Scenery"}, {"name": "pig", "display_name": "PIG", "article": "the", "description": "A stuffed pig.  It seems in bad taste.", "type": "Scenery"}, {"name": "scroll", "display_name": "ROLLED-UP SCROLL", "article": "the", "description": "You grab the scroll, unroll it and see that there is only one words, written in blood: \\"YEET\\"", "can_take": false, "type": "Inventory"}, {"name": "plates", "display_name": "PLATES", "article": "the", "description": "Dirty, nasty plates. You'd have these cleaned in a jiffy if you hadn't already eaten all the Tide Pods.", "singular_display_name": "PLATE", "singular_description": "A grody PLATE you grabbed from the DINING TABLE.  You probably wouldn't eat on it.", "type": "Collective"}, {"name": "chairs", "display_name": "CHAIRS", "article": "the", "description": "Fine wooden chairs with attached seat cushions.", "singular_display_name": "CHAIR", "singular_description": "A fine CHAIR. Should come in handy if you get in a wrestling match.", "type": "Collective"}]"""

        serialized_items = ItemSchema().dumps(items.values(), many=True)
        self.assertTrue(test_json == serialized_items)
        pprint(serialized_items)

    def testItemDeserialization(self):

        result = load_items_from_file("items.json")
        self.assertTrue(len(result) == 7)
        pprint(result)

    def testRoomDeserialization(self):
        setup_global_collections()

        schema = RoomSchema()
        room = rooms.values()
        result = schema.dumps(room, many=True)
        pprint(result)

    def testRoomSerialization(self):

        schema = RoomSchema()
        result = load_rooms_from_file('rooms.json')
        self.assertTrue(len(result) == 4)
        pprint(result)

    def testGenerateRoomDescription(self):
        setup_global_collections()
        r = rooms["dining_room"]

        long_text = "You walk briskly in to the dining room with a grand DINING TABLE.  At once you notice that the former occupants must have left in great haste, for there are the blackened remnants of food on the PLATES, and the CHAIRS have been pushed away with little regard. Rats skitter away form the putrid remains of the forsaken dinner as you enter \nThe rats haven't seemed to have touched the main dish - a fully intact PIG lies upon the table, and a ROLLED UP SCROLL has been wedged in its mouth."
        rooms_text = "To your RIGHT is a KITCHEN. There are STAIRS heading UPWARDS leading to a BATHROOM. BEHIND you is the FOYER. "
        item_list_text = """CHAIRS litter the ground and PLATES are scattered on the a DINING TABLE. In the center of the DINING_TABLE there is a PIG with a ROLLED-UP-SCROLL wedged in it's mouth. """

        self.assertTrue(r.long_description == long_text)
        self.assertTrue(r.room_list_narration() == rooms_text)
        self.assertTrue(r.item_list_narration() == item_list_text)

        self.assertTrue(r.get_room_narration() == long_text + "\n" + rooms_text)
        self.assertTrue(r.get_room_narration() == r.short_description + " " + item_list_text + "\n" + rooms_text)

if __name__ == '__main__':
    unittest.main()

def setup_global_collections_from_code_obj():

    r: List[Room] = [dining_room, foyer, kitchen, bathroom]
    i: List[Item] = [door, stairs, dining_table, pig, scroll, plates, chairs]

    for item in i:
        items[item.name] = item

    for room in r:
        rooms[room.name] = room

    for room in rooms.values():
        room.setup_on_start()

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
    short_description="You are in the dining room.",
    item_setup_dict={
        "chairs": "CHAIRS litter the ground and ",
        "plates": "PLATES are scattered on the a DINING TABLE. ",
        "dining_table": "In the center of the DINING_TABLE there is a ",
        "pig": "PIG",
        "scroll": " with a ROLLED-UP-SCROLL wedged in it's mouth. "
    },
    room_list=[
        RoomConnector(direction="RIGHT", room_name="kitchen", connector_item_name="door_to_kitchen", article="a"),
        RoomConnector(direction="UPWARDS", room_name="bathroom", connector_item_name="stairs_to_foyer",
                      narrative_text="There are $$this heading $$direction", known_to_player=True),
        RoomConnector(direction="BEHIND", room_name="foyer", narrative_text="$$direction you is the $$this")
    ]
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
    description="You grab the scroll, unroll it and see that there is only one words, written in blood: \"YEET\"",
    can_take=False
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


