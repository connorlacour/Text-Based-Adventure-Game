import unittest
from pprint import pprint

from game_objects.global_collections import *
from game_objects.object_schemas import *
from game_objects.item_event import *
from game_objects.room import Room, RoomConnector

test_dir = os.path.dirname(__file__)


def get_test_file_name(filename: str):
    return os.path.join(test_dir, f'{filename}')


class ItemSetupTests(unittest.TestCase):

    def usingTestFolder(self):
        self.assertTrue("unit_tests" in get_test_file_name("templates/items"))

    def testDropEvent(self):
        setup_global_collections_for_test(test_dir)

        move_events = [
            "drop pig"
        ]

        e = ItemEvent(move_events)

        print(e.do_event(player_location.room))

    def testMoveEvents(self):
        setup_global_collections_for_test(test_dir)

        move_events = [
            "move player to foyer",
            "move player to empire_state_building"
        ]

        e = ItemEvent(move_events)

        print(e.do_event(player_location.room))
        self.assertTrue(player_location.room.name == "foyer")

        move_events = [
            "move pig to foyer",
            "move plates to limbo",
            "move bimbus to takkawut",
            "move your booty real fast",
            "move plates to urmoms_house"
        ]

        self.assertTrue("pig" in rooms["dining_room"].item_list)
        print(ItemEvent(move_events).do_event(player_location.room))
        self.assertFalse("pig" in rooms["dining_room"].item_list)
        self.assertTrue(rooms["foyer"].get_item_from_room("pig") is not None)

    def testChangeEvents(self):
        setup_global_collections_for_test(test_dir)

        change_events = [
            """change pig display_name to `BIG PIG`""",
            f"""change pig display_name to BOING""",
            """change pig bobs to `BIG PIG`""",
            """change meow max_count to 5""",
            """change plates max_count to 7""",
            """change dining_room.direction.upwards known_to_player to False"""
        ]

        e = ItemEvent(change_events)

        print("Change Event Output: \n" + e.do_event(player_location.room))

        self.assertTrue(items["pig"].display_name == "BOING")
        self.assertTrue(items["plates"].max_count == 7)
        self.assertTrue(rooms["dining_room"].connecting_rooms["UPWARDS"].known_to_player == False)

    def testPrintEvent(self):
        setup_global_collections_for_test(test_dir)

        print_events_1 = [
            """print Hi!""",
            """print You are a smelly sock""",
        ]
        print_events_output_1 = ItemEvent(print_events_1).do_event(player_location.room)

        expected_output_1 = 'Hi!\nYou are a smelly sock\n'

        print_events_2 = [
            "print \"Hi!\"",
        ]
        expected_output_2 = "\"Hi!\"\n"

        print_events_output_2 = ItemEvent(print_events_2).do_event(player_location.room)
        self.assertTrue(print_events_output_1 == expected_output_1)
        self.assertTrue(print_events_output_2 == expected_output_2)

        print("Print Event Output: \n" + print_events_output_1 + print_events_output_2)

    def testItemSerialization(self):
        setup_global_collections_for_test(test_dir)
        test_json = """[{"name": "door_to_kitchen", "display_name": "CLOSED DOOR", "events": {}, "article": "the", "description": "It's a closed door. You don't live in a barn.", "type": "Scenery"}, {"name": "stairs_to_foyer", "display_name": "STAIRS", "events": {}, "article": "the", "description": "I warned you bro, I warned you about the STAIRS...", "type": "Scenery"}, {"name": "dining_table", "display_name": "DINING TABLE", "events": {}, "article": "the", "description": "Strewn with rotting food and even a stuffed pig. Who could have left it in such a state?", "type": "Scenery"}, {"name": "pig", "display_name": "PIG", "events": {}, "article": "the", "description": "A stuffed pig.  It seems in bad taste.", "type": "Scenery"}, {"name": "scroll", "display_name": "ROLLED-UP SCROLL", "events": {}, "article": "the", "description": "You grab the scroll, unroll it and see that there is only one words, written in blood: \\"YEET\\"", "can_take": false, "type": "Inventory"}, {"name": "plates", "display_name": "PLATES", "events": {"WASH": {"events": ["print You try to $$verb the plate, with what? Your tongue?"], "passive_obj": ""}}, "article": "the", "description": "Dirty, nasty plates. You'd have these cleaned in a jiffy if you hadn't already eaten all the Tide Pods.", "singular_display_name": "PLATE", "singular_description": "A grody PLATE you grabbed from the DINING TABLE.  You probably wouldn't eat on it.", "max_count": 5, "type": "Collective"}, {"name": "chairs", "display_name": "CHAIRS", "events": {}, "article": "the", "description": "Fine wooden chairs with attached seat cushions.", "singular_display_name": "CHAIR", "singular_description": "A fine CHAIR. Should come in handy if you get in a wrestling match.", "max_count": 5, "type": "Collective"}]"""
        serialized_items = ItemSchema().dumps(items.values(), many=True)
        self.assertTrue(test_json == serialized_items)
        pprint(serialized_items)

    def testItemDeserialization(self):

        result = load_items_from_file(get_test_file_name("templates/items.json"))
        self.assertTrue(len(result) == 7)
        pprint(result)

    def testRoomSerialization(self):
        setup_global_collections_for_test(test_dir)

        schema = RoomSchema()
        room = rooms.values()
        result = schema.dumps(room, many=True)
        pprint(result)

        return result

    def testRoomDeserialization(self):

        schema = RoomSchema()
        result = load_rooms_from_file(get_test_file_name('templates/rooms.json'))
        self.assertTrue(len(result) == 4)
        pprint(result)

    def testGenerateRoomDescription(self):
        setup_global_collections_for_test(test_dir)
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

    dining_room.set_item_list({
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

# plates = CollectiveItem(
#     name="plates",
#     display_name="PLATES",
#     description="Dirty, nasty plates. You'd have these cleaned in a jiffy if you hadn't "
#                 "already eaten all the Tide Pods.",
#     singular_display_name="PLATE",
#     singular_description="A grody PLATE you grabbed from the DINING TABLE.  You probably wouldn't eat on it.",
#     max_count=5,
#     events={"WASH": ItemEvent(["print You try to $$verb the plate, with what? Your tongue?"])}
# )

chairs = CollectiveItem(
    name="chairs",
    display_name="CHAIRS",
    description="Fine wooden chairs with attached seat cushions.",
    singular_display_name="CHAIR",
    singular_description="A fine CHAIR. Should come in handy if you get in a wrestling match.",
    max_count=5
)


