/*
*	db - database module for access database
*/
#pragma once
#include "stdsvr.h"
#include "mysql_connection.h"
BEGIN_SERVICE_NAMESPACE
class db {
public:
	//exception of database access
	typedef std::exception error;

public:
	db() : _connection(0){}
	~db() {}

	/*
	*	connect to database
	*@param host: in, host of database
	*@param user: in, user name of database
	*@param pwd: in, password for user
	*@param db: in, database name
	*@param port: in, service port of database
	*@return:
	*	0 for success, otherwise <0
	*/
	int connect(const std::string &host, const std::string &user, const std::string &pwd, const std::string &db, ushort port = 3306, std::string *error = 0);

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

private:
	//connection to database
	sql::Connection *_connection;
};

class dao {
public:
	dao() {}
	~dao() {}

	/*
	*	execute a sql
	*@param sql: in, sql to execute
	*@param stmt: out, pointer for execute result statement
	*@return:
	*	0 for success, otherwise <0
	*/
	int execute(const std::string &sql, std::string *error = 0);

public:
	/*
	*	set database for dao
	*@param db: in, database for dao
	*@return:
	*	void
	*/
	static void setdb(db *db);
private:
	//database of dao
	static db *_db;
};
END_SERVICE_NAMESPACE
