def razz_ai_loose_aggressive(hero,villain,villain_actions):
    # AI will be very aggro, raise pots on scare cards and protect value hands
    # Output a decision tree flattened into an array for play on each street
    # B = bet, F = fold, C = call, b = bringin, c = check, R = raise
    # RRR = raise to cap


    actions = []

    hero_start = [hero[0],hero[1],hero[2]]

    hero_up = hero[2]
    villain_up = villain[2]

    premiums = [["A","2","3","4","5"],["A","2","3","4","6"],["A","2","3","5","6"],
                ["A","2","4","5","6"],["A","3","4","5","6"],["2","3","4","5","6"]]

    # 3rd Street
    # Rule 1: If hero has three cards below a 8, raise till cap 
    if all(values.index(x[0]) < 8 for x in hero_start):
        actions.append([3,"RRR"])

    # Rule 2: If hero has lower up card than villain and villain card is T or higher, raise/call
    elif values.index(hero_up[0]) < values.index(villain_up[0]) and values.index(villain_up[0]) >= 9:
        actions.append([3,"RC"])

    # Rule 3: If hero has higher up card than villain, bringin/fold
    elif values.index(hero_up[0]) > values.index(villain_up[0]):
        actions.append([3,"bF"])

    # Rule 4: If hero has a pair, fold
    elif len(list(set[values.index(x[0]) for x in hero_start])) < 3:
        actions.append([3,"F"])

    # 4th Street
    # Rule 5: If hero has 3 cards lower than an 8, check call
    if len([values.index(x[0]) < 8 for x in hero[:4]]) == 3:
        actions.append([4,"cC"])

    # Rule 6: If hero has 4 cards lower than an 8, raise to cap
    elif all(values.index(x[0]) < 8 for x in hero[:4]):
        actions.append([4,"RRR"])

    # Rule 7: If hero has an open pair, fold
    elif hero[3][0] == hero[4][0]:
        actions.append([4,"cF"])

    return actions
