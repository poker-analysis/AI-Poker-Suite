# Quiz: Test your knowledge of equity of poker hands

from Tkinter import * 
from random import randrange
from equity_calculator import holdem_postflop_equity_calculator as hpec
from equity_calculator import razz_equity_calculator as razz_calc
from equity_calculator import stud_equity_calculator as stud_calc
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

    def holdem_solve():
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

    def razz_solve():
        global correct
        global incorrect 

        answer = int(e.get())
        actual = 100.0*razz_calc("".join(hero) + " vs " + "".join(villain)+"xx")[1]
        difference = answer - actual 
        if fabs(answer - actual) <= 5:
            Label(root,text="Correct: %.2f equity" % (actual)).grid(row=5,column=0)
            correct += 1
        else:
            Label(root,text="Incorrect: %.2f equity" % (actual)).grid(row=5,column=0)
            incorrect += 1
        Label(root,text="Correct: %s" % (correct),background='grey95').grid(row=5,column=2)
        Label(root,text="Incorrect: %s" % (incorrect),background='grey95').grid(row=5,column=3)

    def stud_solve():
        global correct
        global incorrect 

        answer = int(e.get())
        actual = 100.0*stud_calc("".join(hero) + " vs " + "".join(villain)+"xx")[1]
        difference = answer - actual 
        if fabs(answer - actual) <= 5:
            Label(root,text="Correct: %.2f equity" % (actual)).grid(row=5,column=0)
            correct += 1
        else:
            Label(root,text="Incorrect: %.2f equity" % (actual)).grid(row=5,column=0)
            incorrect += 1
        Label(root,text="Correct: %s" % (correct),background='grey95').grid(row=5,column=2)
        Label(root,text="Incorrect: %s" % (incorrect),background='grey95').grid(row=5,column=3)

    def next():
        for child in root.winfo_children():
            child.destroy()
        quiz()
    
    deck = [value+suit for suit in suits for value in lo_values]

    game = randrange(1,4)

    # Hold Em Post Flop Quiz
    if game == 1:
        print len(deck),len(user_hand),len(villain_hand),len(flop)
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

        Label(root,text="Hero",background='grey95').grid(row=1,column=0)
        Label(root,image=user_card,background='grey95').grid(row=1,column=1)
        Label(root,image=user_card2,background='grey95').grid(row=1,column=2)
        Label(root,text="Villain",background='grey95').grid(row=2,column=0)
        Label(root,image=villain_card,background='grey95').grid(row=2,column=1)
        Label(root,image=villain_card2,background='grey95').grid(row=2,column=2)
        Label(root,text="Flop",background='grey95').grid(row=3,column=0)
        Label(root,image=flop1,background='grey95').grid(row=3,column=1)
        Label(root,image=flop2,background='grey95').grid(row=3,column=2)
        Label(root,image=flop3,background='grey95').grid(row=3,column=3)
        e=Entry(root,width=15)
        e.grid(row=4, column=0)
        e.focus_set()

        b = Button(root, text="Submit", width=5, command=holdem_solve,relief="flat").grid(row=4,column=1)
        n = Button(root, text="Next", width=5, command=next,relief="flat").grid(row=4,column=2)
        Label(root,text="Hold Em",background='grey95').grid(row=5,column=1)
        Label(root,text="Correct: %s" % (correct),background='grey95').grid(row=5,column=2)
        Label(root,text="Incorrect: %s" % (incorrect),background='grey95').grid(row=5,column=3)
        print user_hand,villain_hand,flop
        deck.extend(user_hand)
        deck.extend(villain_hand)
        deck.extend(flop)
        del user_hand[:]
        del villain_hand[:]
        del flop[:]
        print user_hand,villain_hand,flop

    # Razz Fifth Street Quiz
    elif game == 2:
        print len(deck),len(user_hand),len(villain_hand)
        while len(user_hand) < 5:
            x = randrange(len(deck))
            user_hand.append(deck[x])
            deck.remove(deck[x])

        while len(villain_hand) < 3:
            x = randrange(len(deck))
            villain_hand.append(deck[x])
            deck.remove(deck[x])

        hero = user_hand[:]
        villain = villain_hand[:]

        user_card = PhotoImage(file="./img/"+user_hand[0]+".gif")
        user_card2 = PhotoImage(file="./img/"+user_hand[1]+".gif")
        user_card3 = PhotoImage(file="./img/"+user_hand[2]+".gif")
        user_card4 = PhotoImage(file="./img/"+user_hand[3]+".gif")
        user_card5 = PhotoImage(file="./img/"+user_hand[4]+".gif")

        down_card = PhotoImage(file="./img/BV.gif")
        villain_card = PhotoImage(file="./img/"+villain_hand[0]+".gif")
        villain_card2 = PhotoImage(file="./img/"+villain_hand[1]+".gif")
        villain_card3 = PhotoImage(file="./img/"+villain_hand[2]+".gif")

        Label(root,text="Hero",background='grey95').grid(row=1,column=0)
        Label(root,image=user_card,background='grey95').grid(row=1,column=1)
        Label(root,image=user_card2,background='grey95').grid(row=1,column=2)
        Label(root,image=user_card3,background='grey95').grid(row=1,column=3)
        Label(root,image=user_card4,background='grey95').grid(row=1,column=4)
        Label(root,image=user_card5,background='grey95').grid(row=1,column=5)

        Label(root,text="Villain",background='grey95').grid(row=2,column=0)
        Label(root,image=down_card,background='grey95').grid(row=2,column=1)
        Label(root,image=down_card,background='grey95').grid(row=2,column=2)
        Label(root,image=villain_card,background='grey95').grid(row=2,column=3)
        Label(root,image=villain_card2,background='grey95').grid(row=2,column=4)
        Label(root,image=villain_card3,background='grey95').grid(row=2,column=5)
        
        e=Entry(root,width=15)
        e.grid(row=4, column=0)
        e.focus_set()

        b = Button(root, text="Submit", width=5, command=razz_solve,borderwidth=.001).grid(row=4,column=1)
        n = Button(root, text="Next", width=5, command=next,borderwidth=.001).grid(row=4,column=2)
        Label(root,text="Razz",background='grey95').grid(row=5,column=1)
        Label(root,text="Correct: %s" % (correct),background='grey95').grid(row=5,column=2)
        Label(root,text="Incorrect: %s" % (incorrect),background='grey95').grid(row=5,column=3)
        
        print user_hand,villain_hand
        deck.extend(user_hand)
        deck.extend(villain_hand)
        del user_hand[:]
        del villain_hand[:]
        print user_hand,villain_hand

    # Stud Fifth Street Quiz
    elif game == 3:
        print len(deck),len(user_hand),len(villain_hand)
        while len(user_hand) < 5:
            x = randrange(len(deck))
            user_hand.append(deck[x])
            deck.remove(deck[x])

        while len(villain_hand) < 3:
            x = randrange(len(deck))
            villain_hand.append(deck[x])
            deck.remove(deck[x])

        hero = user_hand[:]
        villain = villain_hand[:]

        user_card = PhotoImage(file="./img/"+user_hand[0]+".gif")
        user_card2 = PhotoImage(file="./img/"+user_hand[1]+".gif")
        user_card3 = PhotoImage(file="./img/"+user_hand[2]+".gif")
        user_card4 = PhotoImage(file="./img/"+user_hand[3]+".gif")
        user_card5 = PhotoImage(file="./img/"+user_hand[4]+".gif")

        down_card = PhotoImage(file="./img/BV.gif")
        villain_card = PhotoImage(file="./img/"+villain_hand[0]+".gif")
        villain_card2 = PhotoImage(file="./img/"+villain_hand[1]+".gif")
        villain_card3 = PhotoImage(file="./img/"+villain_hand[2]+".gif")

        Label(root,text="Hero",background='grey95').grid(row=1,column=0)
        Label(root,image=user_card,background='grey95').grid(row=1,column=1)
        Label(root,image=user_card2,background='grey95').grid(row=1,column=2)
        Label(root,image=user_card3,background='grey95').grid(row=1,column=3)
        Label(root,image=user_card4,background='grey95').grid(row=1,column=4)
        Label(root,image=user_card5,background='grey95').grid(row=1,column=5)

        Label(root,text="Villain",background='grey95').grid(row=2,column=0)
        Label(root,image=down_card,background='grey95').grid(row=2,column=1)
        Label(root,image=down_card,background='grey95').grid(row=2,column=2)
        Label(root,image=villain_card,background='grey95').grid(row=2,column=3)
        Label(root,image=villain_card2,background='grey95').grid(row=2,column=4)
        Label(root,image=villain_card3,background='grey95').grid(row=2,column=5)
        
        e=Entry(root,width=15)
        e.grid(row=4, column=0)
        e.focus_set()

        b = Button(root, text="Submit", width=5, command=stud_solve,borderwidth=.001).grid(row=4,column=1)
        n = Button(root, text="Next", width=5, command=next,borderwidth=.001).grid(row=4,column=2)
        Label(root,text="Stud Hi",background='grey95').grid(row=5,column=1)
        Label(root,text="Correct: %s" % (correct),background='grey95').grid(row=5,column=2)
        Label(root,text="Incorrect: %s" % (incorrect),background='grey95').grid(row=5,column=3)
        
        print user_hand,villain_hand
        deck.extend(user_hand)
        deck.extend(villain_hand)
        del user_hand[:]
        del villain_hand[:]
        print user_hand,villain_hand
        
    root.mainloop()

quiz()
