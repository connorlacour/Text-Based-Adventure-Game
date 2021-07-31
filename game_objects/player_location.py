from __future__ import annotations  # Enables forward type hints
from typing import Optional

from game_objects.room import Room


class PlayerLocation:
    def __init__(self):
        self.room: Optional[Room] = None

    def set(self, location: Room):
        self.room = location

    def __str__(self):
        return str(self.room)

# Data object to bundle an item name and item narration together allowing us to more
#   intuitively initialize room descriptions

# Data object to facilitate the user being able to move around with both
#       Directions: Go DOWN
#       Item: Take STAIRS
