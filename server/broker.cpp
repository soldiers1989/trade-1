#include "broker.h"
#include "cube\fd.h"
#include "cube\str.h"

#include "cppconn\exception.h"
#include "cppconn\resultset.h"
#include "cppconn\statement.h"
#include "cppconn\prepared_statement.h"

BEGIN_SERVICE_NAMESPACE

//////////////////////////////////////broker class////////////////////////////////////////////
int broker::init(std::string *error) {
	//create dao object
	_dao = new brokerdao();

	//load data from database
	int err = _dao->get(_broker.id, _depts, error);
	if (err != 0) {
		return -1;
	}

	err = _dao->get(_broker.id, server::type::trade, _trades, error);
	if (err != 0) {
		return -1;
	}

	err = _dao->get(_broker.id, server::type::quote, _quotes, error);
	if (err != 0) {
		return -1;
	}

	return 0;
}

int broker::select(server::type type, server &server, std::string *error) {
	return 0;
}

int broker::destroy() {
	if (_dao != 0) {
		delete _dao;
		_dao = 0;
	}
	return 0;
}

//////////////////////////////////////brokers class////////////////////////////////////////////
int brokers::init(std::string *error ) {
	std::lock_guard<std::mutex> lock(_mutex);
	//create dao
	_dao = new brokersdao();

	//load data from database
	std::vector<broker_t> brkrs;
	int err = _dao->get(brkrs, error);
	if (err != 0) {
		return -1;
	}

	for (size_t i = 0; i < brkrs.size(); i++) {
		broker *brkr = new broker(brkrs[i]);
		err = brkr->init(error);
		if (err != 0) {
			delete brkr;
			return -1;//process error later
		}
		_brokers.insert(std::pair<std::string, broker*>(brkr->brkr().code, brkr));
	}

	return 0;
}

int brokers::add(const broker_t &brkr, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<std::string, broker*>::iterator iter = _brokers.find(brkr.code);
	if (iter != _brokers.end()) {
		return 0; //broker exists
	}

	//insert new broker to database
	int err = _dao->add(brkr, error);
	if (err != 0) {
		return -1;
	}

	//get complete broker from database
	broker_t newbrkr;
	err = _dao->get(brkr.code, newbrkr, error);
	if (err != 0) {
		return -1;
	}

	//add new broker to brokers
	_brokers.insert(std::pair<std::string, broker*>(newbrkr.code, new broker(newbrkr)));

	return 0;
}

int brokers::select(const std::string &code, server::type type, server &server, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);

	std::map<std::string, broker*>::iterator iter = _brokers.find(code);
	if (iter != _brokers.end()) {
		return iter->second->select(type, server, error);
	} else {
		cube::throw_assign<brokers::error>(error, cube::str::format("broker %s not exist.", code.c_str()));
	}

	return -1;
}

int brokers::destroy() {
	std::lock_guard<std::mutex> lock(_mutex);
	
	//free all brokers
	std::map<std::string, broker*>::iterator iter = _brokers.begin(), iterend = _brokers.end();
	while (iter != iterend) {
		delete iter->second;
	}
	_brokers.clear();

	//free dao
	if (_dao != 0) {
		delete _dao;
		_dao = 0;
	}

	return 0;
}
END_SERVICE_NAMESPACE
