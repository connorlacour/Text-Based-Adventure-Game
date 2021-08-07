from game_objects.global_collections import *
from game_objects.object_schemas import *
from unit_tests.item_setup_tests import *
from gui.text_scroll import Scroll
from unit_tests.item_setup_tests import *
import os
import marshmallow
import json
import unittest


class Save:
    def __init__(self, save_file_name: str, cur_scroll: Scroll):
        self.game_data = {
            "room_files": [],
            "item_files": [],
            "text_scroll": [],
            "player": []}
        self.save_file_name = save_file_name
        self.home_dir = os.getcwd()
        self.scroll = cur_scroll

    def get_rooms(self):
        pass

    def get_items(self):
        pass

    def get_player_info(self):
        pass

    def get_text_scroll(self):
        return self.scroll.text_in_scroll

    def get_json_file_list(self):
        room_dir = r".\default_items\room_files"
        item_dir = r".\default_items\item_files"
        rooms_loaded = []
        items_loaded = []

        jsons_to_load = {"rooms": [], "items": []}

        for room_json in os.listdir(room_dir):
            if room_json.endswith(".json"):
                jsons_to_load["rooms"].append(room_json)

        for item_json in os.listdir(item_dir):
            if item_json.endswith(".json"):
                jsons_to_load["items"].append(item_json)

        for room in jsons_to_load["rooms"]:
            rooms_loaded.append(
                load_rooms_from_file(
                    os.path.join(room_dir, room)
                )
            )

        for item_collection in jsons_to_load["items"]:
            items_loaded.append(
                load_items_from_file(
                    os.path.join(item_dir, item_collection)
                )
            )

        self.game_data["room_files"] = rooms_loaded
        self.game_data["item_files"] = items_loaded

    def save_data(self):
        self.get_json_file_list()
        self.game_data["scroll"] = self.get_text_scroll()
        schema = RoomSchema()

        # nav to saves dir
        try:
            os.chdir(r".\saves")
        except FileNotFoundError:
            print('Internal Error')

        if self.save_file_name not in os.listdir():
            os.mkdir(self.save_file_name)
        os.chdir(self.save_file_name)

        items = []
        rooms = []

        for sub_dir in self.game_data.keys():

            if sub_dir not in os.listdir():
                os.mkdir(sub_dir)
            os.chdir(sub_dir)

            if sub_dir == "scroll":
                path = open("scroll.txt", mode="w+")
                for line in self.game_data["text_scroll"]:
                    path.writelines(str(line) + "\n")
                path.close()

            else:
                for element in self.game_data[sub_dir]:
                    if sub_dir == "item_files":
                        items.append(element)
                    elif sub_dir == "room_files":
                        rooms.append(element)
                    dumped = schema.dumps(element, many=True)
                    path = open(str(element[0]) + ".json", mode="w+")
                    path.write(dumped)
                    path.close()

            os.chdir("..")
        os.chdir(self.home_dir)
        return items, rooms


class LoadGame:
    def __init__(self, load_file_name):
        self.load_file_name = load_file_name
        self.game_data = {
            "room_files": [],
            "item_files": [],
            "text_scroll": [],
            "player": []}
        self.home_dir = os.getcwd()
        self.scroll = []
        self.load_dir = os.path.join(r".\saves", self.load_file_name)

        self.setup_game()

    def setup_game(self):
        # get starting location
        # TO WRITE
        starting_player_location = 'dining_room'

        self.load_object_files()
        self.load_scroll()

        # setup_rooms_and_items(
        #     self.game_data["item_files"],
        #     self.game_data["room_files"],
        #     starting_player_location
        # )

    def load_object_files(self):

        room_dir = os.path.join(self.load_dir, "room_files")
        item_dir = os.path.join(self.load_dir, "item_files")

        # find all room json files in dir
        # load rooms from file
        # append those rooms to list: rooms_loaded
        for room_json in os.listdir(room_dir):
            if room_json.endswith(".json"):
                print(room_json)
                self.game_data["room_files"].append(
                    load_rooms_from_file(
                        os.path.join(room_dir, room_json)
                    )
                )

        # find all item json files in dir
        # load items from file
        # append those items to list: items_loaded
        for item_json in os.listdir(item_dir):
            if item_json.endswith(".json"):
                print("item json: " + str(item_json))
                try:
                    loaded_items = load_items_from_file(
                            os.path.join(item_dir, item_json)
                        )
                    print(loaded_items)
                    self.game_data["item_files"].append(loaded_items)
                except marshmallow.exceptions.ValidationError:
                    print("Validation Error with: " + str(item_json))

    def load_scroll(self):
        scroll_file_path = os.path.join(
            self.load_dir,
            r"text_scroll\scroll.txt"
        )

        with open(scroll_file_path, mode="r") as file:
            self.scroll = file.readlines()
            self.scroll = [x.strip() for x in self.scroll]
            self.scroll.append("")


class initGameTest(unittest.TestCase):

    def test_init(self):
        test_scroll = Scroll(test=1)
        test = Save("connor2", test_scroll)

        # collect files to "load"
        test.get_json_file_list()

        # calls load_items_from_file() and load_rooms_from_file()
        items, rooms = test.save_data()


if __name__ == '__main__':
    unittest.main()


# test_scroll = Scroll(test=1)
# Save("connor1", test_scroll).save_data()

# LoadGame("connor7").load_scroll()

