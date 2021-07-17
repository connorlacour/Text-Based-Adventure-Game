from parse_cmd import parse_entry
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


if __name__ == '__main__':
    unittest.main()
