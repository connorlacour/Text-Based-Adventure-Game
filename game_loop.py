from global_collections import *
from parse_cmd import *
from typing import Dict, Optional

class GameLoop:

    def __init__(self):

        self.player_position = rooms["dining_room"]


    def getNextNarration(self, user_text) -> str:
        word_dict = parse_entry(user_text)

