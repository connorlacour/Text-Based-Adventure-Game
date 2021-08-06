import unittest
from pprint import pprint

from game_objects.game_loop import *

test_dir = os.path.dirname(__file__)


def get_test_file_name(filename: str):
    return os.path.join(test_dir, f'{filename}')


class NarrationTests(unittest.TestCase):


    # def testGetMeanins(self):
    #     import time
    #     import PyDictionary
    #
    #     d =PyDictionary.PyDictionary()
    #
    #     a = "The quick brown fox jumped over the lazy dog"
    #     for word in a.split(" "):
    #         start_time = time.time()
    #         d.meaning(word)
    #         print("meaning call: --- %s seconds ---" % (time.time() - start_time))
    #
    #

    def testNarration_pickup_drop(self):
        setup_global_collections_for_test(test_dir)
        e = get_next_narration("pick up scroll")
        print(e)
        self.assertTrue(player_inventory.get("scroll") is not None)

        get_next_narration("discard scroll")
        e = player_location.room.get_discard_narration()
        self.assertTrue(len(player_location.room.discarded_items) == 1)
        print(e)

    def test_scope_mapping(self):

        setup_global_collections_for_test(test_dir)

        e = get_next_narration("pick up scroll")
        self.assertTrue(player_inventory.get("scroll") is not None)

        print(in_scope_event_synonym_mapping())


    def testusingTestFolder(self):
        self.assertTrue("unit_tests" in get_test_file_name("templates/items"))


    def testRoom(self):
        setup_global_collections_for_test(test_dir)
        result = (rooms["dining_room"].get_item_event_synonym_mapping())
        print(result)
        self.assertTrue(True)


    def test_move_commands(self):
        setup_global_collections_for_test(test_dir)
        e = do_direction_command("GO", "UPWARDS")
        print(e)
        self.assertTrue(player_location.room.name == "bathroom")

        setup_global_collections_for_test(test_dir)
        e = do_direction_command("GO", "", "stairs_to_bathroom")
        print(e)
        self.assertTrue(player_location.room.name == "bathroom")


    def test_combine_pig_and_scroll(self):
        setup_global_collections_for_test(test_dir)

        a = resolve_event_item("COMBINE", "pig", "scroll")
        rooms["dining_room"].visited = True
        event_narration = "You combine the PIG and the SCROLL."
        substring = "In the center of the DINING_TABLE there is a a PIG WITH A SCROLL. That's whack."
        print(a)

        self.assertTrue(event_narration in a)
        self.assertTrue(substring in rooms["dining_room"].get_room_narration())

    def test_combine_pig_and_plates(self):
        setup_global_collections_for_test(test_dir)

        a = resolve_event_item("COMBINE", "pig", "plates")
        event_narration = "What the heck are you talking about??"
        print(a)

        self.assertTrue(event_narration in a)

    def test_resolve_items(self):
        setup_global_collections_for_test(test_dir)

        a, p = resolve_noun_to_item_name("TABLE", "SCROLL")
        self.assertTrue(a == "dining_table")
        self.assertTrue(p == "scroll")

        a, p = resolve_noun_to_item_name("STAIR", "BOLLS")
        self.assertTrue(a == "stairs_to_bathroom")
        self.assertTrue(p == "BOLLS")

    def testDropEvent(self):
        setup_global_collections_for_test(test_dir)

        move_events = [
            "drop pig"
        ]

        e = Event(move_events)

        print(e.do_event(player_location.room))


    def testMoveEvents(self):
        setup_global_collections_for_test(test_dir)

        move_events = [
            "move player to foyer",
            "move player to empire_state_building"
        ]

        e = Event(move_events)

        print(e.do_event(player_location.room))
        self.assertTrue(player_location.room.name == "foyer")

        move_events = [
            "move pig to foyer",
            "move plates to limbo",
            "move bimbus to takkawut",
            "move your booty real fast",
            "move plates to urmoms_house",
            "move scroll to player_inventory"
        ]

        self.assertTrue("pig" in rooms["dining_room"].item_list)
        print(Event(move_events).do_event(player_location.room))
        self.assertTrue("scroll" in player_inventory)
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
            """change dining_room.direction.upwards known_to_player to False""",
            "change pig narration to `That's one big pig`"
        ]

        e = Event(change_events)

        print("Change Event Output: \n" + e.do_event(player_location.room))

        self.assertTrue(items["pig"].display_name == "BOING")
        self.assertTrue(rooms["dining_room"].item_list["pig"].narration == "That's one big pig")

        self.assertTrue(items["plates"].max_count == 7)
        self.assertTrue(rooms["dining_room"].connecting_rooms["UPWARDS"].known_to_player == False)


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
