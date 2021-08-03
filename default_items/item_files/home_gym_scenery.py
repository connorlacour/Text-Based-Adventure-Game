from typing import Optional, List, Dict

from game_objects.item_event import *
from game_objects.items import *


class Shelf(SceneryItem):
    def __init__(self, description, events):
        super().__init__("shelf", "SHELF", description, events=events, article="a")


class Mirror(SceneryItem):
    def __init__(self, description, events):
        super().__init__("mirror", "MIRROR", description, events=events, article="a")


def initialize_home_gym_scenery(items: list = None):
    guard = None
    window = None
    night_stand = None

    if items is None:
        guard = Guard("The GUARD'S badge says 'Tuck'.", [{"fight": "You try to fight the guard, but you are no match for him.  He knocks you out, and when you wake, you find yourself in a jail cell.  GAME OVER."}, {"bribe": "Tuck raises his eyebrows at you curiously.  There’s a moment of silence between the two of you as he considers the offer.\n\n“I’m too old for this crap,” he mutters, swiping the pouch out of your hand and walking toward the door.  You listen as he stomps down the stairs before finally hearing the front door slam shut."}, {"persuade": "You remember the note from Carole you found.  It had been addressed to someone named Tuck.  Hoping it will help you out of the situation, you offer the note to the guard.  He narrows his gaze in suspicion at you as you fish out the paper and hand it over.  His eyes soften as he reads what’s written.\n\n“Where did you…” he starts to say.  He looks between you and the note several times before finally sighing.  “I quit.  Hell, I’m probably out of a job anyway after falling asleep here.  As far as I’m concerned, I never saw you.”\n\nWith that, he walks out of the room."}])
        window = Window("You stare out the WINDOW.")
        night_stand = Night_Stand("Opening the drawer to the NIGHT STAND, you see a GLOVE.")
    else:
        for x in range(len(items)):
            if items[x].guard:
                guard = Guard(items[x].guard.desc, items[x].guard.events)
            elif items[x].window:
                window = Window(items[x].window.desc, items[x].window.events)
            elif items[x].night_stand:
                night_stand = Night_Stand(items[x].night_stand.desc, items[x].night_stand.events)

    return guard, window, night_stand
