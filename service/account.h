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
//security account class
class account {
public:
	account(const std::string &user, std::string &name, const std::string &pwd, bool disable, uint ctime) : _trade(0), _online(false), _user(user), _name(name), _pwd(pwd), _disable(disable), _ctime(ctime) {}
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
	//trade channel object
	trade::trade *_trade;
	//online status
	bool _online;

	//trade account
	std::string _user;
	//account name
	std::string _name;
	//trade account password
	std::string _pwd;
	//disable status
	bool _disable;
	//account create time
	uint _ctime;
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
	*	destroy account module
	*/
	int destroy();

private:
	//accounts managed
	std::map<std::string, account> _accounts;
	//mutex for accounts
	std::mutex _mutex;

	//brokers supported
	brokers *_brokers;

	//database access
	accountdao *_dao;
};

//account database access
class accountdao : public dao {
public:
	accountdao(db *db) : dao(db) {}
	~accountdao() {}

	/*
	*	select all accounts from database
	*@param results: in/out, accounts selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int select(std::vector<account> &results, std::string *error = 0);

	/*
	*	insert new account to database
	*@param account: in, new account to insert
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int insert(const account &account, std::string *error = 0);

};
END_SERVICE_NAMESPACE
