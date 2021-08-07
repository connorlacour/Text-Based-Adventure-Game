from game_objects.event import Event
from typing import Dict

events: Dict[str, Event] = {
    "HUM": Event(["print You HUM a jaunty little tune"]),
    "JUMP": Event(["print You JUMP up and down like a clown"])
}

for e in events.keys():
    events[e].set_verb_and_synonyms(e)