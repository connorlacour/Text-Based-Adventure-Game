# Found dictionary library at https://pypi.org/project/PyDictionary/
# Run pip install PyDictionary
# Can be used for determining whether the word is a verb or noun and for finding synonyms
from PyDictionary import PyDictionary

dict = PyDictionary()

# Set up defined directions, determiners, and prepositions
dirs = ["NORTH", "SOUTH", "EAST", "WEST"]

det = ["A", "AN", "ANY", "EVERY", "FEW", "HER", "ITS", "HIS", "LITTLE", "MANY", "MORE", "MY", "OUR", 
    "SOME", "THAT", "THE", "THEIR", "THESE", "THIS", "THOSE", "YOUR"]

preps = ['ABOARD', 'ABOUT', 'ABOVE', 'ACROSS', 'AFTER', 'AGAINST', 'ALONG', 'AMID', 'AMONG', 'AROUND', 'AS', 'AT',
    'BEFORE', 'BEHIND', 'BELOW', 'BENEATH', 'BESIDE', 'BETWEEN', 'BEYOND', 'BUT', 'BY', 'CONCERNING', 'CONSIDERING', 'DESPITE',
    'DOWN', 'DURING', 'EXCEPT', 'FOLLOWING', 'FOR', 'FROM', 'IN', 'INSIDE', 'INTO', 'LIKE', 'MINUS', 'NEAR', 'NEXT', 'OF', 'OFF',
    'ON', 'ONTO', 'OPPOSITE', 'OUT', 'OUTSIDE', 'OVER', 'PAST', 'PER', 'PLUS', 'REGARDING', 'ROUND', 'SAVE', 'SINCE', 'THAN',
    'THROUGH', 'TIL', 'TILL', 'TO', 'TOWARD', 'UNDER', 'UNDERNEATH', 'UNLIKE', 'UNTIL', 'UP', 'UPON', 'VERSUS', 'VIA', 'WITH',
    'WITHIN', 'WITHOUT']


def parse_entry(usr_cmd: str) -> dict:
    """
    Processing function for counting words in user entered string,
    and isolating verbs, directions, and objects
    
    params: usr_cmd = user entered text
    returns:
        cmds = dictionary with verb, dir, a_obj, and p_obj if there are any
    """
    # Initialize return variables
    cmds = {}

    # Separate words in command for parsing
    wrd_lst = usr_cmd.split()
    count = len(wrd_lst)
    idx = 0
    after_prep = False

#    print(wrd_lst)
    for x in range(count):
#        print(x)
#        print(wrd_lst[x])
        temp = dict.meaning(wrd_lst[x], disable_errors=True)
#        print(temp)
        # Save directional words first
        if wrd_lst[x].upper() in dirs:
            cmds["dir"] = wrd_lst[x].upper()
            continue
        elif wrd_lst[x].upper() in preps:
            after_prep = True
            continue
        elif temp != None:
            # Save verb
            if "Verb" in temp and "verb" not in cmds:
                cmds["verb"] = wrd_lst[x].upper()
                continue
            elif "Noun" in temp:
                if after_prep:
                    cmds["p_obj"] = wrd_lst[x].upper()
                    after_prep = False
                else:
                    cmds["a_obj"] = wrd_lst[x].upper()
                continue
    return cmds
