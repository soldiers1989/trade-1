// test.cpp: 定义控制台应用程序的入口点。
//

#include "stdafx.h"
#include "tdx.h"
#include "tdx1.h"
#include "tdx2.h"
#include "cube\str.h"
#include "cube\ini.h"
#include "cube\tm.h"
#include "cube\log.h"
#include "cube\cc.h"
#include "cube\http.h"
#include "cube\net.h"
#include <string>
#include <sstream>
#include <iostream>

int test_reactor();
int test_crontab();
int test_timer();
int test_trade();
int test_quote1();
int test_quote2();

int main(int argc, char* argv[]) {
	const char *s = "ab";
	char buf[256] = { 0 };

	std::stringstream ss(std::ios_base::in | std::ios_base::out);
	ss.write(s, strlen(s));
	ss.getline(buf, 256);
	if (ss.eof()) {
		ss.clear();
		//int rdsz = strlen(buf);
		//ss.seekg(-rdsz, std::ios::end);
	}

	ss.write("\n", strlen("\n"));
	ss.getline(buf, 256);

	const char *s1 = "cd\n";
	ss.write(s1, strlen(s1));
	ss.getline(buf, 256);

	const char *s2 = "ef\n";
	ss.write(s2, strlen(s2));
	ss.getline(buf, 256);

	return 0;
	//const char *res = cube::str::strstr(s, (int)strlen(s), "cd");
	//std::vector<std::string> res = cube::str::split(s, "cd");
	//cube::http::params *a = cube::http::params::parse("a=1 & b=2 & c=%ad%12 & d=&e&q");

	/*while (true) {
		char url[1024] = { 0 };
		std::cout << "input url" << std::endl;
		std::cin >> url;

		cube::http::uri u;
		u.parse(url, strlen(url));

		std::cout << u.description().c_str() << std::endl;
	}*/

	
	//test_crontab();
	//test_reactor();
	//test_timer();
	//test_trade();
	//test_quote1();
	//test_quote2();
}

class mytask : public cube::task {
public:
	mytask(int id) : _id(id) {

	}
	void run() {
		cube::log::info("run task, id: %d", _id);
		//std::this_thread::sleep_for(std::chrono::milliseconds(10));
	}

private:
	int _id;
};

int test_reactor() {
	for (int i = 0; i <100000; i++)
		cube::reactor::default::react(new mytask(i));
	std::this_thread::sleep_for(std::chrono::seconds(300));
	return 0;
}

int test_crontab() {
	//for(int i=0; i<100; i++)
	//	cube::crontab::default::setup(new mytask(i), -1, -1, -1, -1, -1);

	for(int i=0; i<60; i++)
		cube::crontab::default::setup(new mytask(i), i, -1, -1, -1, -1);

	std::this_thread::sleep_for(std::chrono::seconds(3600));
	return 0;
}

int test_timer() {
	for (int i = 0; i < 10; i++) {
		int id = cube::timer::default::setup(1000, 500, new mytask(i));
		cube::log::info("start timer task : %d", id);
	}
	
	cube::timer::default::setup(3000, new mytask(11));

	std::this_thread::sleep_for(std::chrono::seconds(30));
	
	for (int i = 0; i < 10; i++) {
		cube::timer::default::cancel(i);
	}

	std::this_thread::sleep_for(std::chrono::seconds(300));
	
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
	err = quote->query_current_quote_data(quote::market::sz, "601318", result, &error);
	if (err != 0) {
		std::cout << "query quote data failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	err = quote->query_current_time_data(quote::market::sz, "000100", result, &error);
	if (err != 0) {
		std::cout << "query time data failed. reason: " << error.c_str() << std::endl;
		return -1;
	}
	cube::str::print(result);

	err = quote->query_f10_category(quote::market::sz, "000100", result, &error);
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

	err = quote->query_security_kline(quote::kline::min1, quote::market::sz, "000100", 0, count, result, &error);
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