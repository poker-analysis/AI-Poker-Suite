from itertools import combinations
from itertools import izip as zip,count
from collections import Counter
from random import randrange
import time 

suits = ["s","h","d","c"]
values = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]
lo_values = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]

def create_deck():
    deck = []
    for value in values: 
        for suit in suits:
            deck.append(value + suit)
    return deck 


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
        if set.issubset(set(x),set(total_board)) == True:
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
        for x in xrange(12,-1,-1):
            if len(hand_values) == 3:
                break
            if pairs[x] == 1:
                hand_values.append(x+2)
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
        return "High Card", 0, max([values.index(x[0]) for x in total_board])


def razz_evaluator(hand1,hand2):
    h1_lo = []
    h2_lo = []

    h1_set = sorted(set([lo_values.index(x[0]) for x in hand1]))
    h2_set = sorted(set([lo_values.index(x[0]) for x in hand2]))

    # Add to each array the lowest unpaired elements
    # Add to each array the paired elements until hand complete
    print h1_set,h2_set

def plo_evaluator(total_board):
    pass


def holdem_preflop_equity_calculator(hand1,hand2):
    
    start = time.time()

    user_wins = 0
    cpu_wins = 0
    ties = 0
    
    deck = create_deck()
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
    
    print "====================SIMULATION RESULTS===================="
    print hand1 + " equity: %f" % ((user_wins*1.0+ties/2.0)/(user_wins+cpu_wins+ties))
    print hand2 + " equity: %f" % ((cpu_wins*1.0+ties/2.0)/(user_wins+cpu_wins+ties))
    elapsed = time.time() - start
    print "Calculated 17123 runs in: %s seconds" % (elapsed) 


def holdem_postflop_equity_calculator(board,hand1,hand2):
    # Because the number of computations is bounded at 990 hands, we can search
    # exhaustively through all possible outcomes to calculate equity. 
    start = time.time()

    user_wins = 0
    cpu_wins = 0
    ties = 0

    user_hand = [hand1[:2],hand1[2:]]
    cpu_hand = [hand2[:2],hand2[2:]]
    
    deck = create_deck()
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
    for x in xrange(0,len(combos)):
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
    print "====================SIMULATION RESULTS===================="
    print hand1 + " equity: %f" % ((user_wins*1.0+ties/2.0)/(user_wins+cpu_wins+ties))
    print hand2 + " equity: %f" % ((cpu_wins*1.0+ties/2.0)/(user_wins+cpu_wins+ties))
    elapsed = time.time() - start
    print "Exhaustive search. Calculated in: %s seconds" % (elapsed) 
