import unittest
from pprint import pprint
import sys
sys.path.append('../')
from game_objects.global_collections import *
from game_objects.object_schemas import *
from game_objects.room import Room, RoomConnector

test_dir = os.path.dirname(__file__)


def get_test_file_name(filename: str):
    return os.path.join(test_dir, f'{filename}')

class ItemSetupTests(unittest.TestCase):

    def usingTestFolder(self):
        self.assertTrue("unit_tests" in get_test_file_name("templates/game_items"))

    def testDropEvent(self):
        setup_global_collections_for_test(test_dir)

        move_events = [
            "drop glove"
        ]

        e = ItemEvent(move_events)

        print(e.do_event(player_location.room))


    def testMoveEvents(self):
        setup_global_collections_for_test(test_dir)

        move_events = [
            "move player to closet",
            "move player to living room"
        ]

        e = ItemEvent(move_events)

        print(e.do_event(player_location.room))
        self.assertTrue(player_location.room.name == "closet")

        move_events = [
            "move coat to foyer",
            "move katana to upstairs hallway",
            "move painting to kitchen"
        ]

        self.assertTrue("coat" in rooms["closet"].item_list)
        print(ItemEvent(move_events).do_event(player_location.room))
        self.assertFalse("coat" in rooms["closet"].item_list)
        self.assertTrue(rooms["foyer"].get_item_from_room("coat") is not None)



    def testChangeEvents(self):
        setup_global_collections_for_test(test_dir)

        change_events = [
           """change dog display_name to `CALM DOG`""",
            """change silver_key can_take to True""",
            """change attic.direction.north narrative_text to `The BOOKCASE slides to the side revealing a walk-in safe with a KEYPAD.`"""
        ]

        e = ItemEvent(change_events)

        print("Change Event Output: \n" + e.do_event(player_location.room))

        print(items["dog"].display_name)
        self.assertTrue(items["dog"].display_name == "CALM DOG")
        self.assertTrue(items["silver_key"].can_take == True)
        self.assertTrue(rooms["attic"].connecting_rooms["NORTH"].narrative_text == "The BOOKCASE slides to the side revealing a walk-in safe with a KEYPAD.")

    def testPrintEvent(self):
        setup_global_collections_for_test(test_dir)

        print_events_1 = [
            """print Hi!""",
            """print You're a smelly sock""",
        ]
        print_events_output_1 = ItemEvent(print_events_1).do_event(player_location.room)

        expected_output_1 = "Hi!\nYou're a smelly sock\n"

        self.assertTrue(print_events_output_1 == expected_output_1)


if __name__ == '__main__':
    unittest.main()

