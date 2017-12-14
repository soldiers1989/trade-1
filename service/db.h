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
	*@param port: in, service port of database
	*@return:
	*	0 for success, otherwise <0
	*/
	int connect(const std::string &host, const std::string &user, const std::string &pwd, ushort port = 3306, std::string *error = 0);

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

class dao {
public:
	dao() {}
	~dao() {}

	/*
	*	 set database for dao
	*/
	static void setdb(db *db);
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
	db *database() { return _db; }

	/*
	*	get database connection
	*/
	sql::Connection *conn() { return _db->conn(); }

private:
	//database of dao
	static db *_db;
};
END_SERVICE_NAMESPACE
