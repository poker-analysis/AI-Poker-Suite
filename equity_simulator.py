from itertools import combinations

suits = ["s","h","d","c"]
values = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]

def create_deck():
    deck = []
    for value in values: 
        for suit in suits:
            deck.append(value+suit)
    return deck 

def holdem_evaluator(total_board):
    pass

def plo_evaluator(total_board):
    pass

def stud_evaluator(total_board):
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

    deck.remove(user_hand[:2]), deck.remove(user_hand[2:])
    deck.remove(cpu_hand[:2]), deck.remove(cpu_hand[2:])

    # Because the number of combinations is bounded at 1.7m, we can calculate it 
    # through brute force of all possible combinationss

def omaha_simulator():
    pass

def stud_simulator():
    pass

equity_simulator()
