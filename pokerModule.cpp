// Steps:
// Create deck
// Create a hold em hand evaluator
// Create hand comparison (preflop) function
// Write bindings to Python via Swig

#include <iostream>
#include <string>
#include <algorithm>
#include <sstream>
#include <vector>

using namespace std;

string suits = "cdhs";
string values = "23456789TJQKA";

char flushSuit(string totalboard)
{	
	// Suit Retrieval
	for (int i=0; i<4;i++){
		size_t suit = count(totalboard.begin(), totalboard.end(), suits[i]);
		if (suit >= 5){
			return suits[i];
		}
	}
	return ' ';
}

void flushValues(string totalboard)
{
	vector<char> v;
	char flSuit = flushSuit(totalboard);
	// Grab Flush Cards

	if (flSuit != ' '){
		for (int x = 0; x<14; x++){
			if (totalboard[x+1] == flSuit){
				v.push_back(totalboard[x]);
			}
		}
	}
	for (int i=0;i<v.size();i++){
		cout << v.at(i);
	}
}

int holdemEvaluate(string totalboard)
{
	// Flush
	if (flushSuit(totalboard) != ' '){
		return 6;
	}
	return 0;
}

int main()
{
	cout << holdemEvaluate("Ah2h3h4h5h6d7h");
}
