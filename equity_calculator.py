from itertools import combinations
from itertools import izip as zip,count
from collections import Counter
from random import randrange
import time 

# To Do: 
# Omaha Evaluator
# Omaha HU Calculator
# Omaha Multiway Calculator
# O8 Evaluator
# Stud8 Evaluator
# Rewrite HoldEm in C++
# Rewrite Razz in C++ 
# Rewrite Stud in C++

suits = ["s","h","d","c"]
values = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
lo_values = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]

def holdem_evaluator(total_board):
    # Useful Variables
    indices = set(sorted([values.index(card[0]) for card in total_board]))
    flush_suit = ""
    for suit in suits:
        if "".join(total_board).count(suit) >= 5:
            flush_suit = suit
    flush_indices = [values.index(card[0]) for card in total_board if card[1] == flush_suit]
    pairs = [[card[:-1] for card in total_board].count(x) for x in values]
    
    # Royal Flush
    royal_flushes = [["Ah","Kh","Jh","Th","Qh"] , ["Ac","Kc","Jc","Tc","Qc"] ,
    ["Ad","Kd","Jd","Td","Qd"], ["As","Ks","Js","Ts","Qs"]]

    for x in royal_flushes:
        if set.issubset(set(x),set(total_board)) is True:
            return "Royal Flush", 9, 0

    # Straight Flush
    for x in sorted(list(flush_indices))[::-1]:
        if flush_indices.count(x-1) and flush_indices.count(x-2) and \
        flush_indices.count(x-3) and flush_indices.count(x-4):
            return "Straight Flush", 8, x + 2
    if set.issubset(set([12,0,1,2,3]),flush_indices):
        return "Straight Flush", 8, 0

    # Quads
    if [x for x, y in Counter([card[:-1] for card in total_board]).items() if y == 4] != []:
        quad = [[],[]]
        for x in xrange(12,-1,-1):
            if pairs[x] == 4:
                quad[0].append(x+2)
            elif pairs[x] > 0:
                quad[1].append(x+2)
        return "Quads", 7, max(quad[0])*100+max(quad[1])

    # Full House
    if pairs.count(2) + pairs.count(3) >= 2 and pairs.count(3)>0:
        hand_values = [[],[]]
        for x in xrange(12,-1,-1):
            if pairs[x] == 3:
                if len(hand_values[0]) == 1:
                    hand_values[1].append(x+2)
                else:
                    hand_values[0].append(x+2)
            elif pairs[x] == 2:
                hand_values[1].append(x+2)
        return "Full House", 6, max(hand_values[0])*100 + max(hand_values[1])

    # Flush
    for suit in suits:
        if "".join(total_board).count(suit) >= 5:
            return "Flush",5,sorted(list(indices)[-5:])[::-1]

    # Straight
    for x in sorted(list(indices))[::-1]:
        if list(indices).count(x-1) and list(indices).count(x-2) and \
        list(indices).count(x-3) and list(indices).count(x-4):
            return "Straight",4,x+2
    if set.issubset(set([12,0,1,2,3]),indices):
        return "Straight", 4, 0

    # Trips
    if max(pairs) == 3:
        hand_values = [pairs.index(3)+2]
        for x in xrange(12,-1,-1):
            if len(hand_values) == 3:
                break
            if pairs[x] == 1:
                hand_values.append(x+2)
        return "Trips", 3, hand_values[0] * 10000 + hand_values[1] * 100 + \
        hand_values[2] * 1

    # Two Pair
    if pairs.count(2) >= 2:
        hand_values = [i+2 for i, j in zip(count(), pairs) if j == 2][::-1][:2]
        errored_vals = [values.index(card[0])+2 for card in total_board]
        for x in sorted(errored_vals)[::-1]:
            if len(hand_values) == 3:
                break
            if hand_values.count(x) == 1:
                pass
            else:
                hand_values.append(x)

        return "Two Pair", 2, hand_values[0] * 10000 + hand_values[1] * 100 + \
        hand_values[2] * 1

    # One Pair
    if pairs.count(2) == 1:
        hand_values = [pairs.index(2)+2]
        for x in xrange(12,-1,-1):
            if len(hand_values) == 4:
                break
            if pairs[x] == 1:
                hand_values.append(x+2)
        return "Pair", 1 , hand_values[0]*1000000 + hand_values[1]*10000 + \
        hand_values[2]*100 + hand_values[3]

    # High Card
    else: 
        return "High Card", 0, sorted([values.index(card[0]) for card in total_board])[-5:][::-1]


