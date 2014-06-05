from random import randrange
from collections import Counter 

# global variables
suits = ["s","h","d","c"]
values = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]

def create_deck():
    deck = []
    for value in values: 
        for suit in suits:
            deck.append(value+suit)
    return deck 

def random_hand():
    cards = []
    while len(cards) < 5:
        x = randrange(0,52)
        if cards.count(x) == 1: pass
        else: cards.append(x)
    hand = [create_deck()[x] for x in cards]
    return hand

def straight_check(hand):
    indices = [values.index(x[:-1])+1 for x in hand]
    if sorted([x[:-1] for x in hand]) == ["A","J","K","Q","T"]: return True
    elif 5*min(indices)+10 == sum(indices): return True
    else: return False 

def flush_check(hand):
    for suit in suits: 
        if "".join(hand).count(suit) == 5: return True
    else: return False  

def fullhouse_check(hand):
    pairs = []
    for x in values: 
        pairs.append([card[:-1] for card in hand].count(x))
    if sorted(list(set(pairs)))==[0,2,3]: return True
    else: return False 

def hand_evaluator(hand):
    royal_flushes = [["Ah",'Jh','Kh','Qh','Th'],["Ac",'Jc','Kc','Qc','Tc'],
                    ["As",'Js','Ks','Qs','Ts'],["Ad",'Jd','Kd','Qd','Td']]
    if royal_flushes.count(sorted(hand)) == 1:
        return ("Royal Flush",10)
    elif straight_check(hand)==True and flush_check(hand)==True:
        return ("Straight Flush",9)
    elif [x for x,y in Counter([card[:-1] for card in hand]).items() if y == 4] != []:
        return ("Quads",8)
    elif fullhouse_check(hand)==True: return ("Full House",7)
    elif flush_check(hand)==True: return ("Flush",6)
    elif straight_check(hand)==True: return ("Straight",5)
    elif [x for x,y in Counter([card[:-1] for card in hand]).items() if y == 3] != []:
        return ("Trips",4)
    elif len([x for x,y in Counter([card[:-1] for card in hand]).items() if y == 2]) == 2:
        return ("Two Pair",3)
    elif len([x for x,y in Counter([card[:-1] for card in hand]).items() if y == 2]) == 1:
        return ("Pair",2)
    else: return ("Hi card",1)

def single_player():
    front = []
    middle = []
    back = []

    player1_hand = random_hand()
    print "Your starting hand is " + "".join(player1_hand)

    for card in player1_hand:
        place = raw_input("Where do you want to place " + str(card) + " : F, M or B? ")
        print "Your starting hand was " + "".join(player1_hand)

        if place == "F" and len(front)<3: front.append(card)
        elif place =="M" and len(middle)<5: middle.append(card)
        elif place == "B" and len(back)<5: back.append(card)

        print "".join(front) + "\n" + "".join(middle) + "\n" + "".join(back)

    while len(front) + len(middle) + len(back) < 13:
        remaining_deck = [x for x in create_deck() if x not in front or x not in middle or x not in back]
        draw = remaining_deck[randrange(0,len(remaining_deck))]

        place = raw_input("Where do you want to place " + str(draw) + " : F, M or B? ")

        if place == "F" and len(front)<3: front.append(draw)
        elif place =="M" and len(middle)<5: middle.append(draw)
        elif place == "B" and len(back)<5: back.append(draw)
        
        print "".join(front) + "\n" + "".join(middle) + "\n" + "".join(back)

    print "--------------------FINAL HAND--------------------"    
    print "".join(front) + " " + hand_evaluator(front)[0]
    print "".join(middle) + " " + hand_evaluator(middle)[0]
    print "".join(back) + " " + hand_evaluator(back)[0]

single_player()

