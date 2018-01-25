/*
*	dbm - database managment
*/
#pragma once
#include "dbc.h"
BEGIN_SEC_NAMESPACE
class dbm {
public:
	/*
	*	initialize database with create sql file
	*@param sqlfile: in, create table sql file
	*@param name: in, database name to create tables
	*@param db: in, database connection to use
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	static int init(const std::string &sqlfile, const std::string &name, dbc* db, std::string *error = 0);
};
END_SEC_NAMESPACE
