/*
*	dao - data access object module
*/
#pragma once
#include "dbc.h"
#include "model.h"
#include <vector>

BEGIN_SEC_NAMESPACE
//managers dao class
class managersdao : public dao {
public:
	/*
	*	select all manageristrators from database
	*@param managers: in/out, managers select from database
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(std::vector<manager> &managers, std::string *error = 0);

	/*
	*	select specified manager user
	*@param user: in, manager user
	*@param manager: in/out, manager data selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(const std::string &user, manager &manager, std::string *error = 0);


	/*
	*	insert new manager to database
	*@param manager: in, new manager to insert
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int add(const manager &manager, std::string *error = 0);

	/*
	*	enable or disable user in database
	*@param user: in, manager user
	*@param error, out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int enable(const std::string &user, std::string *error = 0);
	int disable(const std::string &user, std::string *error = 0);
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
	int get(std::vector<account> &accounts, std::string *error = 0);

	/*
	*	get account id by its broker id & account user name
	*@param broker: in, account broker id
	*@param user: in, account user name
	*@param acnt: out, account data
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(int broker, const std::string &user, account &acnt, std::string *error = 0);

	/*
	*	add new account to database
	*@param account: in, new account to insert
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int add(const account &account, std::string *error = 0);

	/*
	*	delete account by id
	*@param id: in, account id
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int del(int id, std::string *error = 0);
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
	int add(const broker &brkr, std::string *error = 0);

	/*
	*	 select all brokers
	*@param brokers: in/out, brokers selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(std::vector<broker> &brokers, std::string *error = 0);

	/*
	*	select specified broker by code
	*@param code: in, broker code
	*@param brkr: in/out, broker selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(const std::string &code, broker &brkr, std::string *error = 0);

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
END_SEC_NAMESPACE
