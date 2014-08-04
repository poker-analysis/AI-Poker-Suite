#!/usr/bin/env python

# PokerTempo: test your knowledge of equity in different poker games
import pygtk
pygtk.require('2.0')
import gtk
from random import randrange
from equity_calculator import holdem_postflop_equity_calculator as hpec
from equity_calculator import razz_equity_calculator as razz_calc
from equity_calculator import stud_equity_calculator as stud_calc
from math import fabs

# Global Variables
suits = ["s","h","d","c"]
lo_values = ["A","2","3","4","5","6","7","8","9","T","J","Q","K"]
deck = [value+suit for suit in suits for value in lo_values]
incorrect = 0
correct = 0
user_hand = []
villain_hand = []
flop = []

def holdem_tempo(self):
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
    
    # Hero + Villain Hands
    for x in xrange(2):
        hero_card = gtk.Image()
        villain_card = gtk.Image()
        hero_card.set_from_file("./img/"+user_hand[x]+".gif")
        villain_card.set_from_file("./img/"+villain_hand[x]+".gif")
        self.table.attach(villain_card,x+1,x+2,1,2)
        self.table.attach(hero_card,x+1,x+2,0,1)
        hero_card.show()
        villain_card.show()

    # Flop
    for x in xrange(3):
        flop_card = gtk.Image()
        flop_card.set_from_file("./img/" + flop[x] + ".gif")
        self.table.attach(flop_card,x+1,x+2,2,3)
        flop_card.show()

    # Labels
    label = gtk.Label('Hero')
    self.table.attach(label,0,1,0,1)
    label.show()

    label = gtk.Label('Villain')
    self.table.attach(label,0,1,1,2)
    label.show()

    label = gtk.Label('Flop')
    self.table.attach(label,0,1,2,3)
    label.show()

    # Entry
    self.entry = gtk.Entry()
    self.entry.set_max_length(6)
    self.entry.set_width_chars(1)
    self.table.attach(self.entry,2,3,3,4)
    self.entry.show()

    self.button = gtk.Button(label="Submit")
    self.button.connect("clicked",self.holdem_solve,self.button)
    self.table.attach(self.button,1,2,3,4)
    self.button.show()

    self.table.set_row_spacings(8)
    self.table.set_col_spacings(3)
    self.window.set_border_width(14)

    return hero,villain,board

class PokerTempo:

    def __init__(self):
        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("PokerTempo v1.0")
        self.window.connect("delete_event", self.delete_event)

        self.table = gtk.Table(4, 4, False)
        self.window.add(self.table)

        stored_values = holdem_tempo(self)
        self.hero = stored_values[0]
        self.villain = stored_values[1]
        self.board = stored_values[2] 

        self.hbox = gtk.HBox()
        self.hbox.pack_start(self.button)
        self.window.add(self.hbox)
        self.table.show()
        self.window.show()


    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def reset(self,widget,event,data=None):
        self.window.remove(self.table)
        print list(self.window)

    def holdem_solve(self, widget, callback_data=None):
        answer = int(self.entry.get_text())
        actual = 100.0*hpec("".join(self.board),"".join(self.hero),"".join(self.villain))[1]
        if fabs(answer - actual) <= 5:
            label = gtk.Label("Correct: %.2f equity" % (actual))
        else:
            label = gtk.Label("Incorrect: %.2f equity" % (actual))
        self.table.attach(label,4,5,4,5)
        label.show()
        self.next = gtk.Button(label="Next")
        self.next.connect("clicked",self.reset,self.next)
        self.table.attach(self.next,4,5,3,4)
        self.next.show()

def main():
    gtk.main()
    return 0       

if __name__ == "__main__":
    PokerTempo()
    main()