from game_objects.global_collections import setup_global_collections, rooms
from parse_cmd import *
import unittest

test_dir = os.path.dirname(__file__)
class TestParse(unittest.TestCase):


    def test1(self):
        verb, direction, passive_obj, active_object = parse_entry("Put key in lock")
        self.assertTrue(verb == "PUT")
        self.assertTrue(active_object == "KEY")
        self.assertTrue(passive_obj == "LOCK")

    def test2(self):
        verb, direction, passive_obj, active_object = parse_entry("eat apple")
        self.assertTrue(verb == "EAT")
        self.assertTrue(active_object == "APPLE")

    def test_go_through_door(self):
        verb, direction, passive_obj, active_object = parse_entry("Go through locked door")
        self.assertTrue(verb == "GO")
        self.assertTrue(passive_obj == "DOOR")

    def test_noun_and_verb(self):
        verb, direction, passive_obj, active_object = parse_entry("Go through locked door")
        self.assertTrue(verb == "GO")
        self.assertTrue(passive_obj == "DOOR")

    def test_pick_up(self):
        verb, direction, passive_obj, active_object = parse_entry("Pick up the apple")
        self.assertTrue(verb == "PICK UP")
        self.assertTrue(active_object == "APPLE")

    def test_two_obj_no_prep(self):
        verb, direction, passive_obj, active_object = parse_entry("COMBINE PIG AND SCROLL")
        self.assertTrue(active_object == "PIG")
        self.assertTrue(passive_obj == "SCROLL")

    def test3(self):
        setup_global_collections_for_test(test_dir = test_dir)
        verb, direction, passive_obj, active_object = parse_entry("Go North")
        self.assertTrue(verb == "GO")
        self.assertTrue(direction == "NORTH")

    def test4(self):
        test_cmd = act_exists("select")
        expect_exist = "CHOOSE"
        self.assertTrue(test_cmd == expect_exist)

if __name__ == '__main__':
    unittest.main()
