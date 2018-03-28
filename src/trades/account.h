#pragma once
#include <map>
#include <mutex>
#include "trade\trade.h"
#include "trades\stdtrds.h"
BEGIN_TRADES_NAMESPACE
class accounts {
public:
	virtual ~accounts() {}
	static accounts *instance();

	int login(const std::string &laccount, const std::string taccount, const std::string tpwd, const std::string cpwd, const std::string &ip, ushort port, int dept, const std::string &version, std::string *error);
	
	int quote(const std::string &account, const std::string &code, trade::table &result, std::string *error);
	
	int query(const std::string &account, int category, trade::table &result, std::string *error);

	int query(const std::string &account, int category, const std::string &start_date, const std::string &end_date, trade::table &result, std::string *error);

	int order(const std::string &account, int otype, int ptype, const std::string &gddm, const std::string &zqdm, float price, int count, trade::table &result, std::string *error);

	int cancel(const std::string &account, const std::string &seid, const std::string &orderno, trade::table &result, std::string *error);

	int logout(const std::string &account, std::string *error);
private:
	accounts() {}

private:
	//singleton instance of accounts
	static accounts *_instance;
	//mutex for accounts
	std::mutex _mutex;
	//current login accounts
	std::map<std::string, trade::trade*> _accounts;
};
END_TRADES_NAMESPACE
