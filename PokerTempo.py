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

class PokerTempo:
    
    def callback(self, widget, data=None):
        print "Hello again - %s was pressed" % data

    def delete_event(self, widget, event, data=None):
        gtk.main_quit()
        return False

    def __init__(self):
        def holdem_tempo():
            label = gtk.Label('Hero')
            table.attach(label,0,1,0,1)
            label.show()

            label = gtk.Label('Villain')
            table.attach(label,1,2,0,1)
            label.show()

        self.window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.window.set_title("Table")

        self.window.connect("delete_event", self.delete_event)

        self.window.set_border_width(20)
        table = gtk.Table(5, 5, True)

        self.window.add(table)
        
        table.show()
        self.window.show()

def main():
    gtk.main()
    return 0       

if __name__ == "__main__":
    PokerTempo()
    main()