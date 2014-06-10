from random import randrange
from collections import Counter 

# global variables
suits = ["s","h","d","c"]
values = ["2","3","4","5","6","7","8","9","T","J","Q","K","A"]

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
    if sorted([x[:-1] for x in hand]) == ["2","3","4","5","A"]: return True
    elif len(hand) < 5: return False
    elif 5*min(indices)+10 == sum(indices): return True
    else: return False 

def flush_check(hand):
    for suit in suits: 
        if "".join(hand).count(suit) == 5: return True
    else: return False  

def flush_draw_check(hand):
    for suit in suits:
        if "".join(hand).count(suit) == 3 or "".join(hand).count(suit) == 4:
            return True,suit
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
    # Output True if hand1 beats hand2, or False, or Tie if hand1 == hand2
    # Useful variables for implementing tiebreak resolution:
    hand1_name = hand_evaluator(hand1)[0]
    hand1_strength = hand_evaluator(hand1)[1]
    hand2_strength = hand_evaluator(hand2)[1]
    h1_indices = [values.index(x[:-1])+1 for x in hand1]
    h2_indices = [values.index(x[:-1])+1 for x in hand2]
    h1_common = max(set(h1_indices), key=h1_indices.count)
    h2_common = max(set(h2_indices), key=h2_indices.count)

    # Compare hand1/hand2 and resolve tiebreaks
    if hand1_strength > hand2_strength: 
        return True
    elif hand1_strength < hand2_strength: 
        return False
    else:
        if sorted(h1_indices) == sorted(h2_indices):
            return "Tie"
        elif hand1_name == "Straight Flush" or hand1_name == "Straight":
            return sorted(h1_indices)[0] > sorted(h2_indices)[0] 
        elif hand1_name == "Quads" or hand1_name == "Full House" or hand1_name == "Trips":
            return h1_common > h2_common
        elif hand1_name == "Flush" or hand1_name == "Hi-card":
            return sorted(h1_indices)[::-1] > sorted(h2_indices)[::-1]
        elif hand1_name == "Two Pair":
            if h1_common == h2_common:
                h1_pairs = [x for x,y in Counter(h1_indices).items() if y == 2]
                h2_pairs = [x for x,y in Counter(h2_indices).items() if y == 2]
                if sorted(h1_pairs) == sorted(h2_pairs):
                    return sorted(list(set(h1_pairs))) > sorted(list(set(h1_pairs)))
                else: 
                    return sorted(h1_pairs)[::-1] > sorted(h2_pairs)[::-1]
            else: 
                return h1_common > h2_common

        elif hand1_name == "Pair":
            if h1_common == h2_common:
                return sorted(h1_indices)[::-1] > sorted(h2_indices)[::-1]
            else: 
                return h1_common > h2_common

def is_foul(front, middle, back):
    # return True if hand is fouled, False otherwise
    if hand_comparison(front,middle) == True or hand_comparison(front,back) == True \
    or hand_comparison(middle,back) == True: return True
    else: return False

def ai_starting_hand(hand):
    # Breakdown:
    # How the computer should place the top 7.618544 % of its opening range
    # How the computer should place the rest of its range (draws, garbage, etc.)
    front = []
    middle = []
    back = []
    hand_indices = [values.index(x[:-1])+1 for x in hand]
    hand_pairs = [x for x,y in Counter(hand_indices).items() if y == 2]

    
    # If you draw lucky (Straight +), place the hand in the back
    if hand_evaluator(hand)[1] > 4:
        back.append(hand)

    # If you draw trips, place trips + smallest of remainders in the back
    elif hand_evaluator(hand)[0] == "Trips":
        trip_value = max(set(hand_indices), key=hand_indices.count)
        for card in hand:
            if hand_indices.count(values.index(card[:-1])+1)==3:
                back.append(card)
        # Place weakest value in the back to draw to a full house
        remainder = [values.index(card[:-1]) for card in hand if back.count(card) == 0]
        for card in hand:
            if values.index(card[:-1]) == min(remainder): 
                back.append(card)
            elif back.count(card) == 0 and values.index(card[:-1])<7:
                front.append(card)
            elif back.count(card) == 0:
                middle.append(card)

    # Place the fifth card on the front if it is weak, middle if it is strong
    elif hand_evaluator(hand)[0] == "Two Pair":
        for card in hand: 
            if hand_indices.count(values.index(card[:-1])+1)>1:
                back.append(card)
        for card in hand:
            if back.count(card) == 0 and values.index(card[:-1])>=7:
                middle.append(card)
            else: front.append(card)

    # If the computer has flush draws (3 card, 4 card), place in the back
    elif flush_draw_check(hand)[0] == True:
        for card in hand: 
            if card[-1:] == flush_draw_check(hand)[1]:
                back.append(card)
            elif values.index(card[:-1])>=7:
                middle.append(card)
            else: front.append(card)

    return front, middle, back

def single_player_openface():
    front = []
    middle = []
    back = []
    overall_hand = [front,middle,back]

    player1_hand = random_hand()
    print "Your starting hand is " + " ".join(player1_hand)
    # Prompt user for placement of initial starting hand
    # Button placement, while statement until the user ends session
    # If CPU has button, then play. If human has button, you play first.
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
        draw = remaining_deck[randrange(0,len(remaining_deck))]

        # Provide user with the odds that they will foul for the sweat
        if len(front) + len(middle) + len(back) == 12:
            potential_fouls = 0
            for card in remaining_deck:
                if len(front) < 3:
                    front.append(card)
                elif len(middle) < 5:
                    middle.append(card)
                elif len(back) < 5:
                    back.append(card)
                if is_foul(front,middle,back)==True:
                    potential_fouls +=1
                if front.count(card) > 0: front.remove(card)
                elif middle.count(card) > 0: middle.remove(card)
                elif back.count(card) > 0: back.remove(card)


            print potential_fouls,len(remaining_deck)
            print "You have a %f percent chance of fouling your hand!" % (100.0*potential_fouls/len(remaining_deck))

        place = raw_input("Where do you want to place " + str(draw) + " : F, M or B? ")

        if place.lower() == "f" and len(front)<3: front.append(draw)
        elif place.lower() =="m" and len(middle)<5: middle.append(draw)
        elif place.lower() == "b" and len(back)<5: back.append(draw)
        
        while place.lower() not in ("f", "m", "b") or \
        (front.count(draw) == 0 and middle.count(draw)==0 and back.count(draw)==0):  
            print front,middle,back
            place = raw_input("Please enter F, M or B: ")

            if place.lower() == "f" and len(front)<3: front.append(draw)
            elif place.lower() =="m" and len(middle)<5: middle.append(draw)
            elif place.lower() == "b" and len(back)<5: back.append(draw)

            # DEBUG: Debugging print statements

        print " ".join(front) + "\n" + " ".join(middle) + "\n" + " ".join(back)

    # Returning final hand, foul information, and hand evaluation to user
    print "--------------------FINAL HAND--------------------"    
    print " ".join(front) + "       | " + hand_evaluator(front)[0]
    print " ".join(middle) + " | " + hand_evaluator(middle)[0]
    print " ".join(back) + " | " + hand_evaluator(back)[0]
    if is_foul(front,middle,back) == True: print "You fouled!"

single_player_openface()

