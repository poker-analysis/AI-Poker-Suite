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

def tiebreak(x):
	return x 

def hand_compare(hand1,hand2):
	if hand_evaluator(hand1)[1]>hand_evaluator(hand2)[1]:
		return "Player 1 wins"
	elif hand_evaluator(hand1)[1]<hand_evaluator(hand2)[1]:
		return "Player 2 wins"

print hand_evaluator(['9h','8h','2c','8s','Td'])