def razz_evaluator(hand1,hand2):

    h1 = sorted([lo_values.index(x[0]) for x in hand1])
    h2 = sorted([lo_values.index(x[0]) for x in hand2])

    h1_lo = sorted(set([lo_values.index(x[0]) for x in hand1]))
    h2_lo = sorted(set([lo_values.index(x[0]) for x in hand2]))

    h1_diff = list((Counter(h1)-Counter(h1_lo)).elements())
    h2_diff = list((Counter(h2)-Counter(h2_lo)).elements())

    h1_strength = 0
    h2_strength = 0

    while len(h1_lo) < 5:
        for x in h1_diff:
            if h1_lo.count(x) <= h1_strength and len(h1_lo) < 5:
                h1_lo.append(x)
                h1_diff.remove(x)
        h1_strength+=1

    while len(h2_lo) < 5:
        for x in h2_diff:
            if h2_lo.count(x) <= h2_strength and len(h2_lo) < 5:
                h2_lo.append(x)
                h2_diff.remove(x)
        h2_strength+=1

    h1_indices = [h1_lo.count(x) for x in range(13)] 
    h2_indices = [h2_lo.count(x) for x in range(13)]

    h1_lo = sorted(h1_lo)[::-1][-5:]
    h2_lo = sorted(h2_lo)[::-1][-5:]

    if h1_lo == h2_lo:
        return "Tie"

    elif sorted(list(set(h1_lo))) == sorted(h1_lo) and sorted(list(set(h2_lo))) == sorted(h2_lo):
        return h1_lo < h2_lo

    elif h1_indices.count(3) != h2_indices.count(3):
        return h1_indices.count(3) < h2_indices.count(3)

    elif h1_indices.count(2) != h2_indices.count(2):
        return h1_indices.count(2) < h2_indices.count(2)

    elif h1_indices.count(3) == h2_indices.count(3) == 1:
        if h1_indices.index(3) != h2_indices.index(3):
            return h1_indices.index(3) < h2_indices.index(3)
        else:
            return h2_indices.index(2) < h2_indices.index(2)

    elif h1_indices.count(2) == h2_indices.count(2) == 1:
        if h1_indices.index(2) != h2_indices.index(2):
            return h1_indices.index(2) < h2_indices.index(2)
        else:
            return [x for x in h1_indices if h1_indices.index(x)==1] < \
            [x for x in h2_indices if h2_indices.index(x)==1]

    elif h1_indices.count(2) == h2_indices.count(2) == 2:
        return h1_lo < h2_lo

    else:
        return "Tie"


def omaha_evaluator(hand,board):
    # Brute force omaha evaluator for testing (hand,board = arrays)
    start = time.time()
    max_rank = -1
    answer = "     "
    boards = list(combinations(board,3))
    hands = list(combinations(hand,2))
    for a in boards:
        for b in hands:
            if holdem_evaluator(a+b)[1] > max_rank:
                max_rank = holdem_evaluator(a+b)[1]
                answer = holdem_evaluator(a+b)
            elif holdem_evaluator(a+b)[1] == max_rank:
                if holdem_evaluator(a+b)[2] > answer[2]:
                    max_rank = holdem_evaluator(a+b)[1]
                    answer = holdem_evaluator(a+b)
    elapsed = time.time() - start 
    return answer


def o8_evaluator(hand,board):
    pass


def omaha_headsup_flop_equity_calculator(hero,villain,board):
    user_wins = 0
    cpu_wins = 0
    ties = 0
    
    deck = [value+suit for suit in suits for value in values]

    for card in hero:
        deck.remove(card)
    for card in villain:
        deck.remove(card)
    for card in board:
        deck.remove(card)
    
    combos = list(combinations(deck,5 - len(board)))
    for x in combos:
        draws = list(x)
        if omaha_evaluator(hero,board+draws)[1] > omaha_evaluator(villain,board+draws)[1]:
            user_wins += 1
        elif omaha_evaluator(hero,board+draws)[1] < omaha_evaluator(villain,board+draws)[1]:
            cpu_wins += 1
        else:
            if omaha_evaluator(hero,board+draws)[2] > omaha_evaluator(villain,board+draws)[2]:
                user_wins += 1
            elif omaha_evaluator(hero,board+draws)[2] < omaha_evaluator(villain,board+draws)[2]:
                cpu_wins += 1
            else:
                ties+=1

    hand1_equity = ((user_wins+ties/2.0)/(user_wins+ties+cpu_wins))
    hand2_equity = ((cpu_wins+ties/2.0)/(user_wins+ties+cpu_wins))
    return hero,hand1_equity,villain,hand2_equity,user_wins,cpu_wins,ties 


