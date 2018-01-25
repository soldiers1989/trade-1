#include "broker.h"
#include "cube\fd.h"
#include "cube\str.h"

#include "cppconn\exception.h"
#include "cppconn\resultset.h"
#include "cppconn\statement.h"
#include "cppconn\prepared_statement.h"

BEGIN_SEC_NAMESPACE
//////////////////////////////////////brokers class////////////////////////////////////////////
int brokers::init(std::string *error ) {
	std::lock_guard<std::mutex> lock(_mutex);
	//create dao
	_dao = new brokersdao();

	//load data from database
	std::vector<broker> brkrs;
	int err = _dao->get(brkrs, error);
	if (err != 0) {
		return -1;
	}

	for (size_t i = 0; i < brkrs.size(); i++) {
		_brokers.insert(std::pair<std::string, broker>(brkrs[i].code, brkrs[i]));
	}

	return 0;
}

int brokers::add(const broker &brkr, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<std::string, broker>::iterator iter = _brokers.find(brkr.code);
	if (iter != _brokers.end()) {
		return 0; //broker exists
	}

	//insert new broker to database
	int err = _dao->add(brkr, error);
	if (err != 0) {
		return -1;
	}

	//get complete broker from database
	broker newbrkr;
	err = _dao->get(brkr.code, newbrkr, error);
	if (err != 0) {
		return -1;
	}

	//add new broker to brokers
	_brokers.insert(std::pair<std::string, broker>(newbrkr.code, newbrkr));

	return 0;
}

int brokers::select(const std::string &code, server::type type, server &server, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);

	std::map<std::string, broker>::iterator iter = _brokers.find(code);
	if (iter != _brokers.end()) {
		return iter->second.select(type, server, error);
	} else {
		cube::throw_assign<brokers::error>(error, cube::str::format("broker %s not exist.", code.c_str()));
	}

	return -1;
}

int brokers::destroy() {
	std::lock_guard<std::mutex> lock(_mutex);
	
	//clear brokers
	_brokers.clear();

	//free dao
	if (_dao != 0) {
		delete _dao;
		_dao = 0;
	}

	return 0;
}
END_SEC_NAMESPACE
