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
    else: return ("Hi-card",1)

def hand_comparison(hand1,hand2):
    hand1_name = hand_evaluator(hand1)[0]
    hand1_strength = hand_evaluator(hand1)[1]
    hand2_strength = hand_evaluator(hand2)[1]

    # Compare hand1/hand2 and resolve tiebreaks
    if hand1_strength > hand2_strength: return True
    elif hand1_strength < hand2_strength: return False
    
    else:
        if hand1_name == "Royal Flush": return "Tie"
        elif hand1_name == "Straight Flush": pass
        elif hand1_name == "Quads": pass
        elif hand1_name == "Full House": pass
        elif hand1_name == "Flush": pass
        elif hand1_name == "Straight": pass
        elif hand1_name == "Trips": pass
        elif hand1_name == "Two Pair": pass
        elif hand1_name == "Pair": pass
        elif hand1_name == "Hi-card": pass

def foul(front, middle, back):
    # return True if hand is fouled, false otherwise
    if hand_comparison(front,middle) == True: return True
    elif hand_comparison(front,back) == True: return True
    elif hand_comparison(middle,back) == True: return True
    else: return False
    
def single_player_openface():
    front = []
    middle = []
    back = []

    player1_hand = random_hand()
    print "Your starting hand is " + " ".join(player1_hand)

    # Prompt user for placement of initial starting hand
    for card in player1_hand:
        place = raw_input("Where do you want to place " + str(card) + " : F, M or B? ")

        print "Your starting hand was " + "".join(player1_hand)

        if place.lower() == "f" and len(front)<3: front.append(card)
        elif place.lower() =="m" and len(middle)<5: middle.append(card)
        elif place.lower() == "b" and len(back)<5: back.append(card)

        # Error Handling
        while place.lower() not in ("f", "m", "b") or \
        (front.count(card) == 0 and middle.count(card)==0 and back.count(card)==0): 

            place = raw_input("Please enter F, M or B: ")

            if place.lower() == "f" and len(front)<3: front.append(card)
            elif place.lower() =="m" and len(middle)<5: middle.append(card)
            elif place.lower() == "b" and len(back)<5: back.append(card)

        print " ".join(front) + "\n" + " ".join(middle) + "\n" + " ".join(back)

    # Prompt user for placement of subsequent draws until hand is complete
    while len(front) + len(middle) + len(back) < 13:
        remaining_deck = [x for x in create_deck() if x not in front and x not in middle and x not in back]
        card = remaining_deck[randrange(0,len(remaining_deck))]

        place = raw_input("Where do you want to place " + str(card) + " : F, M or B? ")

        if place.lower() == "f" and len(front)<3: front.append(card)
        elif place.lower() =="m" and len(middle)<5: middle.append(card)
        elif place.lower() == "b" and len(back)<5: back.append(card)
        
        # Error Handling
        while place.lower() not in ("f", "m", "b") or \
        (front.count(card) == 0 and middle.count(card)==0 and back.count(card)==0):  

            place = raw_input("Please enter F, M or B: ")

            if place.lower() == "f" and len(front)<3: front.append(card)
            elif place.lower() =="m" and len(middle)<5: middle.append(card)
            elif place.lower() == "b" and len(back)<5: back.append(card)

        print " ".join(front) + "\n" + " ".join(middle) + "\n" + " ".join(back)

    print "--------------------FINAL HAND--------------------"    
    print " ".join(front) + " " + hand_evaluator(front)[0]
    print " ".join(middle) + " " + hand_evaluator(middle)[0]
    print " ".join(back) + " " + hand_evaluator(back)[0]

single_player_openface()