def plo_multiway_equity_calculator(hero,villain,villain2):
    pass


def deuce_to_seven_evaluator(hand1,hand2):
    if holdem_evaluator(hand1)[1] > holdem_evaluator(hand2)[1]:
        return False
    elif holdem_evaluator(hand1)[1] < holdem_evaluator(hand2)[1]:
        return True
    else:
        if holdem_evaluator(hand1)[2] > holdem_evaluator(hand2)[2]:
            return False
        elif holdem_evaluator(hand1)[2] < holdem_evaluator(hand2)[2]:
            return True
        else:
            return Tie


def holdem_preflop_equity_calculator(hand1,hand2):
    
    start = time.time()

    user_wins = 0
    cpu_wins = 0
    ties = 0
    
    deck = [value+suit for suit in suits for value in values]
    deck.remove(hand1[:2]), deck.remove(hand1[2:])
    deck.remove(hand2[:2]), deck.remove(hand2[2:])

    user_hand = [hand1[:2],hand1[2:]]
    cpu_hand = [hand2[:2],hand2[2:]]

    combos = list(combinations(deck,5))
    for x in xrange(0,len(combos),100):
        x = list(combos[x])
        if holdem_evaluator(x + user_hand)[1] > holdem_evaluator(x + cpu_hand)[1]:
            user_wins += 1
        elif holdem_evaluator(x + user_hand)[1] < holdem_evaluator(x + cpu_hand)[1]:
            cpu_wins += 1
        else:
            if holdem_evaluator(x+user_hand)[2] > holdem_evaluator(x+cpu_hand)[2]:
                user_wins += 1
            elif holdem_evaluator(x+cpu_hand)[2] < holdem_evaluator(x+user_hand)[2]:
                cpu_wins += 1
            else:
                ties+=1
    
    hand1_equity = ((user_wins+ties/2.0)/(user_wins+ties+cpu_wins))
    hand2_equity = ((cpu_wins+ties/2.0)/(user_wins+ties+cpu_wins))
    return hand1,hand1_equity,hand2,hand2_equity


def holdem_postflop_equity_calculator(board,hand1,hand2):
    # Because the number of computations is bounded at 990 hands, we can search
    # exhaustively through all possible outcomes to calculate equity. 
    start = time.time()

    user_wins = 0
    cpu_wins = 0
    ties = 0

    user_hand = [hand1[:2],hand1[2:]]
    cpu_hand = [hand2[:2],hand2[2:]]
    
    deck = [value+suit for suit in suits for value in values]
    for x in xrange(0,len(board),2):
        if x+2 > len(board) - 1:
            deck.remove(board[x:])
            user_hand.append(board[x:])
            cpu_hand.append(board[x:])
        else:
            deck.remove(board[x:x+2])
            user_hand.append(board[x:x+2])
            cpu_hand.append(board[x:x+2])

    deck.remove(hand1[:2]), deck.remove(hand1[2:])
    deck.remove(hand2[:2]), deck.remove(hand2[2:])
    
    combos = list(combinations(deck,7 - len(user_hand)))
    for x in combos:
        x = list(x)
        if holdem_evaluator(x + user_hand)[1] > holdem_evaluator(x + cpu_hand)[1]:
            user_wins += 1
        elif holdem_evaluator(x + user_hand)[1] < holdem_evaluator(x + cpu_hand)[1]:
            cpu_wins += 1
        else:
            if holdem_evaluator(x+user_hand)[2] > holdem_evaluator(x+cpu_hand)[2]:
                user_wins += 1
            elif holdem_evaluator(x+user_hand)[2] < holdem_evaluator(x+cpu_hand)[2]:
                cpu_wins += 1
            else:
                ties+=1

    hand1_equity = ((user_wins+ties/2.0)/(user_wins+ties+cpu_wins))
    hand2_equity = ((cpu_wins+ties/2.0)/(user_wins+ties+cpu_wins))
    return hand1,hand1_equity,hand2,hand2_equity,user_wins,cpu_wins,ties
 

