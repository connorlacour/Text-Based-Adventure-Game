


go_synonyms = {
    "GO", "WALK", "RUN", "CRAWL", "TRAVEL"
}

look_synonyms = {
    "LOOK", "CHECK", "CHECK OUT", "EXAMINE"
}

take_synonyms = {
    "TAKE", "GRAB", "PICK UP"
}

drop_synonyms = {
    "DROP", "PUT DOWN", "PLACE DOWN", "DISCARD", "CHUCK", "THROW OUT", "THROW AWAY"
}


synonym_dict = {
    "GO": list(go_synonyms),
    "LOOK": list(look_synonyms),
    "DROP": list(drop_synonyms),
    "WASH": ["SCRUB", "CLEAN"],
    "COMBINE": ["USE", "SMASH TOGETHER", "PUT IN"],
    "PLACE": ["PUT DOWN", "PUT ON"],
    "BARF": ["THROW UP", "WRETCH", "SPILL GUTS", "VOMIT"]
}
