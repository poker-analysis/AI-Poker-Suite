def razz_ai_loose_aggressive(hero,villain,villain_actions):
    # AI will be very aggro, raise pots on scare cards and protect value hands
    # Output a decision tree flattened into an array for play on each street
    # List of actions
    # B = bet
    # F = fold
    # C = call
    # b = bringin
    # c = complete
    # R = raise
    # RRR = raise to cap

    actions = []

    hero_start = [hero[0],hero[1],hero[2]]

    hero_up = hero[2]
    villain_up = villain[2]

    # Rule 1: If hero has three cards below a 8, raise till cap 
    if all(values.index(x[0]) < 8 for x in hero_start):
        actions.append([0,"RRR"])

    return actions
