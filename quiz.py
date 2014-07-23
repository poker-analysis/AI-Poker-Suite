# Quiz: Test your knowledge of equity of poker hands

from Tkinter import * 
from random import randrange

# Global Variables
suits = ["s","h","d","c"]
lo_values = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]
deck = [value+suit for suit in suits for value in lo_values]
user_hand = []
villain_hand = []
flop = []
root = Tk()

def random_hand():
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

def preflop_quiz():
    user_card = PhotoImage(file="./img/"+user_hand[0]+".gif")
    user_card2 = PhotoImage(file="./img/"+user_hand[1]+".gif")
    villain_card = PhotoImage(file="./img/"+villain_hand[0]+".gif")
    villain_card2 = PhotoImage(file="./img/"+villain_hand[1]+".gif")

    Label(root,text="Hero").grid(row=1,column=0)
    Label(root,image=user_card).grid(row=1,column=1)
    Label(root,image=user_card2).grid(row=1,column=2)
    Label(root,text="Villain").grid(row=2,column=0)
    Label(root,image=villain_card).grid(row=2,column=1)
    Label(root,image=villain_card2).grid(row=2,column=2)

root.mainloop()
