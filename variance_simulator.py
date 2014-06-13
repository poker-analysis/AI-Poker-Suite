from random import normalvariate
import matplotlib.pyplot as plt

def profit_per_hand(winrate, stdev):
	winrate_per_hand = winrate/100.0
	stdev_per_hand = stdev/100.0
	return normalvariate(winrate_per_hand,stdev_per_hand)

def simulation(number_of_hands,runs,winrate,stdev):
	results_per_hand = []
	results_per_run = []

	for run in range(runs):
		results_per_hand.append([profit_per_hand(winrate,stdev) for hand in xrange(1,number_of_hands)])

	for profit in results_per_hand:
		results_per_run.append([sum(profit[:hand]) for hand in xrange(1,number_of_hands)])
	
	for run in results_per_run:
		plt.plot(run)

	plt.title('Variance Simulation')
	plt.ylabel('Profit')
	plt.xlabel('Number of Hands')
	plt.show()

number_of_hands = int(raw_input("How many hands do you want to simulate? "))
runs = int(raw_input("How many runs do you want to simulate? "))
winrate = float(raw_input("What is the winrate in bb/100 you want to simulate? " ))
stdev = float(raw_input("What is the standard deviation in bb/100 you want to simulate? "))

simulation(number_of_hands,runs,winrate,stdev)