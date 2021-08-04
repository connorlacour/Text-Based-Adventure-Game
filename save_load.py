from game_objects.global_collections import *
from game_objects.object_schemas import *
from unit_tests.item_setup_tests import *
from gui.text_scroll import Scroll
import os
import json
from marshmallow import Schema, fields, post_load, post_dump
from marshmallow.fields import Int, Str, Bool
from marshmallow_oneofschema import OneOfSchema

from default_items.item_files import dining_room_scenery
from default_items.room_files.bathroom import *


# class Save:
#     def __init__(self, save_name: str, game_state: dict = {}, testing=False):
#         self.save_name = save_name
#         self.home_dir = os.getcwd()
#         if testing:
#             self.rooms = self.generate_room()
#             self.items = self.generate_items()
#             self.game_state = {
#                 "rooms": self.rooms,
#                 "items": self.items
#             }
#         else:
#             self.game_state = game_state
#
#         self.save_game()
#
#     def save_game(self):
#         # nav to saves dir
#         try:
#             os.chdir(r".\saves")
#             print(os.getcwd())
#         except FileNotFoundError:
#             print('Internal Error')
#
#         sub_dirs = ["item_files", "room_files"]
#
#         if self.save_name not in os.scandir():
#             os.mkdir(self.save_name)
#             os.chdir(self.save_name)
#             for sub_dir in sub_dirs:
#                 os.mkdir(sub_dir)
#             print('back home')
#             os.chdir(self.home_dir)
#             print(os.getcwd())
#         else:
#             os.chdir(self.save_name)
#             os.chdir("..")
#
#         # save_file = open(self.save_name, "w")
#         # save_file.write(json.dumps(self.game_state))
#         # save_file.close()
#         # os.chdir("..")
#
#     @staticmethod
#     def generate_room() -> List[str]:
#         test = ItemSetupTests()
#         room_file = test.testRoomSerialization()
#         room_files = [room_file]
#         return room_files
#
#     @staticmethod
#     def generate_items() -> List[str]:
#         test = ItemSetupTests()
#         item_file = test.testItemSerialization()
#         item_files = [item_file]
#         return item_files
#
#
# class Load:
#     def __init__(self, open_file_name: str):
#         self.open_file_name = open_file_name
#         self.game_state = self.load_game_state()
#
#     def load_game_state(self) -> dict:
#         # nav to saves dir
#         try:
#             os.chdir(r".\saves")
#             print(os.getcwd())
#         except FileNotFoundError:
#             print('Internal Error')
#
#         load_file = open(self.open_file_name, "r")
#         game_state = json.loads(load_file.read())
#         os.chdir("..")
#
#         # print("LOAD READ: ")
#         # print(game_state)
#         return game_state


class Save:
    def __init__(self, save_name: str, cur_scroll: Scroll):
        self.classes = {
            "room_files": [],
            "item_files": [],
            "text_scroll": [],
            "player": []}
        self.save_name = save_name
        self.home_dir = os.getcwd()
        self.scroll = cur_scroll

    def set_scroll(self):
        self.classes["text_scroll"] = self.scroll.text_in_scroll

    def get_json_file_list(self):
        x = self.home_dir
        room_dir = r".\default_items\room_files"
        item_dir = r".\default_items\item_files"

        jsons_to_load = {"rooms": [], "items": []}

        for room_json in os.listdir(room_dir):
            if room_json.endswith(".json"):
                jsons_to_load["rooms"].append(room_json)

        for item_json in os.listdir(item_dir):
            if item_json.endswith(".json"):
                jsons_to_load["items"].append(item_json)

        rooms_loaded = []
        for room in jsons_to_load["rooms"]:
            path = os.path.join(room_dir, room)
            y = load_rooms_from_file(path)
            rooms_loaded.append(y)

        self.classes["room_files"] = rooms_loaded

    def save_rooms(self):
        self.get_json_file_list()
        self.set_scroll()
        schema = RoomSchema()

        # nav to saves dir
        try:
            os.chdir(r".\saves")
            print(os.getcwd())
        except FileNotFoundError:
            print('Internal Error')

        if self.save_name not in os.listdir():
            os.mkdir(self.save_name)
        os.chdir(self.save_name)

        for sub_dir in self.classes.keys():

            if sub_dir not in os.listdir():
                os.mkdir(sub_dir)
            os.chdir(sub_dir)

            if sub_dir == "text_scroll":
                path = open("scroll.txt", mode="w+")
                for line in self.classes["text_scroll"]:
                    path.writelines(str(line) + "\n")
                path.close()

            else:
                for element in self.classes[sub_dir]:
                    dumped = schema.dumps(element, many=True)
                    path = open(str(element[0]) + ".json", mode="w+")
                    path.write(dumped)
                    path.close()
            os.chdir("..")
        os.chdir(self.home_dir)


test_scroll = Scroll(test=1)
Save("connor2", test_scroll).save_rooms()

