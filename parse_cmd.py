# Found dictionary library at https://pypi.org/project/PyDictionary/
# Run pip install PyDictionary
# Can be used for determining whether the word is a verb or noun and for finding synonyms
from typing import Dict, Optional
from PyDictionary import PyDictionary
from game_objects.global_collections import *

pydict = PyDictionary()

# Set up defined directions, determiners, and prepositions
directions = {"NORTH", "SOUTH", "EAST", "WEST"}

det = {"A", "AN", "ANY", "EVERY", "FEW", "HER", "ITS", "HIS", "LITTLE", "MANY", "MORE", "MY", "OUR",
    "SOME", "THAT", "THE", "THEIR", "THESE", "THIS", "THOSE", "YOUR"}

prepositions = {'ABOARD', 'ABOUT', 'ABOVE', 'ACROSS', 'AFTER', 'AGAINST', 'ALONG', 'AMID', 'AMONG', 'AROUND', 'AS', 'AT',
    'BEFORE', 'BEHIND', 'BELOW', 'BENEATH', 'BESIDE', 'BETWEEN', 'BEYOND', 'BUT', 'BY', 'CONCERNING', 'CONSIDERING', 'DESPITE',
    'DOWN', 'DURING', 'EXCEPT', 'FOLLOWING', 'FOR', 'FROM', 'IN', 'INSIDE', 'INTO', 'LIKE', 'MINUS', 'NEAR', 'NEXT', 'OF', 'OFF',
    'ON', 'ONTO', 'OPPOSITE', 'OUT', 'OUTSIDE', 'OVER', 'PAST', 'PER', 'PLUS', 'REGARDING', 'ROUND', 'SAVE', 'SINCE', 'THAN',
    'THROUGH', 'TIL', 'TILL', 'TO', 'TOWARD', 'UNDER', 'UNDERNEATH', 'UNLIKE', 'UNTIL', 'UP', 'UPON', 'VERSUS', 'VIA', 'WITH',
    'WITHIN', 'WITHOUT'}

actions = {'GO',
           'LOOK',
           'DROP',
           'GRAB',
           "PICK UP",
           "PUT DOWN"}


def setup_parser():
    #Add all exisiting directions to dirs
    for room in rooms.values():
        for direction in room.connecting_rooms.keys():
            directions.add(direction.upper())



def parse_entry(usr_cmd: str) -> (str, str, str ,str):
    import time
    """
    Processing function for counting words in user entered string,
    and isolating verbs, directions, and objects
    
    params: usr_cmd = user entered text
    returns:
        cmds = dictionary with verb, dir, a_obj, and p_obj if there are any
    """
    # Initialize return variables
    # Separate words in command for parsing
    word_list = usr_cmd.upper().split()
    after_preposition = False
    after_verb = False

    verb, direction, passive_obj, active_object = "", "", "", ""
    for word in word_list:
        start_time = time.time()
        word_type = pydict.meaning(word, disable_errors=True)
        print("meaning call: --- %s seconds ---" % (time.time() - start_time))

        # Save directional words first
        if after_verb:
            after_verb = False
            composite_verb = verb + " " + word
            if composite_verb in actions:
                verb = composite_verb
                continue

        if word in directions:
            direction = word
        elif word in prepositions:
            after_preposition = True
        elif word_type is not None:
            # Save verb
            if "Verb" in word_type and verb == "":
                verb = word
                after_verb = True

            elif "Noun" in word_type:
                if after_preposition:
                    passive_obj = word
                    after_preposition = False
                else:
                    if active_object == "":
                        active_object = word
                    elif passive_obj == "": #If active already specified second becomes passive by defualt
                        passive_obj = word
                continue

    if passive_obj == "" and active_object != "":
        passive_obj = active_object

    return verb, direction, passive_obj, active_object


# WILL NEED TO LINK TO ACTIONS FOR CHECKING
def act_exists(player_action: str) -> Optional[str]:
    """
    Takes an action and determines if it is an existing action within the gameplay.
    Searches word for synonyms that might be used for action as well.

    params: action = verb obtained from user command
    returns: String with game action if exists; otherwise, returns False
    """
    synonyms = [x.upper() for x in pydict.synonym(player_action)]

    # TEMP ACTION TESTING
    actions = ['EAT', 'DROP', 'UNLOCK', 'PERSUADE', 'COMBINE', 'JUMP', 'FIGHT', 'CHOOSE', 'PRESS', 'GIVE', 'LOOK', 'GO', 'TAKE', 'HELP']

    for actor in actions:
        if actor == player_action.upper():
            return actor

    for synonym in synonyms:
        if synonym in actions:
            return synonym

    return None
