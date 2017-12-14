// server.cpp: 定义控制台应用程序的入口点。
//
#include "cube\fd.h"
#include "db.h"
#include "dbinit.h"
#include "account.h"

int main()
{
	svr::db mydb;
	mydb.connect("10.0.0.8", "test", "test");

	std::string error;
	int err = svr::dbinit::init("trade.sql", "trade", &mydb, &error);
	if (err != 0) {
		std::cout << "dbinit: " << error.c_str() << std::endl;
	} else {
		std::cout << "dbinit: success." << std::endl;
	}

	svr::dao::setdb(&mydb);

	svr::brokers brokers;
	err = brokers.init(&error);
	if (err != 0) {
		std::cout << "broker init: " << error.c_str() << std::endl;
	} else {
		std::cout << "broker init: success." << std::endl;
	}
	
	err = brokers.add(svr::broker_t("htzq", "haitongzhengquan", "6.09", false), &error);
	if (err != 0) {
		std::cout << "broker add: " << error.c_str() << std::endl;
	} else {
		std::cout << "broker add: success." << std::endl;
	}

	svr::accounts accounts(&brokers);
	err = accounts.init(&error);
	if (err != 0) {
		std::cout << "account init: " << error.c_str() << std::endl;
	} else {
		std::cout << "account init: success." << std::endl;
	}

	err = accounts.add(svr::account_t(1, 1, "a", "a", "a", 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, false), &error);
	if (err != 0) {
		std::cout << "account add: " << error.c_str() << std::endl;
	} else {
		std::cout << "account add: success." << std::endl;
	}

	/*cube::server<svr::sessionapi> server;
	server.start(80);

	while (true) {
		::Sleep(1000);
	}*/

    return 0;
}

