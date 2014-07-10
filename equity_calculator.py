from itertools import combinations
from itertools import izip as zip,count
from collections import Counter
from random import randrange
import time 

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

    if h1_lo == h2_lo:
        return "Tie"

    elif list(set(h1_lo)) == h1_lo and list(set(h2_lo)) == h2_lo:
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
    
def plo_evaluator(total_board):
    pass


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
            elif holdem_evaluator(x+cpu_hand)[2] < holdem_evaluator(x+user_hand)[2]:
                cpu_wins += 1
            else:
                ties+=1
    print "====================SIMULATION RESULTS===================="
    print hand1 + " equity: %f" % ((user_wins*1.0+ties/2.0)/(user_wins+cpu_wins+ties))
    print hand2 + " equity: %f" % ((cpu_wins*1.0+ties/2.0)/(user_wins+cpu_wins+ties))
    elapsed = time.time() - start
    print "Exhaustive search. Calculated in: %s seconds" % (elapsed) 
 

def razz_equity_calculator(hand1,hand2):
    if len(hand1)!=len(hand2):
        return "Please enter two legal hands."
    deck = [value+suit for suit in suits for value in values]
    
    user_hand = []
    cpu_hand = []

    user_wins = 0
    cpu_wins = 0
    ties = 0

    for x in xrange(0,len(hand1),2):
        if x+2 > len(hand1) - 1:
            deck.remove(hand1[x:]), user_hand.append(hand1[x:])
            deck.remove(hand2[x:]), cpu_hand.append(hand2[x:])

        else:
            deck.remove(hand1[x:x+2]), user_hand.append(hand1[x:x+2])
            deck.remove(hand2[x:x+2]), cpu_hand.append(hand2[x:x+2])
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

    print "====================SIMULATION RESULTS===================="
    print hand1 + " equity: %f" % ((user_wins*1.0+ties/2.0)/(user_wins+cpu_wins+ties))
    print hand2 + " equity: %f" % ((cpu_wins*1.0+ties/2.0)/(user_wins+cpu_wins+ties))
    elapsed = time.time() - start
    print "Random search. Calculated in: %s seconds" % (elapsed) 
