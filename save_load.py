from game_objects import global_collections
from gui.text_scroll import Scroll
from unit_tests.item_setup_tests import *
import os
import marshmallow
import json
import unittest

base_dir = os.path.dirname(__file__)
saves = os.path.join(base_dir, r"saves")


def start_new_game():
    room_dir = os.path.join(base_dir, r"default_items/room_files")
    item_dir = os.path.join(base_dir, r"default_items/item_files")

    rooms_loaded = []
    items_loaded = []

    home_dir = os.getcwd()
    jsons_to_load = {"rooms": [], "items": []}

    for room_json in os.listdir(room_dir):
        if room_json.endswith(".json"):
            jsons_to_load["rooms"].append(room_json)

    for item_json in os.listdir(item_dir):
        if item_json.endswith(".json"):
            jsons_to_load["items"].append(item_json)

    for room in jsons_to_load["rooms"]:
        try:
            read = load_rooms_from_file(
                os.path.join(room_dir, room)
            )
            rooms_loaded.append(read[0])
        except (json.decoder.JSONDecodeError, UnicodeDecodeError) as e:
            print(str(e) + " : " + str(room))

    for item_collection in jsons_to_load["items"]:
        try:
            read = load_items_from_file(
                os.path.join(item_dir, item_collection)
            )
            items_loaded.append(read)
        except (json.decoder.JSONDecodeError, UnicodeDecodeError) as e:
            print(str(e) + " : " + str(item_collection))

    os.chdir(home_dir)

    if len(items_loaded) > 1:
        temp = items_loaded[0]
        for x in items_loaded[1]:
            temp.append(x)
        items_loaded = temp
    else:
        items_loaded = items_loaded[0]

    setup_rooms_and_items(items_loaded, rooms_loaded, "foyer")


class SaveGame:
    def __init__(self, save_file_name: str, cur_scroll: Scroll):
        self.game_data = {
            "room_files": {},
            "item_files": {},
            "scroll": [],
            "player": {}}
        self.save_file_name = save_file_name
        self.home_dir = os.getcwd()
        self.scroll = cur_scroll

    @staticmethod
    def get_rooms():
        return global_collections.rooms

    @staticmethod
    def get_items():
        return global_collections.items.values()

    def get_player_info(self):
        self.game_data["player"]["player_location"] = \
            global_collections.player_location

        self.game_data["player"]["inventory"] = \
            global_collections.player_inventory

    def get_text_scroll(self):
        return self.scroll.text_in_scroll

    def save_data(self):
        # get data from global collections
        self.game_data["item_files"] = self.get_items()
        self.game_data["room_files"] = self.get_rooms()
        self.game_data["scroll"] = self.get_text_scroll()
        self.get_player_info()

        # create save dir if doesn't exist
        # nav to save dir
        if self.save_file_name not in os.listdir(saves):
            os.mkdir(os.path.join(saves, self.save_file_name))
        os.chdir(os.path.join(saves, self.save_file_name))

        # creat sub directories if they don't exist
        for sub_dir in self.game_data.keys():
            if sub_dir not in os.listdir():
                os.mkdir(sub_dir)

        self.write_scroll()
        self.write_items()
        self.write_rooms()
        self.write_player_info()

        os.chdir(self.home_dir)

    def write_player_info(self):
        os.chdir("player")

        with open("inventory.txt", "w+") as file:
            file.truncate(0)
            for item in self.game_data["player"]["inventory"]:
                file.writelines(item + "\n")
            file.close()

        with open("player_location.txt", "w+") as file:
            file.truncate(0)
            file.write(str(self.game_data["player"]["player_location"]))
            file.close()

        os.chdir("..")

    def write_rooms(self):
        os.chdir("room_files")

        keys = list(self.game_data["room_files"].keys())

        for x in keys:
            path = open(str(x) + ".json", mode="w+")
            path.write(
                RoomSchema().dumps(
                    [self.game_data["room_files"][x]], many=True
                )
            )
            path.close()

        os.chdir("..")

    def write_items(self):
        os.chdir("item_files")

        path = open("items.json", mode="w+")
        path.write(
            ItemSchema().dumps(
                self.game_data["item_files"], many=True
            )
        )

        path.close()
        os.chdir("..")

    def write_scroll(self):
        os.chdir("scroll")

        path = open("scroll.txt", mode="w+")
        for line in self.game_data["scroll"]:
            path.writelines(str(line) + "\n")

        path.close()
        os.chdir("..")


