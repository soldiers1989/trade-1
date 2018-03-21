#pragma once
#include "dao.h"
BEGIN_SEC_DBA_NAMESPACE
class dba {
public:
	dba() {}
	virtual ~dba() {}

	int connect(const db &db, std::string *error = 0);
	int close(std::string *error = 0);

	//manager data access
	int get_manager(std::vector<model::manager> &managers, std::string *error = 0);
	int get_manager(const std::string &user, model::manager &manager, std::string *error = 0);
	int add_manager(const model::manager &manager, std::string *error = 0);
	int del_manager(int id, std::string *error = 0);
	int del_manager(const std::string &user, std::string *error = 0);
	int mod_manager(const std::string &user, bool disable, std::string *error = 0);
	int mod_manager(const std::string &user, const model::manager &manager, std::string *error = 0);

	//account data access
	int get_account(std::vector<model::account> &accounts, std::string *error = 0);
	int get_account(int broker, const std::string &user, model::account &account, std::string *error = 0);
	int add_account(const model::account &account, std::string *error = 0);
	int del_account(int id, std::string *error = 0);

	//broker data access
	int get_broker(std::vector<model::broker> &brokers, std::string *error = 0);
	int get_broker(const std::string &code, model::broker &brkr, std::string *error = 0);
	int get_broker(int id, std::vector<model::dept> &depts, std::string *error = 0);
	int get_broker(int id, model::server::type stype, std::vector<model::server> &servers, std::string *error = 0);
	int add_broker(const model::broker &brkr, std::string *error = 0);

private:
	//database connection
	dbc _dbc;

	//manager dao
	dao::manager _managerdao;
	//account dao
	dao::account _accountdao;
	//broker dao
	dao::broker _brokerdao;
};
END_SEC_DBA_NAMESPACE
