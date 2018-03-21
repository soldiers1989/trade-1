/*
*	dao - data access object module
*/
#pragma once
#include "dbc.h"
#include "model.h"
#include <vector>

BEGIN_SEC_DAO_NAMESPACE
//dao base class
class dao {
public:
	//exception of database access
	typedef cube::cexception error;

public:
	dao() : _dbc(0) {}
	dao(dbc *dbc) : _dbc(dbc) {}
	~dao() {}

	/*
	*	set dao databasec connection
	*/
	void db(dbc *dbc) { _dbc = dbc; }

protected:
	/*
	*	execute a sql
	*@param sql: in, sql to execute
	*@param stmt: out, pointer for execute result statement
	*@return:
	*	0 for success, otherwise <0
	*/
	int execute(const std::string &sql, std::string *error = 0);

	/*
	*	get database object
	*/
	dbc *database() { return _dbc; }

	/*
	*	get database connection
	*/
	sql::Connection *conn() { return _dbc->conn(); }

private:
	//database of dao
	dbc *_dbc;
};

//manager dao class
class manager : public dao {
public:
	/*
	*	select all manageristrators from database
	*@param managers: in/out, managers select from database
	*@param error: in/out, error message when failure happened
	*@return:
	*	number got, otherwise <0
	*/
	int get(std::vector<model::manager> &managers, std::string *error = 0);

	/*
	*	select specified manager user
	*@param user: in, manager user
	*@param manager: in/out, manager data selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	number got, otherwise <0
	*/
	int get(const std::string &user, model::manager &manager, std::string *error = 0);


	/*
	*	insert new manager to database
	*@param manager: in, new manager to insert
	*@param error: in/out, error message when failure happened
	*@return:
	*	number add, otherwise <0
	*/
	int add(const model::manager &manager, std::string *error = 0);

	/*
	*	delete manager from database
	*@param manager: in, new manager to insert
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int del(int id, std::string *error = 0);
	int del(const std::string &user, std::string *error = 0);

	/*
	*	enable or disable user in database
	*@param user: in, manager user
	*@param error, out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int mod(const std::string &user, bool disable, std::string *error = 0);
	int mod(const std::string &user, const model::manager &manager, std::string *error = 0);
};

//account database access
class account : public dao {
public:
	/*
	*	get all accounts from database
	*@param accounts: in/out, accounts selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(std::vector<model::account> &accounts, std::string *error = 0);

	/*
	*	get account id by its broker id & account user name
	*@param broker: in, account broker id
	*@param user: in, account user name
	*@param acnt: out, account data
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(int broker, const std::string &user, model::account &account, std::string *error = 0);

	/*
	*	add new account to database
	*@param account: in, new account to insert
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int add(const model::account &account, std::string *error = 0);

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
class broker : public dao {
public:
	/*
	*	 select all brokers
	*@param brokers: in/out, brokers selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(std::vector<model::broker> &brokers, std::string *error = 0);

	/*
	*	select specified broker by code
	*@param code: in, broker code
	*@param brkr: in/out, broker selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(const std::string &code, model::broker &brkr, std::string *error = 0);

	/*
	*	 select departments by specfied broker
	*@param id: in, broker id
	*@param depts: in/out, departments selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(int id, std::vector<model::dept> &depts, std::string *error = 0);

	/*
	*	 select departments by specfied broker
	*@param id: in, broker id
	*@param stype: in, server type
	*@param servers: in/out, servers selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int get(int id, model::server::type stype, std::vector<model::server> &servers, std::string *error = 0);

	/*
	*	insert new broker
	*@param brkr: new broker
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int add(const model::broker &brkr, std::string *error = 0);
};

END_SEC_DAO_NAMESPACE
