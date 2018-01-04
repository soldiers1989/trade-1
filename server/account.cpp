#include "account.h"
BEGIN_SERVICE_NAMESPACE
//////////////////////////////////////////account class/////////////////////////////////////
int account::login(const std::string &ip, ushort port, const std::string &version, int deptid, std::string *error) {
	//initialize account's depends first
	int err = init(error);
	if (err != 0) {
		return -1;
	}

	//login to the trading server
	err = _trade->login(ip, port, version, deptid, _account.user, _account.user, _account.pwd, _account.pwd, error);
	if (err != 0) {
		return -1;
	}

	//set online state
	_account.online = true;

	return 0;
}

int account::query(trade::query::type category, trade::table &result, std::string *error) {
	return _trade->query(category, result, error);
}

int account::query(trade::query::type category, const std::string &start_date, const std::string &end_date, trade::table &result, std::string *error) {
	return _trade->query(category, start_date, end_date, result, error);
}
int account::send(trade::order::type category, trade::price::type type, const std::string &gddm, const std::string &zqdm, float price, int count, trade::table &result, std::string *error) {
	return _trade->send(category, type, gddm, zqdm, price, count, result, error);
}

int account::cancel(const std::string &exchangeid, const std::string &orderno, trade::table &result, std::string *error) {
	return _trade->cancel(exchangeid, orderno, result, error);
}

int account::logout() {
	//logout first
	_trade->logout();
	_account.online = true;

	//destroy account
	destroy();

	return 0;
}

int account::init(std::string *error) {
	if (_trade == 0) {
		_trade = trade::trade::create();
		return _trade->init(".", error);
	}
	return 0;
}

void account::destroy() {
	if (_trade != 0) {
		_trade->destroy();
		delete _trade;
		_trade = 0;
	}
}

//////////////////////////////////////////accounts class/////////////////////////////////////
int accounts::init(std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//create dao
	_dao = new accountsdao();

	//load all accounts from database
	std::vector<account_t> acnts;
	int err = _dao->get(acnts, error);
	if (err != 0)
		return -1;

	for (size_t i = 0; i < acnts.size(); i++) {
		_accounts.insert(std::pair<std::string, account*>(acnts[i].name, new account(acnts[i])));
	}

	return 0;
}

int accounts::add(const account_t &acnt, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//add account if not exist
	std::map<std::string, account*>::iterator iter = _accounts.find(acnt.name);
	if (iter != _accounts.end())
		return 0;
	return _dao->add(acnt, error);
}

int accounts::del(int id, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//first remove from account list
	

	//then remove from database
	return _dao->del(id, error);
}

int accounts::destroy() {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<std::string, account*>::iterator iter = _accounts.begin(), iterend = _accounts.end();
	while (iter != iterend) {
		delete iter->second;
		iter++;
	}
	_accounts.clear();

	if (_dao != 0) {
		delete _dao;
		_dao = 0;
	}
	return 0;
}


END_SERVICE_NAMESPACE
