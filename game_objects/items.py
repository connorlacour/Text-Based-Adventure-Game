from typing import Optional, List, Dict

from game_objects.event import Event
from game_objects.game_util import print_warning

class Item:

    def __init__(self, name, display_name, description, events: Dict[str, Event] = {}, article="the"):
        self.name: str = name  # reference name
        self.article: str = article  # reference name

        self.display_name: str = display_name  # name shown to players
        self.description: str = description  # look discription
        self.can_take: bool = True
        self.discarded = False
        self.vowels = ['a', 'i', 'o', 'u', 'e']
        self.events: Dict[str, Event] = events

        for e in self.events.keys():
            self.events[e].set_verb_and_synonyms(e)

    def get_article(self) -> str:
        if self.display_name[0] in self.vowels:
            return "an"
        else:
            return "a"

    def do_event(self, verb, room = None) -> str:
        from game_objects.global_collections import player_location
        narration = ""
        event = self.events.get(verb)
        if room is None: room = player_location.room
        if event is not None:
            if not event.repeatable:
                narration = event.do_event(room, verb, self.display_name)
                del self.events[verb]
                room.update_item_event_mapping_cache()
            else:
                narration = event.do_event(room, verb, self.display_name)

        else:
            print_warning(f"Couldn't find {verb} in {self}")
        return narration


    def __str__(self):
        return self.name

class InventoryItem(Item):

    def __init__(self, name, display_name, description, events={}, article="the", can_take=True):
        super().__init__(name, display_name, description, events, article)
        self.can_take = can_take
        self.discarded = False

    def discard(self) -> Item:
        self.discarded = True
        return self


# Item that cannot be taken from the room
class SceneryItem(Item):

    def __init__(self, name, display_name, description, events={}, article="the"):
        super().__init__(name, display_name, description, events, article)
        self.can_take = False


# Item where if it is picked up, it isn't removed from the room
# Up to max_count items can be taken by the user, resulting in a new item being created
class CollectiveItem(Item):
    takenCount: int = 0

    def __init__(self,
                 name: str,
                 display_name: str,
                 description: str,
                 singular_display_name: str,  # New look discription for created singular objects
                 singular_description: str,  # New look discription for created singular objects
                 max_count: int = 5,
                 events: Dict[str, Event]={},
                 article="the"):  # max number of items that can be created from collective

        super().__init__(name, display_name, description, events, article)
        self.singular_display_name = singular_display_name
        self.singular_description = singular_description
        self.max_count = max_count

    # create a new item with the name: {self.name_#created}
    def new_singular_item(self) -> Optional[InventoryItem]:
        if self.takenCount < self.max_count:
            self.takenCount += 1
            return InventoryItem(f"{self.name}_{str(self.takenCount)}", self.singular_display_name,
                                 self.singular_description)




