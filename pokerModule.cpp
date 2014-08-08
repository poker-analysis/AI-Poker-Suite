// Steps:
// Create deck
// Create a hold em hand evaluator
// Create hand comparison (preflop) function
// Write bindings to Python via Swig

#include <iostream>
#include <string>
#include <algorithm>
#include <sstream>

using namespace std;

char suits[] = {'c','h','d','s'};
char values[] = {'2','3','4','5','6','7','8','9','T','J','Q','K','A'};

string flushsuit(string totalboard)
{	
	// Suit Counter
	for (int i=0; i<4;i++){
		size_t suit = count(totalboard.begin(), totalboard.end(), suits[i]);
		if (suit>=5){
			stringstream ss; string s; char c = suits[i];
			ss << c; ss >> s;
			return s;
		}
	}
	return "";	
}

string holdem_evaluate(string totalboard)
{
	// Flush
	if (flushsuit(totalboard) != ""){
		return "Flush";
	}
	else {
		return "";
	}
}

int main()
{
	cout << holdem_evaluate("AhKhQhThJh7h3c") << "\n";
}