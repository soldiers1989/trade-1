/*
*	account - account module for security account
*/
#pragma once
#include "stdsvr.h"
#include "db.h"
#include "broker.h"
#include "trade\tdx.h"

#include <mutex>

BEGIN_SERVICE_NAMESPACE
class accountsdao;

//account's fee property
class fee_t {
public:
	fee_t() {}
	fee_t(float cfrate, float cflimit, float bfrate, float sfrate) : cfrate(cfrate), cflimit(cflimit), bfrate(bfrate), sfrate(sfrate) {}
	~fee_t() {}

	//commission fee rate
	float cfrate;
	//commission fee lower limit
	float cflimit;
	//buy in fee rate
	float bfrate;
	//sell out fee rate
	float sfrate;
};

//account's money property
class money_t {
public:
	money_t() {}
	money_t(float smoney, float lmoney) : smoney(smoney), lmoney(lmoney) {}
	~money_t() {}

	//start money
	float smoney;
	//left money
	float lmoney;
};

//account property class
class account_t {
public:
	account_t() {}
	account_t(const account_t &acnt) : 
		id(acnt.id), broker(acnt.broker), admin(acnt.admin), name(acnt.name), user(acnt.user), pwd(acnt.pwd), 
		smoney(acnt.smoney), lmoney(acnt.smoney), cfrate(acnt.cfrate), cflimit(acnt.cflimit), bfrate(acnt.bfrate), 
		sfrate(acnt.sfrate), disable(acnt.disable), ctime(acnt.ctime), online(acnt.online) {}

	account_t(int broker, int admin, const std::string &name, const std::string &user, const std::string &pwd, float smoney, float lmoney, float cfrate, float cflimit, float bfrate, float sfrate, bool disable) : 
		id(-1), broker(broker), admin(admin), name(name), user(user), pwd(pwd), smoney(smoney), lmoney(lmoney), cfrate(cfrate), cflimit(cflimit), bfrate(bfrate), sfrate(sfrate), disable(disable), ctime(0), online(false) {}

	account_t(int id, int broker, const std::string &name, const std::string &user, const std::string &pwd, float smoney, float lmoney, float cfrate, float cflimit, float bfrate, float sfrate, bool disable, uint ctime) :
		id(id), broker(broker), name(name), user(user), pwd(pwd), smoney(smoney), lmoney(lmoney), cfrate(cfrate), cflimit(cflimit), bfrate(bfrate), sfrate(sfrate), disable(disable), ctime(ctime), online(false) {}
	
	~account_t() {}

	//acccount id
	int id;
	//broker id
	int broker;
	//admin id
	int admin;
	//account name
	std::string name;
	//trade account
	std::string user;
	//trade account password
	std::string pwd;
	//start money
	float smoney;
	//left money
	float lmoney;
	//commission fee rate
	float cfrate;
	//commission fee lower limit
	float cflimit;
	//buy in fee rate
	float bfrate;
	//sell out fee rate
	float sfrate;
	//disable status
	bool disable;
	//account create time
	uint ctime;
	//online status
	bool online;
};

//security account class
class account {
public:
	account(const account_t &acnt):  _account(acnt), _trade(0) {}
	~account() {}

	/*
	*	login to trading server
	*@param ip: in, remote trading server ip
	*@param port: in, remote trading server port
	*@param version: in, version of client
	*@param deptid: in, department of account belongs to
	*@param error: out, error message when login failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	int login(const std::string &ip, ushort port, const std::string &version, int deptid, std::string *error = 0);

	/*
	*	query current trading data of account by specified data category
	*@param category: in, data category
	*@param result: out, query result
	*@param error: out, error message when query failed
	*@return:
	*	0 for success, otherwise <0
	*/
	int query(trade::query::type category, trade::table &result, std::string *error = 0);


	/*
	*	query history trading data of accounts by specified data categories
	*@param category: in, data category
	*@param results: out, query results
	*@param errors: out, error messages when query failed
	*@return:
	*	0 for success, otherwise <0
	*/
	int query(trade::query::type category, const std::string &start_date, const std::string &end_date, trade::table &result, std::string *error = 0);


	/*
	*	send delegate order to remote server
	*@param category: in, order category
	*@param type: in, delegate price type
	*@param gddm: in, order's shareholder code
	*@param zqdm: in, order's stock code
	*@param price: in, delegate price
	*@param count: in, delegate count
	*@param result: out, send order result
	*@param error: out, error message when send order failed
	*@return:
	*	0 for success, otherwise <0
	*/
	int send(trade::order::type category, trade::price::type type, const std::string &gddm, const std::string &zqdm, float price, int count, trade::table &result, std::string *error = 0);


	/*
	*	cancel order by specified order number
	*@param exchange_id: in, exchange id of the order sent
	*@param order_no: in, order number want to cancel
	*@param result: out, cancel result
	*@param error, out, error message when cancel order failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	int cancel(const std::string &exchangeid, const std::string &orderno, trade::table &result, std::string *error = 0);

	/*
	*	logout from trading server
	*@return:
	*	always 0
	*/
	int logout();

public:
	/*
	*	get account information
	*/
	const account_t &acnt() { return _account; }

private:
	/*
	*	initialize account's depend objects
	*/
	int init(std::string *error = 0);

	/*
	*	destroy account's depend objects
	*/
	void destroy();

private:
	//account property
	account_t _account;

	//trade channel object
	trade::trade *_trade;
};

//service accounts class
class accounts {
public:
	accounts(brokers *brokers) : _brokers(brokers) {}
	~accounts() {}

	/*
	*	initialize accounts module
	*@param error: out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int init(std::string *error = 0);

	/*
	*	add new account
	*@param acnt: in, new account
	*@param error: out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int add(const account_t &acnt, std::string *error = 0);

	/*
	*	destroy account module
	*/
	int destroy();

private:
	//accounts managed
	std::map<std::string, account*> _accounts;
	//mutex for accounts
	std::mutex _mutex;

	//brokers supported
	brokers *_brokers;

	//database access
	accountsdao *_dao;
};

//account database access
class accountsdao : public dao {
public:
	accountsdao() {}
	~accountsdao() {}

	/*
	*	select all accounts from database
	*@param accounts: in/out, accounts selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int select(std::vector<account_t> &accounts, std::string *error = 0);

	/*
	*	insert new account to database
	*@param account: in, new account to insert
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int insert(const account_t &account, std::string *error = 0);

};
END_SERVICE_NAMESPACE
