#pragma once
#include "stdapi.h"
#include "trade\trade.h"
#include <string>
BEGIN_SEC_NAMESPACE
//model base class
class model {
public:
	model() {}
	virtual ~model() {}
};

//account's fee property
class fee {
public:
	fee() : cfrate(0.0), cflimit(0.0), bfrate(0.0), sfrate(0.0) {}
	//fee(float cfrate, float cflimit, float bfrate, float sfrate) : cfrate(cfrate), cflimit(cflimit), bfrate(bfrate), sfrate(sfrate) {}
	~fee() {}

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
class money {
public:
	money() : smoney(0), lmoney(0) {}
	//money(float smoney, float lmoney) : smoney(smoney), lmoney(lmoney) {}
	~money() {}

	//start money
	float smoney;
	//left money
	float lmoney;
};

//broker department class
class dept : public model{
public:
	dept() : id(-1), code(""), name(""), disable(true), ctime(0) {}
	//dept(int id, const std::string &name, const std::string &code, bool disable, uint ctime) : id(id), code(code), name(name), disable(disable), ctime(ctime) {}
	//dept(const std::string &name, const std::string &code) : name(name), code(code) {}
	~dept() {}

	int id; //department id
	std::string code; //department code
	std::string name; //department name
	bool disable; //disable flag
	uint ctime; //create time
};

//broker's server class
class server : public model {
public:
	//server type
	typedef enum class type { trade = 0, quote = 1 } type;

public:
	server() {}
	//server(int id, const std::string &name, const std::string &host, ushort port, int stype, bool disable, uint ctime) : id(id), name(name), host(host), port(port), stype((type)stype), disable(disable), ctime(ctime) {}
	//server(const std::string &name, const std::string &host, ushort port) : name(name), host(host), port(port) {}
	~server() {}

	int id; //server id
	std::string name; //server name
	std::string host; //host address, ip or domain name
	ushort port; //service port
	int stype; //server type;
	bool disable; //disable flag
	uint ctime; //create time
};

//manager model class
class manager : public model{
public:
	manager() : id(-1), name(""), user(""), pwd(""), role(-1), disable(true), ctime(0), online(false), token("") {}
	~manager() {}

	/*
	*	manager user login
	*@param pwd: in, user password
	*@param error, out, error message when failure happened.
	*@return:
	*	0 for success, otherwise <0
	*/
	int login(const std::string &pwd, std::string *error = 0);

	/*
	*	manager user logout
	*@param user: in, manager user
	*@return:
	*	void
	*/
	void logout();

public:
	int id; //manager id
	std::string name; //manager name
	std::string user; //manager account
	std::string pwd; //manager password
	int role; //manager role
	bool disable;//disable status
	uint ctime; //create time

	bool online; //online status
	std::string token; //token for manager
};

//account model class
class account : public model{
public:
	account() :  _trade(0) {}
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
	//acccount id
	int id;
	//broker id
	int broker;
	//manager id
	int manager;
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

private:

	//trade channel object
	trade::trade *_trade;
};

//broker model class
class broker : public model{
public:
	broker() : id(-1), code(""), name(""), version(""), disable(true), ctime(0) {}
	~broker() {}
	/*
	*	select a server from broker
	*@param type: in, type of server
	*@param server: in/out, server selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise<0
	*/
	int select(server::type type, server &server, std::string *error = 0);

	/*
	*	destroy brokers
	*/
	int destroy();

public:
	int id; //broker id
	std::string code; //broker code
	std::string name; //broker name
	std::string version; //client version
	bool disable; //disable flag
	uint ctime; //create time

	std::vector<dept> depts; //broker's departments
	std::vector<server> quotes; //quote servers
	std::vector<server> trades; //trade servers
};
END_SEC_NAMESPACE
