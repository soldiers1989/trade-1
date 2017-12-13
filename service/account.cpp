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
	return _trade->login(ip, port, version, deptid, _user, _user, _pwd, _pwd, error);
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

	//load all accounts
	int err = _dao->select(_accounts, error);
	if (err != 0)
		return -1;

	return 0;
}

int accounts::destroy() {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<std::string, account*>::iterator iter = _accounts.begin(), iterend = _accounts.end();
	while (iter != iterend) {
		delete iter->second;
		iter++;
	}
	_accounts.clear();

	return 0;
}

//////////////////////////////////////////accountdao class/////////////////////////////////////
int accountsdao::select(std::map<std::string, account*> &accounts, std::string *error) {
	return 0;
}

int accountsdao::insert(const account &account, std::string *error) {
	return 0;
}
END_SERVICE_NAMESPACE
