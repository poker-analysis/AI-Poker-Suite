from random import randrange

# Global Variables
suits = ["s","h","d","c"]
lo_values = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]
deck = [value+suit for suit in suits for value in lo_values]

def razz_ai_loose_aggressive(hero,villain,villain_actions):
    # Human heuristic AI: AI based on set of rules guided by human analysis
    # Output a decision tree flattened into an array for play on each street
    # Decision = out of position | in position
    # B = bet, F = fold, C = call, b = bringin, c = check, R = raise
    # P = raise to cap

    actions = []

    hero_start = [hero[0],hero[1],hero[2]]

    hero_up = hero[2]
    villain_up = villain[2]

    premiums = [["A","2","3","4","5"],["A","2","3","4","6"],["A","2","3","5","6"],
                ["A","2","4","5","6"],["A","3","4","5","6"],["2","3","4","5","6"]]

    # 3rd Street
    # Rule 1: If hero has three cards below a 8, raise till cap 
    if all(lo_values.index(x[0]) < 8 for x in hero_start):
        actions.append([3,"bP"])

    # Rule 2: If hero has lower up card than villain and villain card is T or higher, raise/call
    elif lo_values.index(hero_up[0]) < lo_values.index(villain_up[0]) and lo_values.index(villain_up[0]) >= 9:
        actions.append([3,"RC"])

    # Rule 3: If hero has higher up card than villain, bringin/fold
    elif lo_values.index(hero_up[0]) > lo_values.index(villain_up[0]):
        actions.append([3,"bF"])

    # Rule 4: If hero has a pair, fold
    elif len(list(set[lo_values.index(x[0]) for x in hero_start])) < 3:
        actions.append([3,"cF"])

    # 4th Street
    # Rule 5: If hero has 3 cards lower than an 8, check call
    if len([lo_values.index(x[0]) < 8 for x in hero[:4]]) == 3:
        actions.append([4,"cC"])

    # Rule 6: If hero has 4 cards lower than an 8, raise to cap
    elif all(lo_values.index(x[0]) < 8 for x in hero[:4]):
        actions.append([4,"P"])

    # Rule 7: If hero has an open pair, fold
    elif hero[3][0] == hero[4][0]:
        actions.append([4,"cF"])

    # Rule 8: If hero has 4 cards lower than a 9, bet call
    elif all(lo_values.index(x[0]) < 9 for x in hero[:4]):
        actions.append([4,"BC"])

    # Rule 9: If hero has higher card than villain, check fold
    elif lo_values.index(hero[3]) > lo_values.index(villain[3]):
        actions.append([4,"cF"])

    # 5th Street
    # Rule 10: If hero has low hand lower than an 8, raise to cap
    if all(lo_values.index(x[0]) < 8 for x in hero[:4]):
        actions.append([5,"P"])

    # Rule 11: Bet fold everything else (rule for testing)
    else:
        actions.append([5,"BF"])

    # 6th Street
    # Rule 12: Bet fold everything else (rule for testing)
    actions.append([6,"BF"])

    # 7th Street
    # Rule 13: Bet fold everything else (rule for testing)
    actions.append([7,"BF"])

    return actions

def hu_razz():
    # Turns decision tree into game for user
    # $100/$200, ante: $15, bring in: $30, complete: $100
