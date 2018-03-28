#include "trade\tdx.h"
#include "cube\safe.h"
#include "cube\log\log.h"
#include "trades\config.h"
#include "trades\account.h"
BEGIN_TRADES_NAMESPACE
accounts *accounts::_instance = 0;

accounts *accounts::instance() {
	if (_instance == 0) {
		_instance = new accounts();
	}

	return _instance;
}

int accounts::login(const std::string &laccount, const std::string taccount, const std::string tpwd, const std::string cpwd, const std::string &ip, ushort port, int dept, const std::string &version, std::string *error) {
	cube::log::info("account %s login...", laccount.c_str());
	std::lock_guard<std::mutex> lck(_mutex);
	//account has login
	if (_accounts.find(laccount) != _accounts.end()) {
		cube::log::info("account %s has already login.", laccount.c_str());
		return 0;
	}

	std::string errmsg("");
	//account create
	trade::trade *acnt = new trade::tdx();
	if (acnt->init(config::wdir, &errmsg) != 0) {
		cube::log::error("account %s login failed, error: %s", laccount.c_str(), errmsg.c_str());
		cube::safe_assign<std::string>(error, errmsg);
		return -1;
	}

	//account login
	if (acnt->login(ip, port, version, dept, laccount, taccount, tpwd, cpwd, &errmsg) != 0) {
		cube::safe_assign<std::string>(error, errmsg);
		cube::log::error("account %s login failed, error: %s", laccount.c_str(), errmsg.c_str());
		return -1;
	}

	//add account
	_accounts.insert(std::pair<std::string, trade::trade*>(laccount, acnt));

	cube::log::info("account %s login success.", laccount.c_str());
	return 0;

}

int accounts::quote(const std::string &account, const std::string &code, trade::table &result, std::string *error) {
	cube::log::info("query quote data with code %s from account %s...", code.c_str(), account.c_str());
	std::lock_guard<std::mutex> lck(_mutex);
	std::map<std::string, trade::trade*>::iterator iter = _accounts.find(account);
	//find account
	if (iter == _accounts.end()) {
		cube::safe_assign<std::string>(error, "account not exist.");
		cube::log::error("query quote data with code %s from account %s failed, error: account not exist", code.c_str(), account.c_str());
		return -1;
	}

	std::string errmsg("");
	//query data
	if (iter->second->quote(code, result, &errmsg) != 0) {
		cube::safe_assign<std::string>(error, errmsg);
		cube::log::error("query quote data with code %s from account %s failed, error: %s", code.c_str(), account.c_str(), errmsg.c_str());
		return -1;
	}

	cube::log::info("query quote data with code %s from account %s success.", code.c_str(), account.c_str());
	return 0;
}

int accounts::query(const std::string &account, int category, trade::table &result, std::string *error) {
	cube::log::info("query account %s data with category %d ...", account.c_str(), category);
	std::lock_guard<std::mutex> lck(_mutex);
	std::map<std::string, trade::trade*>::iterator iter = _accounts.find(account);
	//find account
	if (iter == _accounts.end()) {
		cube::safe_assign<std::string>(error, "account not exist.");
		cube::log::error("query account %s data with category %d failed, error: account not exist", account.c_str(), category);
		return -1;
	}

	std::string errmsg("");
	//query data
	if (iter->second->query((trade::query::type)category, result, &errmsg) != 0) {
		cube::safe_assign<std::string>(error, errmsg);
		cube::log::error("query account %s data with category %d failed, error: %s", account.c_str(), category, errmsg.c_str());
		return -1;
	}

	cube::log::info("query account %s data with category %d success.", account.c_str(), category);
	return 0;
}

