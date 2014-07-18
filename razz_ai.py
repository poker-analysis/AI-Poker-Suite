from random import randrange

# Global Variables
suits = ["s","h","d","c"]
lo_values = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]
deck = [value+suit for suit in suits for value in lo_values]

def ai_third_street(hero, villain_up, villain_action):

    hero_start = [hero[0],hero[1],hero[2]]
    hero_up = hero[2]

    # Rule 1: If hero has three cards below a 8, raise till cap 
    if all(lo_values.index(x[0]) < 8 for x in hero_start):
        return "BP"

    # Rule 2: If hero has lower up card than villain and villain card is T or higher, raise/call
    elif lo_values.index(hero_up[0]) < lo_values.index(villain_up[0]) and lo_values.index(villain_up[0]) >= 9:
        return "RC"

    # Rule 3: If hero has a pair, fold
    elif len(set([lo_values.index(x[0]) for x in hero_start])) < 3:
        return "cF"


def ai_fourth_street(hero,villain,villain_actions):
    # Decision = out of position | in position
    # B = bet, F = fold, C = call, b = bringin, c = check, R = raise
    # P = raise to cap

    actions = []

    hero_start = [hero[0],hero[1],hero[2]]

    hero_up = hero[2]
    villain_up = villain[2]

    # 4th Street
    # Rule 1: If hero has 3 cards lower than an 8, check call
    if len([lo_values.index(x[0]) < 8 for x in hero[:4]]) == 3:
        return "cC"

    # Rule 2: If hero has 4 cards lower than an 8, raise to cap
    elif all(lo_values.index(x[0]) < 8 for x in hero[:4]):
        return "P"

    # Rule 3: If hero has an open pair, fold
    elif hero[3][0] == hero[4][0]:
        return "cF"

    # Rule 4: If hero has 4 cards lower than a 9, bet call
    elif all(lo_values.index(x[0]) < 9 for x in hero[:4]):
        return "BC"

    # Rule 5: If hero has higher card than villain, check fold
    elif lo_values.index(hero[3]) > lo_values.index(villain[3]):
        return "cF"


def ai_fifth_street(hero,villain_up):

    # 5th Street
    # Rule 1: If hero has low hand lower than an 8, raise to cap
    if all(lo_values.index(x[0]) < 8 for x in hero[:4]):
        return "P"

    # Rule 2: Bet fold everything else (rule for testing)
    else:
        return "BF"


def ai_sixth_street(hero,villain_up):
    # 6th Street
    # Rule 1: Bet fold everything else (rule for testing)
    return "BF"


def ai_seventh_street(hero,villain_up):
    # 7th Street
    # Rule 2: Bet fold everything else (rule for testing)
    return "BF"

    return actions


def hu_razz():
    # Turns decision tree into game for user
    # $100/$200, ante: $15, bring in: $30, complete: $100
    # Every street should show stack size, both hands, pot size
    user_hand = []
    ai_hand = []  
    user_stack = 6000
    ai_stack = 6000
    user_action = ""
    ai_action = ""

    while len(user_hand) < 3:
        x = randrange(len(deck))
        user_hand.append(deck[x])
        deck.remove(deck[x])

    while len(ai_hand) < 3:
        x = randrange(len(deck))
        ai_hand.append(deck[x])
        deck.remove(deck[x])

    print "".join([x for x in user_hand])
    print " ".join([ai_hand[x] if x == 2 else "X" for x in xrange(3)])

    if lo_values.index(user_hand[2][0]) > lo_values.index(ai_hand[2][0]):
        user_action = raw_input("b for bring in $30, c for complete to $100: ")

    elif lo_values.index(user_hand[2][0]) < lo_values.index(ai_hand[2][0]):
        ai_action = ai_third_street(ai_hand,user_hand[2],None)
        print ai_action
    else:
        if user_hand[2][1]) > ai_hand[2][1]:
            user_action = raw_input("b for bring in $30, c for complete to $100: ")
        elif user_hand[2][1] < ai_hand[2][1]:
            ai_action = ai_third_street(ai_hand,user_hand[2],None) 
            print ai_action

    if user_action == "b":
        print "User brings in for $30."
    elif user_action == "c":
        print "User completes for $100."

    if ai_action == "": 
        print ai_third_street(ai_hand,user_hand[2],None)

hu_razz()
