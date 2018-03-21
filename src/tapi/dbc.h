/*
*	db - database module for access database
*/
#pragma once
#include "stdapi.h"
#include "cube\cube.h"
#include "mysql_connection.h"
BEGIN_SEC_NAMESPACE
class db {
public:
	db() : _host(""), _user(""), _pwd(""), _port(0) {}
	db(const std::string &host, const std::string &user, const std::string &pwd, const std::string &name, ushort port = 3306) : _host(host), _user(user), _pwd(pwd), _name(name), _port(port) {}
	~db() {}

	const std::string &host() const { return _host; }
	const std::string &user() const { return _user; }
	const std::string &pwd() const { return _pwd; }
	const std::string &name() const { return _name; }
	ushort port() const { return _port; }

private:
	std::string _host;
	std::string _user;
	std::string _pwd;
	std::string _name;
	ushort _port;
};

class dbc {
public:
	//exception of database access
	typedef cube::cexception error;

public:
	dbc() : _connection(0){}
	~dbc() {}

	/*
	*	connect to database
	*@param host: in, host of database
	*@param user: in, user name of database
	*@param pwd: in, password for user
	*@param port: in, service port of database
	*@return:
	*	0 for success, otherwise <0
	*/
	int connect(const db &db, std::string *error = 0);
	int connect(const std::string &host, const std::string &user, const std::string &pwd, const std::string &name, ushort port = 3306, std::string *error = 0);

	/*
	*	set current database
	*
	*/
	int use(const std::string &db, std::string *error = 0);

	/*
	*	execute a sql
	*@param sql: in, sql to execute
	*@param stmt: out, pointer for execute result statement
	*@return:
	*	0 for success, otherwise <0
	*/
	int execute(const std::string &sql, std::string *error = 0);

	/*
	*	close database
	*@return:
	*	always 0
	*/
	int close();

public:
	/*
	*	get connection
	*/
	sql::Connection *conn() { return _connection; }

private:
	//connection to database
	sql::Connection *_connection;
};

END_SEC_NAMESPACE
