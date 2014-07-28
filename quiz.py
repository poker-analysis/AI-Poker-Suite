# Quiz: Test your knowledge of equity of poker hands

from Tkinter import * 
from random import randrange
from equity_calculator import holdem_postflop_equity_calculator as hpec
from math import fabs

# Global Variables
suits = ["s","h","d","c"]
lo_values = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]
deck = [value+suit for suit in suits for value in lo_values]
root = Tk()
incorrect = 0
correct = 0
user_hand = []
villain_hand = []
flop = []

def quiz():
    root.wm_title("PokerQuiz v1.0")
    root.configure(background='grey95')

    def callback():
        global correct
        global incorrect
        answer = int(e.get())
        actual = 100.0*hpec("".join(board),"".join(hero),"".join(villain))[1]
        difference = answer - actual 
        if fabs(answer - actual) <= 3:
            Label(root,text="Correct: %.2f equity" % (actual)).grid(row=5,column=0)
            correct += 1
        else:
            Label(root,text="Incorrect: %.2f equity" % (actual)).grid(row=5,column=0)
            incorrect += 1
        Label(root,text="Correct: %s" % (correct)).grid(row=5,column=2)
        Label(root,text="Incorrect: %s" % (incorrect)).grid(row=5,column=3)

    def next():
        for child in root.winfo_children():
            child.destroy()
        quiz()
    
    deck = [value+suit for suit in suits for value in lo_values]

    while len(user_hand) < 2:
        x = randrange(len(deck))
        user_hand.append(deck[x])
        deck.remove(deck[x])

    while len(villain_hand) < 2:
        x = randrange(len(deck))
        villain_hand.append(deck[x])
        deck.remove(deck[x])

    while len(flop) < 3:
    	x = randrange(len(deck))
    	flop.append(deck[x])
    	deck.remove(deck[x])

    hero = user_hand[:]
    villain = villain_hand[:]
    board = flop[:]

    user_card = PhotoImage(file="./img/"+user_hand[0]+".gif")
    user_card2 = PhotoImage(file="./img/"+user_hand[1]+".gif")
    villain_card = PhotoImage(file="./img/"+villain_hand[0]+".gif")
    villain_card2 = PhotoImage(file="./img/"+villain_hand[1]+".gif")
    flop1 = PhotoImage(file="./img/"+flop[0]+".gif")
    flop2 = PhotoImage(file="./img/"+flop[1]+".gif")
    flop3 = PhotoImage(file="./img/"+flop[2]+".gif")

    Label(root,text="Hero").grid(row=1,column=0)
    Label(root,image=user_card).grid(row=1,column=1)
    Label(root,image=user_card2).grid(row=1,column=2)
    Label(root,text="Villain").grid(row=2,column=0)
    Label(root,image=villain_card).grid(row=2,column=1)
    Label(root,image=villain_card2).grid(row=2,column=2)
    Label(root,text="Flop").grid(row=3,column=0)
    Label(root,image=flop1).grid(row=3,column=1)
    Label(root,image=flop2).grid(row=3,column=2)
    Label(root,image=flop3).grid(row=3,column=3)
    e=Entry(root,width=15)
    e.grid(row=4, column=0)
    e.focus_set()

    b = Button(root, text="Submit", width=5, command=callback).grid(row=4,column=1)
    n = Button(root, text="Next", width=5, command=next).grid(row=4,column=2)
    Label(root,text="Correct: %s" % (correct)).grid(row=5,column=2)
    Label(root,text="Incorrect: %s" % (incorrect)).grid(row=5,column=3)

    for x in user_hand:
        user_hand.remove(x)
        deck.append(x)
    for x in villain_hand:
        villain_hand.remove(x)
        deck.append(x)
    for x in flop:
        flop.remove(x)
        deck.append(x)

    root.mainloop()

quiz()
