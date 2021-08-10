
from typing import List


go_synonyms = {
    "GO", "WALK", "RUN", "CRAWL", "TRAVEL"
}

look_synonyms = {
    "LOOK", "CHECK", "CHECK OUT", "EXAMINE", "INSPECT"
}

take_synonyms = {
    "TAKE", "GRAB", "PICK UP", "CARRY"
}

drop_synonyms = {
    "DROP", "PUT DOWN", "PLACE DOWN", "DISCARD", "CHUCK", "THROW OUT", "THROW AWAY", "THROW"
}

wear_synonyms = {
    "PUT ON", "EQUIP"
}

press_synonyms = {
     "TOUCH", "MASH"
}

fight_synonyms = {
     "FIGHT WITH", "ATTACK", "BATTLE", "CHALLENGE", "RESIST", "BRAWL", "DUEL", "FEUD", "QUARREL", "SPAR", "STRUGGLE", "WRESTLE", "BOX", "PUNCH"
}

eat_synonyms = {
    "BITE", "CHEW", "CONSUME", "DEVOUR", "DINE", "GOBBLE", "NIBBLE", "GRAZE", "MUNCH", "SCARF", "SNACK"
}

turn_on_synonyms = {
    "ACTIVATE", "SWITCH ON", "START UP", "START"
}

swallow_synonyms = {
    "CONSUME", "GULP", "IMBIBE", "INGEST", "EAT", "DRINK"
}

unlock_synonyms = {
    "UNLOCK WITH", "OPEN WITH", "USE"
}

use_synonyms = {
    "APPLY", "EMPLOY", "OPERATE", "UTILIZE", "WIELD", "SWING"
}

bribe_synonyms = {
    "BUY OFF", "ENTICE", "PAY OFF", "TEMPT", "GIVE"
}

persuade_synonyms = {
    "COAX", "SWAY", "TALK INTO", "URGE", "WIN OVER", "GIVE", "SHOW"
}

enter_code_synonyms = {
    "ENTER CODE", "INSERT", "PUT IN", "ENTER", "ENTER CODE 9338", "ENTER CODE YEET", "ENTER 8338", "ENTER YEET"
}

feed_synonyms = {
    "NOURISH", "PROVIDE", "SATISFY", "STUFF", "SUPPLY", "HAND", "GIVE"
}

open_synonyms = {
    "CRACK", "CRACK OPEN", "UNLATCH" "UNFASTEN", 
}

pick_up_synonyms = {
    "PULL", "LIFT", "RAISE", "READ"
}

synonym_dict = {
    "GO": list(go_synonyms),
    "LOOK": list(look_synonyms),
    "DROP": list(drop_synonyms),
    "BRIBE": list(bribe_synonyms),
    "EAT": list(eat_synonyms),
    "ENTER YEET": list(enter_code_synonyms),
    "ENTER 9338": list(enter_code_synonyms),
    "INSERT": list(enter_code_synonyms),
    "INSERT 9338": list(enter_code_synonyms),
    "INSERT YEET": list(enter_code_synonyms),
    "FEED": list(feed_synonyms),
    "FIGHT": list(fight_synonyms),
    "OPEN": list(open_synonyms),
    "PERSUADE": list(persuade_synonyms),
    "PICK UP": list(pick_up_synonyms),
    "PRESS": list(press_synonyms),
    "SWALLOW": list(swallow_synonyms),
    "TURN ON": list(turn_on_synonyms),
    "UNLOCK": list(unlock_synonyms),
    "USE": list(use_synonyms),
    "WEAR": list(wear_synonyms),
    "ADMIRE": ["BEHOLD", "APPRECIATE"],
    "SIT": ["SIT DOWN"],
    "READ": ["FLIP THROUGH"],
    "TURN OFF": ["SWITCH OFF"],
    "CLOSE": ["SHUT"],
    "TALK": ["TALK TO", "GREET", "WAVE TO", "PLEAD WITH", "BEG", "ANNOY", "YELL", "SMILE", "GLARE", "FROWN", "RUN AWAY"],
    "KISS": ["SMOOCH", "HUG", "SNIFF", "FLATTER"],
    "WORK OUT": ["EXERCISE", "FLEX", "DANCE"],
    "ADMIRE SELF": ["CHECK YOURSELF"],
    "COOK": ["MICROWAVE", "PUT", "ZAP"],
    "TAKE OFF": ["REMOVE"],
    "LIE DOWN": ["LIE ON", "LAY", "COLLAPSE", "NAP", "SLEEP"]

}
