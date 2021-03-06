// test.cpp: 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "cube\str\print.h"
#include "tdx.h"
#include "tdx1.h"
#include "tdx2.h"
#include <string>
#include <sstream>
#include <iostream>
#include <regex>
#include <locale>

int test_trade();
int test_quote1();
int test_quote2();

int main(int argc, char* argv[]) {
	//test_crontab();
	//test_reactor();
	//test_timer();
	//test_trade();
	test_quote1();
	//test_quote2();
	return 0;
}

int test_trade() {
	trade::trade *ptrade = new trade::tdx();
	int err = ptrade->init(".");
	if (err != 0) {
		std::cout << "init trader failed." << std::endl;
		return -1;
	}

	trade::table result;
	std::string error;

	err = ptrade->login("119.167.224.7", 7708, "2.03", 0, "1300171903", "1300171903", "131268", "131268", &error);
	if (err != 0) {
		std::cout << "trader login failed, reason: " << error.c_str() << std::endl;
		return -1;
	}
	std::cout << "login success." << std::endl;

	result.clear();
	err = ptrade->query(trade::query::zj, result, &error);
	if (err != 0) {
		std::cout << "query data failed, reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	result.clear();
	err = ptrade->query(trade::query::gf, result, &error);
	if (err != 0) {
		std::cout << "query data failed, reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	result.clear();
	err = ptrade->query(trade::query::drwt, result, &error);
	if (err != 0) {
		std::cout << "query data failed, reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	result.clear();
	err = ptrade->query(trade::query::drcj, result, &error);
	if (err != 0) {
		std::cout << "query data failed, reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

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

int test_quote1() {
	quote::quote1 *quote = new quote::tdx1();

	quote::table result;
	std::string error;
	int err = quote->init(".", &error);
	if (err != 0) {
		std::cout << "init quote service failed. reason: " << error.c_str() << std::endl;
		return -1;
	}

	err = quote->connect("123.125.108.90", 7709, result, &error);
	if (err != 0) {
		std::cout << "connect to server failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	result.clear();
	err = quote->query_xdxr_data(quote::market::sz, "000725", result, &error);
	if (err != 0) {
		std::cout << "query deal data failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	int count = 0;
	err = quote->query_security_count(quote::market::sh, count, &error);
	if (err != 0) {
		std::cout << "query security count failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	std::cout << "security count in shanghai is: " << count << std::endl;

	result.clear();
	err = quote->query_current_deal_data(quote::market::sz, "000725", 0, count, result, &error);
	if (err != 0) {
		std::cout << "query deal data failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	result.clear();
	err = quote->query_history_deal_data(quote::market::sz, "000725", "20180402",0, count, result, &error);
	if (err != 0) {
		std::cout << "query deal data failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	result.clear();
	err = quote->query_current_quote_data(quote::market::sz, "000725", result, &error);
	if (err != 0) {
		std::cout << "query quote data failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	err = quote->query_current_time_data(quote::market::sz, "000725", result, &error);
	if (err != 0) {
		std::cout << "query time data failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	err = quote->query_history_time_data(quote::market::sz, "000725", "20180402", result, &error);
	if (err != 0) {
		std::cout << "query time data failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	err = quote->query_f10_category(quote::market::sz, "000725", result, &error);
	if (err != 0) {
		std::cout << "query f10 failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	err = quote->query_f10_content(quote::market::sz, "000725", "000725.B01", 0, 1024*1024,result, &error);
	if (err != 0) {
		std::cout << "query f10 failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	err = quote->query_security_list(quote::market::sz, 0, count, result, &error);
	if (err != 0) {
		std::cout << "query seclist data failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	err = quote->query_security_kline(quote::kline::min1, quote::market::sz, "000725", 0, count, result, &error);
	if (err != 0) {
		std::cout << "query kline data failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	return 0;
}

int test_quote2() {
	quote::quote2 *quote = new quote::tdx2();

	quote::table result;
	std::string error;
	int err = quote->init(".", &error);
	if (err != 0) {
		std::cout << "init quote service failed. reason: " << error.c_str() << std::endl;
		return -1;
	}

	err = quote->connect("61.152.107.141", 7727, result, &error);
	if (err != 0) {
		std::cout << "connect to server failed. reason: " << error.c_str() << std::endl;
		return -1;
	}

	int count = 0;
	err = quote->query_security_count(quote::market::sh, count, &error);
	if (err != 0) {
		std::cout << "query security count failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	std::cout << "security count in shanghai is: " << count << std::endl;

	result.clear();
	err = quote->query_current_deal_data(quote::market::sz, "000100", 0, count, result, &error);
	if (err != 0) {
		std::cout << "query deal data failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	result.clear();
	err = quote->query_current_quote_data(quote::market::sz, "000100", result, &error);
	if (err != 0) {
		std::cout << "query quote data failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	return 0;
}