def razz_equity_calculator(query):

    query = query.split()

    deck = [value+suit for suit in suits for value in values]
    hand1 = [x for x in query[0] if x != "*"]
    hand2 = [x for x in query[2] if x != "*"]
    
    user_wins = 0
    cpu_wins = 0
    ties = 0

    user_hand = ["".join(x) for x in zip(\
                    [x for x in hand1 if hand1.index(x) % 2 == 0],\
                    [x for x in hand1 if hand1.index(x) % 2 == 1])
                ]

    cpu_hand = ["".join(x) for x in zip(\
                    [x for x in hand2 if hand2.index(x) % 2 == 0],\
                    [x for x in hand2 if hand2.index(x) % 2 == 1])
               ]
    
    for x in user_hand:
        deck.remove(x)

    for x in cpu_hand:
        deck.remove(x)

    start = time.time()
    while user_wins + cpu_wins + ties < 5000:

        added_cards = []

        while len(user_hand) < 7:
            x = randrange(len(deck))
            user_hand.append(deck[x])
            added_cards.append(deck[x])
            deck.remove(deck[x])

        while len(cpu_hand) < 7:
            x = randrange(len(deck))
            cpu_hand.append(deck[x])
            added_cards.append(deck[x])
            deck.remove(deck[x])

        if razz_evaluator(user_hand,cpu_hand):
            user_wins += 1
        elif razz_evaluator(user_hand,cpu_hand) is False:
            cpu_wins += 1
        elif razz_evaluator(user_hand,cpu_hand) == "Tie":
            ties += 1
        
        for x in added_cards:
            deck.append(x)
            if user_hand.count(x) > 0: 
                user_hand.remove(x)
            if cpu_hand.count(x) > 0:
                cpu_hand.remove(x)
    hand1_equity = ((user_wins+ties/2.0)/(user_wins+ties+cpu_wins))
    hand2_equity = ((cpu_wins+ties/2.0)/(user_wins+ties+cpu_wins))
    return query[0],hand1_equity,query[2],hand2_equity


def stud_equity_calculator(query):
    query = query.split()

    deck = [value+suit for suit in suits for value in values]
    hand1 = [x for x in query[0] if x != "*"]
    hand2 = [x for x in query[2] if x != "*"]
    
    user_wins = 0
    cpu_wins = 0
    ties = 0

    user_hand = ["".join(x) for x in zip(\
                    [x for x in hand1 if hand1.index(x) % 2 == 0],\
                    [x for x in hand1 if hand1.index(x) % 2 == 1])
                ]

    cpu_hand = ["".join(x) for x in zip(\
                    [x for x in hand2 if hand2.index(x) % 2 == 0],\
                    [x for x in hand2 if hand2.index(x) % 2 == 1])
               ]
    
    for x in user_hand:
        deck.remove(x)

    for x in cpu_hand:
        deck.remove(x)

    start = time.time()
    while user_wins + cpu_wins + ties < 5000:

        added_cards = []

        while len(user_hand) < 7:
            x = randrange(len(deck))
            user_hand.append(deck[x])
            added_cards.append(deck[x])
            deck.remove(deck[x])

        while len(cpu_hand) < 7:
            x = randrange(len(deck))
            cpu_hand.append(deck[x])
            added_cards.append(deck[x])
            deck.remove(deck[x])

        if holdem_evaluator(user_hand)[1] > holdem_evaluator(cpu_hand)[1]:
            user_wins += 1
        elif holdem_evaluator(user_hand)[1] < holdem_evaluator(cpu_hand)[1]:
            cpu_wins += 1
        else:
            if holdem_evaluator(user_hand)[2] > holdem_evaluator(cpu_hand)[2]:
                user_wins += 1
            elif holdem_evaluator(user_hand)[2] < holdem_evaluator(cpu_hand)[2]:
                cpu_wins += 1
            else:
                ties+=1
        
        for x in added_cards:
            deck.append(x)
            if user_hand.count(x) > 0: 
                user_hand.remove(x)
            if cpu_hand.count(x) > 0:
                cpu_hand.remove(x)

    hand1_equity = ((user_wins+ties/2.0)/(user_wins+ties+cpu_wins))
    hand2_equity = ((cpu_wins+ties/2.0)/(user_wins+ties+cpu_wins))
    return query[0],hand1_equity,query[2],hand2_equity

print omaha_headsup_flop_equity_calculator(["Kd","Qd","2c","2s"],["Qh","Jc","Tc","9s"],['Jd', 'Ts', '9d'])
