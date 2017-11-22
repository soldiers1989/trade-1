// test.cpp: 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "tdx1.h"
#include "tdx.h"
#include <string>
#include <iostream>

int main(int argc, char* argv[]) {
	
	/*quote::quote1 *quote = new quote::tdx1();

	quote::table_t result;
	std::string error;
	int err = quote->init(&error);
	if (err != 0) {
		std::cout << "init quote service failed. reason: " << error.c_str() << std::endl;
		return -1;
	}

	err = quote->connect("202.130.235.189", 7709, result, error);
	if (err != 0) {
		std::cout << "connect to server failed. reason: " << error.c_str() << std::endl;
		return -1;
	}

	int count = 0;
	err = quote->query_security_count(quote::market_t::sh, count, error);
	if (err != 0) {
		std::cout << "query security count failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	std::cout << "security count in shanghai is: " << count << std::endl;
	*/

	trade::trade *ptrade = new trade::tdx();
	int err = ptrade->init("1300171903");
	if (err != 0) {
		std::cout << "init trader failed." << std::endl;
		return -1;
	}

	trade::table_t result;
	std::string error("");

	err = ptrade->login("119.167.224.7", 7708, "2.03", 0, "1300171903", "1300171903", "456300", "456300", error);
	if (err != 0) {
		std::cout << "trader login failed, reason: "<<error.c_str() << std::endl;
		return -1;
	}

	result.clear();
	err = ptrade->query(trade::ccategory_t::zj, result, error);
	if (err != 0) {
		std::cout << "query data failed, reason: " << error.c_str() << std::endl;
		return -1;
	}

	result.clear();
	err = ptrade->quote("000100", result, error);
	if (err != 0) {
		std::cout << "get quote failed, reason: " << error.c_str() << std::endl;
		return -1;
	}

	err = ptrade->logout();
	if (err != 0) {
		std::cout << "trader logout failed." << std::endl;
		return -1;
	}

	err = ptrade->destroy();
	if (err != 0) {
		std::cout << "destroy trader failed." << std::endl;
		return -1;
	}

	return 0;
}
