#include "model.h"
#include "cube\str.h"
BEGIN_SEC_NAMESPACE
//////////////////////////////////////////manager class/////////////////////////////////////
int manager::login(const std::string &pwd, std::string *error) {
	if (disable) {
		cube::safe_assign<std::string>(error, "user has disabled.");
		return -1;
	}

	if (pwd != pwd) {
		cube::safe_assign<std::string>(error, "password is incorrect.");
		return -1;
	}

	token = cube::str::random(16);
	online = true;

	return 0;
}

void manager::logout() {
	token = "";
	online = false;
}

//////////////////////////////////////////account class/////////////////////////////////////
int account::login(const std::string &ip, ushort port, const std::string &version, int deptid, std::string *error) {
	//initialize account's depends first
	if (_trade == 0) {
		_trade = trade::trade::create();
		if( _trade->init(".", error) != 0)
			return -1;
	}

	//login to the trading server
	int err = _trade->login(ip, port, version, deptid, user, user, pwd, pwd, error);
	if (err != 0) {
		return -1;
	}

	//set online state
	online = true;

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
	
	//set online status
	online = true;

	//destroy trade module
	if (_trade != 0) {
		_trade->destroy();
		delete _trade;
		_trade = 0;
	}

	return 0;
}

//////////////////////////////////////broker class////////////////////////////////////////////

int broker::select(server::type type, server &server, std::string *error) {
	return 0;
}

END_SEC_NAMESPACE
