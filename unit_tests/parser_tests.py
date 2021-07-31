from game_objects.global_collections import setup_global_collections, rooms
from parse_cmd import *
import unittest

class TestParse(unittest.TestCase):
    def test1(self):

        test_cmd = parse_entry("Put key in lock")
        expect_parse = {"verb": "PUT", "a_obj": "KEY", "p_obj": "LOCK"}
        self.assertTrue(test_cmd == expect_parse)

    def test2(self):
        test_cmd = parse_entry("eat apple")
        expect_parse = {"verb": "EAT", "a_obj": "APPLE"}
        self.assertTrue(test_cmd == expect_parse)

    def test3(self):
        test_cmd = parse_entry("Go North")
        expect_parse = {"verb": "GO", "dir": "NORTH"}
        self.assertTrue(test_cmd == expect_parse)

    def test4(self):
        test_cmd = act_exists("select")
        expect_exist = "CHOOSE"
        self.assertTrue(test_cmd == expect_exist)

    setup_global_collections()

    def testGenerateRoomDescription(self):
        d = rooms["dining_room"]
        first_visit_text = "You walk briskly in to the dining room with a grand DINING TABLE.  At once you notice that the former occupants must have left in great haste, for there are the blackened remnants of food on the PLATES, and the CHAIRS have been pushed away with little regard. Rats skitter away form the putrid remains of the forsaken dinner as you enter \nThe rats haven't seemed to have touched the main dish - a fully intact PIG lies upon the table, and a ROLLED UP SCROLL has been wedged in its mouth.\nTo your RIGHT is a CLOSED DOOR. There are STAIRS heading UPWARDS leading to a BATHROOM. BEHIND you is the FOYER. "
        second_visit_text = "You are in the dining room. CHAIRS litter the ground and PLATES are scattered on the a DINING TABLE. In the center of the DINING_TABLE there is a PIG with a ROLLED-UP-SCROLL wedged in it's mouth. \nTo your RIGHT is a CLOSED DOOR. There are STAIRS heading UPWARDS leading to a BATHROOM. BEHIND you is the FOYER. "

        self.assertTrue(d.get_room_narration() == first_visit_text)
        self.assertTrue(d.get_room_narration() == second_visit_text)

if __name__ == '__main__':
    unittest.main()
