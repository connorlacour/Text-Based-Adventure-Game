import unittest
from pprint import pprint

from game_objects.game_loop import *
from game_objects.global_collections import *
from game_objects.object_schemas import *
from game_objects.event import *
from game_objects.room import Room, RoomConnector

test_dir = os.path.dirname(__file__)


def get_test_file_name(filename: str):
    return os.path.join(test_dir, f'{filename}')

# class ItemSetupTests(unittest.TestCase):
#
#     def usingTestFolder(self):
#         self.assertTrue("unit_tests" in get_test_file_name("templates/items"))
#
#     def testPrintEvent(self):
#         setup_global_collections_for_test(test_dir)
#
#         print_events_1 = [
#             """print Hi!""",
#             """print You are a smelly sock""",
#         ]
#         print_events_output_1 = Event(print_events_1).do_event(player_location.room)
#
#         expected_output_1 = 'Hi!\nYou are a smelly sock\n'
#
#         print_events_2 = [
#             "print \"Hi!\"",
#         ]
#         expected_output_2 =  "\"Hi!\"\n"
#
#         print_events_output_2 = Event(print_events_2).do_event(player_location.room)
#         self.assertTrue(print_events_output_1 == expected_output_1)
#         self.assertTrue(print_events_output_2 == expected_output_2)
#
#         print("Print Event Output: \n" + print_events_output_1 + print_events_output_2)
#
#
#     def testItemSerialization(self):
#         setup_global_collections_for_test(test_dir)
#         test_json = """[{"name": "door_to_kitchen", "display_name": "CLOSED DOOR", "events": {}, "article": "the", "description": "It's a closed door. You don't live in a barn.", "type": "Scenery"}, {"name": "stairs_to_bathroom", "display_name": "STAIRS", "events": {}, "article": "the", "description": "I warned you bro, I warned you about the STAIRS...", "type": "Scenery"}, {"name": "dining_table", "display_name": "DINING TABLE", "events": {}, "article": "the", "description": "Strewn with rotting food and even a stuffed pig. Who could have left it in such a state?", "type": "Scenery"}, {"name": "pig_scroll", "display_name": "PIG WITH SCROLL", "events": {}, "article": "the", "description": "It's a pig... it's got a scroll... that's whack", "can_take": true, "type": "Inventory"}, {"name": "pig", "display_name": "PIG", "events": {"COMBINE,SCROLL": {"events": ["print You combine the PIG and the SCROLL.", "move scroll to limbo", "move pig to limbo", "move pig_scroll to player_room"], "repeatable": true, "passive_obj": "SCROLL"}, "COMBINE,PLATES": {"events": ["print What the heck are you talking about??"], "repeatable": true, "passive_obj": "PLATES"}}, "article": "the", "description": "A stuffed pig.  It seems in bad taste.", "type": "Scenery"}, {"name": "scroll", "display_name": "ROLLED-UP SCROLL", "events": {}, "article": "the", "description": "You grab the scroll, unroll it and see that there is only one words, written in blood: \\"YEET\\"", "can_take": true, "type": "Inventory"}, {"name": "plates", "display_name": "PLATES", "events": {"WASH": {"events": ["print You try to $$verb the plate, with what? Your tongue?"], "repeatable": true, "passive_obj": ""}}, "article": "the", "description": "Dirty, nasty plates. You'd have these cleaned in a jiffy if you hadn't already eaten all the Tide Pods.", "singular_display_name": "PLATE", "singular_description": "A grody PLATE you grabbed from the DINING TABLE.  You probably wouldn't eat on it.", "max_count": 5, "type": "Collective"}, {"name": "chairs", "display_name": "CHAIRS", "events": {"WASH": {"events": ["print You try to $$verb the plate, with what? Your tongue?"], "repeatable": true, "passive_obj": ""}, "PLACE,PIG": {"events": ["print You place on the chair. Goodbye."], "repeatable": true, "passive_obj": "PIG"}}, "article": "the", "description": "Fine wooden chairs with attached seat cushions.", "singular_display_name": "CHAIR", "singular_description": "A fine CHAIR. Should come in handy if you get in a wrestling match.", "max_count": 5, "type": "Collective"}]"""
#         serialized_items = ItemSchema().dumps(items.values(), many=True)
#         self.assertTrue(test_json == serialized_items)
#         pprint(serialized_items)
#
#     def testItemDeserialization(self):
#
#         result = load_items_from_file(get_test_file_name("templates/items.json"))
#         self.assertTrue(len(result) == 8)
#         pprint(result)
#
#     def testRoomSerialization(self):
#         setup_global_collections_for_test(test_dir)
#
#         schema = RoomSchema()
#         room = rooms.values()
#         result = schema.dumps(room, many=True)
#         pprint(result)
#
#     def testRoomDeserialization(self):
#
#         schema = RoomSchema()
#         result = load_rooms_from_file(get_test_file_name('templates/rooms.json'))
#         self.assertTrue(len(result) == 5)
#         pprint(result)
#
#
# if __name__ == '__main__':
#     unittest.main()

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
        RoomConnector(direction="UPWARDS", room_name="bathroom", connector_item_name="stairs_to_bathroom",
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
    name="stairs_to_bathroom",
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
    max_count=5,
    events={"WASH": Event(["print You try to $$verb the plate, with what? Your tongue?"])}
)

chairs = CollectiveItem(
    name="chairs",
    display_name="CHAIRS",
    description="Fine wooden chairs with attached seat cushions.",
    singular_display_name="CHAIR",
    singular_description="A fine CHAIR. Should come in handy if you get in a wrestling match.",
    max_count=5
)


