/*
*	manage - management module
*/
#pragma once
#include "dba.h"
#include "auth.h"
#include <map>
#include <mutex>
BEGIN_SEC_NAMESPACE
//manager class
class manage {
public:
	typedef cube::cexception error;

	//manage instance
	static manage inst;
public:
	~manage() {}

	/*
	*	initialize manage module
	*/
	int init(const db &db, std::string *error = 0);

	/*
	*	manager user login/logout
	*@param user: in, manager use name
	*@param pwd: in, user password
	*@param auth: in/out, user auth
	*@param error, out, error message when failure happened.
	*@return:
	*	0 for success, otherwise <0
	*/
	int login(const std::string &user, const std::string &pwd, auth &auth, std::string *error = 0);
	int logout(const auth &auth, std::string *error = 0);

	/*
	*	 manager data manage
	*@return:
	*	0 for success, otherwise <0
	*/
	int get_manager(const auth &auth, std::vector<model::manager> &mgrs, std::string *error = 0);
	int get_manager(const auth &auth, const std::string &user, model::manager &mgr, std::string *error = 0);
	int add_manager(const auth &auth, const model::manager &mgr, std::string *error = 0);
	int del_manager(const auth &auth, int id, std::string *error = 0);
	int del_manager(const auth &auth, const std::string &user, std::string *error = 0);
	int mod_manager(const auth &auth, const std::string &user, bool disable, std::string *error = 0);
	int mod_manager(const auth &auth, const std::string &user, const model::manager &mgr, std::string *error = 0);

	/*
	*	account data manage
	*@return:
	*	0 for success, otherwise <0
	*/
	int get_account(const auth &auth, std::vector<model::account> &acnts, std::string *error = 0);
	int get_account(const auth &auth, int broker, const std::string &user, model::account &acnt, std::string *error = 0);
	int add_account(const auth &auth, const model::account &acnt, std::string *error = 0);
	int del_account(const auth &auth, int id, std::string *error = 0);

	/*
	*	broker data manage
	*@return:
	*	0 for success, otherwise <0
	*/
	int get_broker(const auth &auth, std::vector<model::broker> &brkrs, std::string *error = 0);
	int get_broker(const auth &auth, const std::string &code, model::broker &brkr, std::string *error = 0);
	int get_broker(const auth &auth, int id, std::vector<model::dept> &depts, std::string *error = 0);
	int get_broker(const auth &auth, int id, model::server::type stype, std::vector<model::server> &svrs, std::string *error = 0);
	int add_broker(const auth &auth, const model::broker &brkr, std::string *error = 0);

	/*
	*	destroy manage module
	*/
	void destroy();

private:
	/*
	*	check authority
	*/
	bool check_auth(const auth &auth, std::string *error = 0);

private:
	manage() {}

	//database admin
	dba::dba _dba;

	//mutex auths
	std::mutex _mutex;
	//login auths
	std::map<std::string, auth> _auths;
};
END_SEC_NAMESPACE
