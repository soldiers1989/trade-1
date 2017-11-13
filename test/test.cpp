// test.cpp: 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "trade.h"
#include <iostream>
using namespace std;


int main(int argc, char* argv[]) {
	load("tdx.dll", "1300171903");
	open();
	
	char error[256] = { 0 }, result[65536] = {0};
	//int client_id = login("202.130.235.187", 7708, "7.10", 1, "29633865", "29633865", "456789", "", error);
	int client_id = login("119.167.224.7", 7708, "2.03", 0, "1300171903", "1300171903", "456300", "456300", error);
	query_data(client_id, 5, result, error);//查询资金
	cout << result << endl;
	cout << error << endl;

	get_quote(client_id, "000100", result, error);
	cout << result << endl;

	char *codes[2] = { "000100", "000001" };

	char *results[2] = { 0, 0 };
	results[0] = new char[1024];
	results[1] = new char[1024];
	memset(results[0], 0, 1024);
	memset(results[1], 0, 1024);

	char *errors[2] = { 0, 0 };
	errors[0] = new char[1024];
	errors[1] = new char[1024];
	memset(errors[0], 0, 1024);
	memset(errors[1], 0, 1024);

	get_quotes(client_id, codes, 2, results, errors);
	cout << results[0] << endl;
	cout << results[1] << endl;

	int wait;
	cin >> wait;
}
