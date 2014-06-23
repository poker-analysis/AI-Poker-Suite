from random import randrange
from collections import Counter 
from itertools import combinations

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
    if len(indices)!=len(set(indices)): return False
    elif len(hand) < 5: return False
    elif sorted([x[:-1] for x in hand]) == ["2","3","4","5","A"]: return True
    elif 5*min(indices)+10 == sum(indices): return True
    else: return False 

def openended_draw_check(hand):
    indices = sorted([values.index(x[:-1])+1 for x in hand])
    if sum(indices[1:])==4*min(indices[1:])+6:
        return True,hand[1:]
    elif sum(indices[:4])==4*min(indices)+6:
        return True,hand[:4]
    else: return False

def flush_check(hand):
    for suit in suits: 
        if "".join(hand).count(suit) == 5: return True
    else: return False  

def flush_draw_check(hand):
    for suit in suits:
        if "".join(hand).count(suit) == 3 or "".join(hand).count(suit) == 4:
            return True,suit
    else: return False,-1

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
    hand_indices = sorted([values.index(x[:-1])+1 for x in hand])
    hand_pairs = [x for x,y in Counter(hand_indices).items() if y == 2]
    
    # If cpu draw lucky (Straight +), place the hand in the back
    if hand_evaluator(hand)[1] > 4:
        back.extend(hand)

    # If cpu draw trips, place trips + smallest of remainders in the back
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
        # Add two pair to the back
        for card in hand: 
            if values.index(card[:-1]) == hand_pairs[0]:
                back.append(card)
            elif back.count(card) == 0 and values.index(card[:-1])>=7:
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

    # Elif the computer has open ended straight draws, place in the back 
    elif openended_draw_check(hand) == True:
        back.append(openended_draw_check[1])
        if values.index([x for x in hand if x not in back][0][:-1]) > 8:
            middle.append(x)
        else: front.append([x for x in hand if x not in back][0])

    # Elif the computer has a pair, place in back 
    elif hand_evaluator(hand)[0] == "Pair":
        for card in hand: 
            if values.index(card[:-1]) == hand_pairs[0]:
                back.append(card)
            elif values.index(card[:-1]) > 10 and len(back)<3:
                back.append(card)
            elif values.index(card[:-1]) > 8 and len(middle)<2:
                middle.append(card)
            else: front.append(card)

    # Elif the computer has hi card, place the two highest in back, two medium in middle
    elif hand_evaluator(hand)[0] == "Hi-card":
        for card in hand:
            if values.index(card[:-1])+1 == hand_indices[3] or values.index(card[:-1])+1 == hand_indices[4]:
                back.append(card)
            elif values.index(card[:-1])+1 == hand_indices[1] or values.index(card[:-1])+1 == hand_indices[2]:
                middle.append(card)
            else: 
                front.append(card)

    print " ".join(back) + "\n" + " ".join(middle) + "\n" + " ".join(front)

def ai_place_draws(hand,draw):
    front = []
    middle = [] 
    back = []
    draw = [draw]

    front.extend(hand[0])
    middle.extend(hand[1])
    back.extend(hand[2])

    restricted_places = []

    # Prevent AI from fouling its hand, by noting restricted placements
    if len(front+middle+back) < 12:
        if len(front) < 3 and len(middle) < 5 and len(back) < 5:
            if is_foul(front+draw,middle,back) == True:
                restricted_places.append('front')
            elif is_foul(front,middle+draw,back) == True:
                restricted_places.append('middle')
            elif is_foul(front,middle,back+draw) == True:
                restricted_places.append('back')
        elif len(front) == 3 and len(middle) < 5 and len(back) < 5:
            restricted_places.append('front')
            if is_foul(front,middle+draw,back) == True:
                restricted_places.append('middle')
            elif is_foul(front,middle,back+draw) == True:
                restricted_places.append('back')
        elif len(front) < 3 and len(middle) == 5 and len(back) < 5:
            restricted_places.append('middle')
            if is_foul(front+draw,middle,back) == True:
                restricted_places.append('front')
            elif is_foul(front,middle,back+draw) == True:
                restricted_places.append('back')
        elif len(front) < 3 and len(middle) < 5 and len(back) == 5:
            restricted_places.append('back')
            if is_foul(front+draw,middle,back) == True:
                restricted_places.append('front')
            elif is_foul(front,middle+draw,back) == True:
                restricted_places.append('middle')

    # If all placements lead to a foul, just play any legal move
    if len(restricted_places) == 3:
        if len(front) < 3: return "front"
        elif len(middle) < 5: return "middle"
        elif len(back) < 5: return "back"

    # If two placements lead to a foul, play the final placement
    possible_places = ["front","middle","back"]
    if len(restricted_places) == 2:
        if list(set(possible_places)-set(restricted_places)) == ['front']:
            return "front"
        elif list(set(possible_places)-set(restricted_places)) == ['middle']:
            return "middle"
        elif list(set(possible_places)-set(restricted_places)) == ['back']:
            return "back"

    # If this is the final draw, place in the only legal location
    if len(front) == 3 and len(middle) == 5 and len(back) == 4:
        return "back"
    elif len(front) == 3 and len(middle) == 4 and len(back) == 5:
        return "middle"
    elif len(front) == 2 and len(middle) == 5 and len(back) == 5:
        return "front"

    # Algorithm for placement (right now, dummy algorithm for testing)
    if len(front) < 3: return "front"
    elif len(middle) < 5: return "middle"
    elif len(back) < 5: return "back"

