#include<string>
#include<sstream>
#include<iostream>
using namespace std;

int main(int argc, char** argv)
{
	istringstream is(argv[1]);
	int i;
	is >> i;
	cout << i;
}
