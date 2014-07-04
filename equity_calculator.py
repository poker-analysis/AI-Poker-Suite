from itertools import combinations

suits = ["s","h","d","c"]
values = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]

def create_deck():
    deck = []
    for value in values: 
        for suit in suits:
            deck.append(value + suit)
    return deck 


def holdem_evaluator(total_board):
    # Need to rewrite optimized 7 card evaluator

    # Royal Flush
    royal_flushes = [["Ah","Kh","Jh","Th","Qh"] , ["Ac","Kc","Jc","Tc","Qc"] ,
    ["Ad","Kd","Jd","Td","Qd"], ["As","Ks","Js","Ts","Qs"]]

    for x in royal_flushes:
        if set.issubset(set(x),set(total_board)) == True:
            return "Royal Flush"

    # Straight Flush
    # Check if there are > five cards that have same suit, if there are, check 
    # among cards with same suit if there are 5 in a row

    # Quads
    # return [values.index(x[0]) for x in total_board], 4 of an item

    # Full House
    # return [values.index(x[0]) for x in total_board], 3 + 2

    # Flush
    for suit in suits:
        if "".join(total_board).count(suit) >= 5:
            return "Flush"

    # Straight
    # Trips
    # Two Pair
    # One Pair
    # High Card


def plo_evaluator(total_board):
    pass


def equity_simulator():
    game = raw_input("""
        Select a game type:
        1. Texas Hold Em
        2. Pot Limit Omaha
        3. Seven Card Stud\n""")

    if game == "1": 
        holdem_simulator()
    elif game == "2":
        omaha_simulator()
    elif game == "3":
        stud_simulator()


def holdem_simulator():
    user_hand = "" 
    cpu_hand = ""
    user_wins = 0
    cpu_wins = 0
    ties = 0

    while len(user_hand) < 4:
        user_hand = raw_input("Enter your hand: ")
    while len(cpu_hand) < 4:
        cpu_hand = raw_input("Enter the computer's hand: ")
    deck = create_deck()

    flop = raw_input("Enter a flop such as AhKh2s or enter if preflop all-in: ")
    if len(flop) == 6:
        turn = raw_input("Enter a turn such as 4c or hit enter if no turn: ")
    if len(turn) == 2:
        river = raw_input("Enter a river such as 4s or hit enter if no river: ")
    
    deck.remove(user_hand[:2]), deck.remove(user_hand[2:])
    deck.remove(cpu_hand[:2]), deck.remove(cpu_hand[2:])

    # Because the number of combinations is bounded at 1.7m, we can calculate it 
    # through brute force of all possible combinationss

print holdem_evaluator(["Ah","Kh","Th","Jh","Qs","Js","9s"])