class LoadGame:
    def __init__(self, load_file_name):
        self.load_file_name = load_file_name
        self.game_data = {
            "room_files": [],
            "item_files": [],
            "text_scroll": [],
            "player": {}}
        self.home_dir = os.getcwd()
        self.scroll = []
        self.load_dir = os.path.join(saves, self.load_file_name)

        self.setup_game()

    def setup_game(self):
        self.load_rooms()
        self.load_items()
        self.load_scroll()
        self.load_player_data()

        setup_rooms_and_items(
            self.game_data["item_files"],
            self.game_data["room_files"],
            self.game_data["player"]["player_location"]
        )

        for x in self.game_data["player"]["inventory"]:
            global_collections.player_inventory[
                items[x].name] = x

    def load_rooms(self):
        room_dir = os.path.join(self.load_dir, "room_files")

        # find all room json files in dir
        # load rooms from file
        # append those rooms to list: rooms_loaded
        for room_json in os.listdir(room_dir):
            if room_json.endswith(".json"):
                try:
                    loaded_rooms = load_rooms_from_file(
                        os.path.join(room_dir, room_json)
                    )
                    self.game_data["room_files"].append(loaded_rooms[0])
                except marshmallow.exceptions.ValidationError:
                    print("Validation Error with: ", str(room_json))

        print("rooms ->", str(self.game_data["room_files"]))
        print("rooms length = ", str(len((self.game_data["room_files"]))))

    def load_items(self):
        item_dir = os.path.join(self.load_dir, "item_files")

        # find all item json files in dir
        # load items from file
        # append those items to list: items_loaded
        for item_json in os.listdir(item_dir):
            if item_json.endswith(".json"):
                try:
                    loaded_items = load_items_from_file(
                        os.path.join(item_dir, item_json)
                    )
                    self.game_data["item_files"] = loaded_items
                except marshmallow.exceptions.ValidationError as e:
                    print("Validation Error with: " + str(item_json) + str(e))

        print("items -> ",str(self.game_data["item_files"]))
        print("items length = ", str(len((self.game_data["item_files"]))))

    def load_scroll(self):
        scroll_file_path = os.path.join(
            self.load_dir,
            r"scroll/scroll.txt"
        )

        with open(scroll_file_path, mode="r") as file:
            self.scroll = file.readlines()
            self.scroll = [x.strip() for x in self.scroll]
            self.scroll.append("")

        print('scroll loaded:')
        print('-----------------------')
        for x in self.scroll:
            print(x)
        print('-----------------------')

    def load_player_data(self):
        player_data_path = os.path.join(self.load_dir, r"player")

        # get inventory items
        with open(
                os.path.join(player_data_path, "inventory.txt"),
                mode="r"
        ) as file:
            data = file.readlines()
            data = [x.strip() for x in data]
            self.game_data["player"]["inventory"] = data
            file.close()

        # get player_location
        with open(
            os.path.join(player_data_path, "player_location.txt"),
            mode="r"
        ) as file:
            data = file.readline()
            self.game_data["player"]["player_location"] = data
            file.close()


class initGameTest(unittest.TestCase):

    @staticmethod
    def test_save():
        start_new_game()
        test_scroll = Scroll(test=1)
        SaveGame("Connor_LaCour", test_scroll).save_data()
        print("something")
        f = SaveGame("Connor_LaCour", test_scroll).save_data()

    @staticmethod
    def test_load():
        f = LoadGame("Connor_LaCour")
        print("hi")



if __name__ == '__main__':
    unittest.main()
