// test.cpp: 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "tdx.h"
#include <iostream>

int main(int argc, char* argv[]) {
	trader *ptrader = new tdx("92000053", "188188");
	//trader *ptrader = new tdx("12769301", "201710");
	//trader *ptrader = new tdx("1300171903", "456300");
	int err = ptrader->init();
	if (err != 0) {
		std::cout << "init trader failed." << std::endl;
		return -1;
	}

	err = ptrader->login();
	if (err != 0) {
		std::cout << "trader login failed." << std::endl;
		return -1;
	}

	ptrader->query_money();

	err = ptrader->logout();
	if (err != 0) {
		std::cout << "trader logout failed." << std::endl;
		return -1;
	}

	err = ptrader->destroy();
	if (err != 0) {
		std::cout << "destroy trader failed." << std::endl;
		return -1;
	}

	return 0;
}

/*
int main(int argc, char* argv[]) {
	const char* content = "abcdabcdabde";
	cube::util::find_repeats(content, strlen(content));

	return 0;

	load("tdx.dll", "1300171903");
	open();
	
	char error[256] = { 0 }, result[65536] = {0};
	//int client_id = login("202.130.235.187", 7708, "7.10", 1, "29633865", "29633865", "456789", "", error);
	int client_id = login("119.167.224.7", 7708, "2.03", 0, "1300171903", "1300171903", "456300", "456300", error);
	query_data(client_id, 5, result, error);//查询资金
	std::cout << result << std::endl;
	std::cout << error << std::endl;

	get_quote(client_id, "000100", result, error);
	std::cout << result << std::endl;

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
	std::cout << results[0] << std::endl;
	std::cout << results[1] << std::endl;

	int wait;
	std::cin >> wait;
}
*/