def greedy_chinese_algorithm(front,middle,back):
    # Output best hand user could have created (with perfect information)
    greedy_front = []
    greedy_middle = []
    greedy_back = []

    new_deck = front + middle + back
    best = 0
    best_hand = []  
    for candidate in list(combinations(new_deck,5)):
        if hand_evaluator(candidate)[1] > best or hand_comparison(candidate,best_hand)==True:
            best = hand_evaluator(candidate)[1]
            best_hand = candidate

    greedy_back.extend(best_hand)

    for y in greedy_back: 
        new_deck.remove(y)

    best = 0 
    best_hand = []

    for candidate in list(combinations(new_deck,5)):
        if hand_evaluator(candidate)[1] > best or hand_comparison(candidate,best_hand)==True:
            best = hand_evaluator(candidate)[1]
            best_hand = candidate
    greedy_middle.extend(best_hand)

    for y in greedy_middle:
        new_deck.remove(y)

    greedy_front.extend(new_deck)

    print " ".join(greedy_front) + "       | " + hand_evaluator(greedy_front)[0]
    print " ".join(greedy_middle) + " | " + hand_evaluator(greedy_middle)[0]
    print " ".join(greedy_back) + " | " + hand_evaluator(greedy_back)[0]


def hu_openface(hand_target):
    hand_counter = 0
    button = 1

    while hand_counter < hand_target:
        front = []
        middle = []
        back = []
        overall_hand = [front,middle,back]
        cpu_indices = []
        user_hand = random_hand()

        # Deal a random hand to the CPU
        while len(cpu_indices) < 5:
            x = randrange(0,52)
            if cpu_indices.count(x) == 1 or user_hand.count(x) == 1: pass
            else: cpu_indices.append(x)

        cpu_hand = [create_deck()[x] for x in cpu_indices]
        cpu_front = []
        cpu_middle = []
        cpu_back = []
        cpu_overall = cpu_front + cpu_middle + cpu_back
        print "Your starting hand is " + " ".join(user_hand)

        # If button is odd, CPU has the button and user acts first
        if button == 1:
            # Prompt user for placement of initial starting hand
            for card in user_hand:
                place = raw_input("Where do you want to place " + str(card) + " : F, M or B? ")

                print "Your starting hand was " + "".join(user_hand)

                if place.lower() == "f" and len(front)<3: front.append(card)
                elif place.lower() == "m" and len(middle)<5: middle.append(card)
                elif place.lower() == "b" and len(back)<5: back.append(card)

                # Error Handling
                while place.lower() not in ("f", "m", "b") or \
                (front.count(card) == 0 and middle.count(card)==0 and back.count(card)==0): 

                    place = raw_input("Please enter F, M or B: ")

                    if place.lower() == "f" and len(front)<3: front.append(card)
                    elif place.lower() == "m" and len(middle)<5: middle.append(card)
                    elif place.lower() == "b" and len(back)<5: back.append(card)
                if len(front+middle+back)<5:
                    print " ".join(front) + "\n" + " ".join(middle) + "\n" + " ".join(back)
                    
            print "-----------------AI HAND-----------------"
            ai_starting_hand(cpu_hand)
            print "----------------USER HAND----------------"
            print " ".join(front) + "\n" + " ".join(middle) + "\n" + " ".join(back)

        cpu_front.extend(ai_starting_hand(cpu_hand)[0])
        cpu_middle.extend(ai_starting_hand(cpu_hand)[1])
        cpu_back.extend(ai_starting_hand(cpu_hand)[2])

        # Prompt user for placement of subsequent draws until hand is complete
        while len(front) + len(middle) + len(back) < 13:
            remaining_deck = [x for x in create_deck() if x not in front and x not in middle and x not in back and x not in cpu_overall]
            draw = remaining_deck[randrange(0,len(remaining_deck))]
            ai_draw = remaining_deck[randrange(0,len(remaining_deck))]

            while draw == ai_draw:
                ai_draw = remaining_deck[randrange(0,len(remaining_deck))]

            while len(cpu_front) + len(cpu_middle) + len(cpu_back) < 13:
                if ai_place_draws((cpu_front,cpu_middle,cpu_back),ai_draw) == "front":
                    cpu_front.append(ai_draw)
                elif ai_place_draws((cpu_front,cpu_middle,cpu_back),ai_draw) == "middle":
                    cpu_middle.append(ai_draw)
                elif ai_place_draws((cpu_front,cpu_middle,cpu_back),ai_draw) == "back":
                    cpu_back.append(ai_draw)

            # Provide user with the odds that they will foul for the sweat
            if len(front) + len(middle) + len(back) == 12:
                potential_fouls = 0
                for card in remaining_deck:

                    if len(front) < 3: front.append(card)
                    elif len(middle) < 5: middle.append(card)
                    elif len(back) < 5: back.append(card)

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

            print " ".join(cpu_back) + "\n" + " ".join(cpu_middle) + "\n" + " ".join(cpu_front)
            print " ".join(front) + "\n" + " ".join(middle) + "\n" + " ".join(back)

        # Returning final hand, foul information, and hand evaluation to user
        print "--------------------FINAL HAND--------------------"    
        print " ".join(front) + "       | " + hand_evaluator(front)[0]
        print " ".join(middle) + " | " + hand_evaluator(middle)[0]
        print " ".join(back) + " | " + hand_evaluator(back)[0]
        if is_foul(front,middle,back) == True: print "You fouled!"
        print "------------------GREEDY CHINESE------------------"
        greedy_chinese_algorithm(front,middle,back)
        hand_counter+=1
        button+=1

# sample test case that breaks 
print ai_starting_hand(["Tc", "Th", "8d", "5c", "5d"])
print ai_starting_hand(["Tc", "Jh", "3d", "Tc", "5d"])


