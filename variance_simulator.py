from random import normalvariate
import matplotlib.pyplot as plt
from pylab import * 

rcParams['figure.figsize'] = 50, 10

def profit_per_hand(winrate, stdev):
    winrate_per_hand = winrate/100.0
    stdev_per_hand = stdev/100.0
    return normalvariate(winrate_per_hand,stdev_per_hand)

def simulation(number_of_hands,runs,winrate,stdev):

    hand_factor = number_of_hands/1000.0

    # Change scale to reflect high number of hands (too expensive to compute)
    if number_of_hands > 1000:
        number_of_hands = 1000
        tick_locs = [0,200,500,750,1000]
        tick_lbls = [x*hand_factor for x in tick_locs]
        plt.xticks(tick_locs, tick_lbls)

    results_per_hand = []
    for run in range(runs):
        results_per_hand.append([profit_per_hand(winrate,stdev)*hand_factor for hand in xrange(1,number_of_hands+1)])

    for profit in results_per_hand:
        plt.plot([sum(profit[:hand]) for hand in xrange(0,number_of_hands+1)])

    # Plot the cumulative average of each run
    avg = [sum(col)/len(col) for col in zip(*results_per_hand)]
    average, = plt.plot([sum(avg[:hand]) for hand in xrange(0,number_of_hands+1)],linewidth=4)
    l1 = plt.legend([average], ["Average"], loc=1)
    plt.gca().add_artist(l1)


    # Gridlines
    grid(b=True, which='major', color='black', linestyle='-')
    grid(b=True, which='minor', color='black', linestyle='--')

    # Plot graph, zero profit line, labels
    plt.axhline(linewidth=4,color='black')
    plt.title('Simulating Results of Poker Player with %d bb/100 winrate and %d bb/100 standard deviation'\
        % (winrate,stdev))
    plt.ylabel('Profit (bb)')
    plt.xlabel('Number of Hands')
    plt.show()

number_of_hands = int(raw_input("How many hands do you want to simulate? "))
winrate = float(raw_input("What is the winrate in bb/100 you want to simulate? " ))
stdev = float(raw_input("What is the standard deviation in bb/100 you want to simulate? "))

simulation(number_of_hands,30,winrate,stdev)

