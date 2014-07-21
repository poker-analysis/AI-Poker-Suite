from Tkinter import * 
from random import randrange
# Global Variables
suits = ["s","h","d","c"]
lo_values = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]
deck = [value+suit for suit in suits for value in lo_values]
user_hand = []
ai_hand = []
root = Tk()
down = PhotoImage(file="./img/BV.gif")
pot = 0
user_stack = 6000
ai_stack = 6000

def deal_hand():
    while len(user_hand) < 3:
        x = randrange(len(deck))
        user_hand.append(deck[x])
        deck.remove(deck[x])

    while len(ai_hand) < 3:
        x = randrange(len(deck))
        ai_hand.append(deck[x])
        deck.remove(deck[x])

deal_hand()

user_up = PhotoImage(file="./img/"+user_hand[2]+".gif")
ai_up = PhotoImage(file="./img/"+ai_hand[2]+".gif")

def paint_hand():
    Label(root,text="User: %d" % (user_stack)).grid(row=1,column=0)
    Label(root,image=down).grid(row=1,column=1)
    Label(root,image=down).grid(row=1,column=2)
    Label(root,image=user_up).grid(row=1,column=3)
    Label(root,text="AI: %d" % (ai_stack)).grid(row=5,column=0)
    Label(root,image=down).grid(row=5,column=1)
    Label(root,image=down).grid(row=5,column=2)
    Label(root,image=ai_up).grid(row=5,column=3)

def ante():
    global pot
    global user_stack
    global ai_stack
    pot += 30
    user_stack -= 15
    ai_stack -= 15

def bringin():
    global pot
    global user_stack
    bet = 30
    pot += 30
    user_stack -=30
    Label(root,text="User: %d" % (user_stack)).grid(row=1,column=0)
    Label(root,text="%d" % (bet)).grid(row=2,column=3)
    Label(root,text=pot).grid(row=3,column=3)

def complete():
    global pot
    global user_stack
    bet = 100
    pot += 100
    user_stack -= 100
    Label(root,text="User: %d" % (user_stack)).grid(row=1,column=0)
    Label(root,text="%d" % (bet)).grid(row=2,column=3)
    Label(root,text=pot).grid(row=3,column=3)

ante()
# Show Third Street Buttons
if lo_values.index(user_hand[2][0]) > lo_values.index(ai_hand[2][0]):
    Button(root,text="Bring-In $30",command=bringin).grid(row=6,columnspan=1)
    Button(root,text="Complete $100",command=complete).grid(row=7,columnspan=1)
elif lo_values.index(user_hand[2][0]) < lo_values.index(ai_hand[2][0]):
    pass
else:
    if user_hand[2][1] > ai_hand[2][1]:
        Button(root,text="Bring-In $30",command=bringin).grid(row=6,columnspan=1)
        Button(root,text="Complete $100",command=complete).grid(row=7,columnspan=1)
    elif user_hand[2][1] < ai_hand[2][1]:
        pass    


paint_hand()

root.mainloop()