int accounts::query(const std::string &account, int category, const std::string &start_date, const std::string &end_date, trade::table &result, std::string *error) {
	cube::log::info("query account %s history data from %s~%s with category %d ...", account.c_str(), start_date.c_str(), end_date.c_str(), category);
	std::lock_guard<std::mutex> lck(_mutex);
	std::map<std::string, trade::trade*>::iterator iter = _accounts.find(account);
	//find account
	if (iter == _accounts.end()) {
		cube::safe_assign<std::string>(error, "account not exist.");
		cube::log::error("query account %s history data from %s~%s with category %d failed, error: account not exist", account.c_str(), start_date.c_str(), end_date.c_str(), category);
		return -1;
	}

	std::string errmsg("");
	//query data
	if (iter->second->query((trade::query::type)category, start_date, end_date, result, &errmsg) != 0) {
		cube::safe_assign<std::string>(error, errmsg);
		cube::log::error("query account %s history data from %s~%s with category %d failed, error: %s", account.c_str(), start_date.c_str(), end_date.c_str(), category, errmsg.c_str());
		return -1;
	}

	cube::log::info("query account %s history data from %s~%s with category %d success.", account.c_str(), start_date.c_str(), end_date.c_str(), category);
	return 0;
}

int accounts::order(const std::string &account, int otype, int ptype, const std::string &gddm, const std::string &zqdm, float price, int count, trade::table &result, std::string *error) {
	cube::log::info("order <otype:%d, ptype:%d, gddm:%s, zqdm:%s, price: %.2f, count: %d> from account %s...", otype, ptype, gddm.c_str(), zqdm.c_str(), price, count, account.c_str());
	std::lock_guard<std::mutex> lck(_mutex);
	std::map<std::string, trade::trade*>::iterator iter = _accounts.find(account);
	//find account
	if (iter == _accounts.end()) {
		cube::safe_assign<std::string>(error, "account not exist.");
		cube::log::error("order <otype:%d, ptype:%d, gddm:%s, zqdm:%s, price: %.2f, count: %d> from account %s failed, error: account not exist", otype, ptype, gddm.c_str(), zqdm.c_str(), price, count, account.c_str());
		return -1;
	}

	std::string errmsg("");
	//send order
	if (iter->second->send((trade::order::type)otype, (trade::price::type)ptype, gddm, zqdm, price, count, result, &errmsg) != 0) {
		cube::safe_assign<std::string>(error, errmsg);
		cube::log::info("order <otype:%d, ptype:%d, gddm:%s, zqdm:%s, price: %.2f, count: %d> from account %s failed. error: %s", otype, ptype, gddm.c_str(), zqdm.c_str(), price, count, account.c_str(), errmsg.c_str());
		return -1;
	}

	cube::log::info("order <otype:%d, ptype:%d, gddm:%s, zqdm:%s, price: %.2f, count: %d> from account %s success", otype, ptype, gddm.c_str(), zqdm.c_str(), price, count, account.c_str());
	return 0;
}

int accounts::cancel(const std::string &account, const std::string &seid, const std::string &orderno, trade::table &result, std::string *error) {
	cube::log::info("cancel <seid:%s, orderno:%s from account %s...", seid.c_str(), orderno.c_str(), account.c_str());
	std::lock_guard<std::mutex> lck(_mutex);
	std::map<std::string, trade::trade*>::iterator iter = _accounts.find(account);
	//find account
	if (iter == _accounts.end()) {
		cube::safe_assign<std::string>(error, "account not exist.");
		cube::log::info("cancel <seid:%s, orderno:%s from account %s failed, error: account not exist", seid.c_str(), orderno.c_str(), account.c_str());
		return -1;
	}

	std::string errmsg("");
	//cancel order
	if (iter->second->cancel(seid, orderno, result, &errmsg) != 0) {
		cube::safe_assign<std::string>(error, errmsg);
		cube::log::info("cancel <seid:%s, orderno:%s from account %s failed, error: %s", seid.c_str(), orderno.c_str(), account.c_str(), errmsg.c_str());
		return -1;
	}

	cube::log::info("cancel <seid:%s, orderno:%s from account %s success", seid.c_str(), orderno.c_str(), account.c_str());
	return 0;
}

int accounts::logout(const std::string &account, std::string *error) {
	std::lock_guard<std::mutex> lck(_mutex);
	std::map<std::string, trade::trade*>::iterator iter = _accounts.find(account);
	//account has login
	if (iter == _accounts.end()) {
		cube::safe_assign<std::string>(error, "account not exist.");
		cube::log::error("account %s logout failed, error: account not exist.", account.c_str());
		return -1;
	}

	//logout
	iter->second->logout();

	//destroy
	iter->second->destroy();

	//delete
	delete iter->second;

	//remove
	_accounts.erase(iter);

	return 0;
}
END_TRADES_NAMESPACE
