#include "dba.h"
BEGIN_SEC_DBA_NAMESPACE
////////////////////////////////////////////dba connect/close methods////////////////////////////////////////
int dba::connect(const db &db, std::string *error) {
	//build connection to database
	int err =  _dbc.connect(db, error);
	if (err != 0) {
		return -1;
	}

	//set dao database connections
	_managerdao.db(&_dbc);
	_accountdao.db(&_dbc);
	_brokerdao.db(&_dbc);

	return 0;
}

int dba::close(std::string *error) {
	_dbc.close();
	return 0;
}

////////////////////////////////////////////manager data access methods////////////////////////////////////////
int dba::get_manager(std::vector<model::manager> &managers, std::string *error) {
	return _managerdao.get(managers, error);
}

int dba::get_manager(const std::string &user, model::manager &manager, std::string *error) {
	return _managerdao.get(user, manager, error);
}

int dba::add_manager(const model::manager &manager, std::string *error) {
	return _managerdao.add(manager, error);
}

int dba::del_manager(int id, std::string *error) {
	return _managerdao.del(id, error);
}

int dba::del_manager(const std::string &user, std::string *error) {
	return _managerdao.del(user, error);
}

int dba::mod_manager(const std::string &user, bool disable, std::string *error) {
	return _managerdao.mod(user, disable, error);
}

int dba::mod_manager(const std::string &user, const model::manager &manager, std::string *error) {
	return _managerdao.mod(user, manager, error);
}

////////////////////////////////////////////account data access methods////////////////////////////////////////
int dba::get_account(std::vector<model::account> &accounts, std::string *error) {
	return _accountdao.get(accounts, error);
}

int dba::get_account(int broker, const std::string &user, model::account &account, std::string *error) {
	return _accountdao.get(broker, user, account, error);
}

int dba::add_account(const model::account &account, std::string *error) {
	return _accountdao.add(account, error);
}

int dba::del_account(int id, std::string *error) {
	return _accountdao.del(id, error);
}

/////////////////////////////////////////////broker data access methods/////////////////////////////////////////
int dba::get_broker(std::vector<model::broker> &brokers, std::string *error) {
	return _brokerdao.get(brokers, error);
}

int dba::get_broker(const std::string &code, model::broker &brkr, std::string *error) {
	return _brokerdao.get(code, brkr, error);
}

int dba::get_broker(int id, std::vector<model::dept> &depts, std::string *error) {
	return _brokerdao.get(id, depts, error);
}

int dba::get_broker(int id, model::server::type stype, std::vector<model::server> &servers, std::string *error) {
	return _brokerdao.get(id, stype, servers, error);
}

int dba::add_broker(const model::broker &brkr, std::string *error) {
	return _brokerdao.add(brkr, error);
}

END_SEC_DBA_NAMESPACE
