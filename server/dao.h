/*
*	dao - data access object module
*/
#pragma once
#include "ds.h"
#include "db.h"
#include <vector>
BEGIN_SERVICE_NAMESPACE
//admin dao class
class admindao : public dao {
public:
	/*
	*	enable or disable user in database
	*@param user: in, admin user
	*@param error, out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int enable(const std::string &user, std::string *error = 0);
	int disable(const std::string &user, std::string *error = 0);
};

//admins dao class
class adminsdao : public dao {
public:
	/*
	*	select all administrators from database
	*@param admins: in/out, admins select from database
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(std::vector<admin_t> &admins, std::string *error = 0);

	/*
	*	select specified admin user
	*@param user: in, admin user
	*@param admin: in/out, admin data selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(const std::string &user, admin_t &admin, std::string *error = 0);


	/*
	*	insert new admin to database
	*@param admin: in, new admin to insert
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int add(const admin_t &admin, std::string *error = 0);
};

//account database access
class accountsdao : public dao {
public:
	accountsdao() {}
	~accountsdao() {}

	/*
	*	get all accounts from database
	*@param accounts: in/out, accounts selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(std::vector<account_t> &accounts, std::string *error = 0);

	/*
	*	get account id by its broker id & account user name
	*@param broker: in, account broker id
	*@param user: in, account user name
	*@param acnt: out, account data
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(int broker, const std::string &user, account_t &acnt, std::string *error = 0);

	/*
	*	add new account to database
	*@param account: in, new account to insert
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int add(const account_t &account, std::string *error = 0);

	/*
	*	delete account by id
	*@param id: in, account id
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int del(int id, std::string *error = 0);
};

//broker dao class
class brokerdao : public dao {
public:
	brokerdao() {}
	~brokerdao() {}

	/*
	*	 select departments by specfied broker
	*@param id: in, broker id
	*@param depts: in/out, departments selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(int id, std::vector<dept> &depts, std::string *error = 0);

	/*
	*	 select departments by specfied broker
	*@param id: in, broker id
	*@param stype: in, server type
	*@param servers: in/out, servers selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(int id, server::type stype, std::vector<server> &servers, std::string *error = 0);
};

//brokers dao class
class brokersdao : public dao {
public:
	brokersdao() {}
	~brokersdao() {}

	/*
	*	insert new broker
	*@param brkr: new broker
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int add(const broker_t &brkr, std::string *error = 0);

	/*
	*	 select all brokers
	*@param brokers: in/out, brokers selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(std::vector<broker_t> &brokers, std::string *error = 0);

	/*
	*	select specified broker by code
	*@param code: in, broker code
	*@param brkr: in/out, broker selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(const std::string &code, broker_t &brkr, std::string *error = 0);
};
END_SERVICE_NAMESPACE
