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
