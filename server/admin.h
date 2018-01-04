/*
*	admin - administrator data access module
*/
#pragma once
#include "dao.h"
#include <mutex>
#include <vector>

BEGIN_SERVICE_NAMESPACE
//admin class
class admin {
public:
	static const char *ERROR_PWD;
	static const char *ERROR_DISABLED;

public:
	admin(const admin_t &adm) : _admin(adm), _dao(0) {}
	~admin() {}

	/*
	*	initialize admin
	*/
	int init(std::string *error = 0);

	/*
	*	admin user login
	*@param user: in, admin user
	*@param pwd: in, user password
	*@param error, out, error message when failure happened.
	*@return:
	*	0 for success, otherwise <0
	*/
	int login(const std::string &pwd, std::string *error = 0);

	/*
	*	admin user logout
	*@param user: in, admin user
	*@return:
	*	always 0
	*/
	int logout();

	/*
	*	disable admin user
	*@param user: in, admin user
	*@param error, out, error message when failure happened
	*@return:
	*	always 0
	*/
	int disable(std::string *error = 0);

	/*
	*	destroy admin
	*/
	void destroy();
private:
	admin_t _admin; //admin property

	admindao *_dao; //admin dao
};

//admins class
class admins {
public:
	static const char * ERROR_NOTEXIST;

public:
	admins() {}
	~admins() {}

	/*
	*	initialize admins
	*/
	int init(std::string *error = 0);

	/*
	*	admin user login
	*@param user: in, admin user
	*@param pwd: in, user password
	*@param error, out, error message when failure happened.
	*@return:
	*	0 for success, otherwise <0
	*/
	int login(const std::string &user, const std::string &pwd, std::string *error = 0);

	/*
	*	admin user logout
	*@param user: in, admin user
	*@return:
	*	always 0
	*/
	int logout(const std::string &user);

	/*
	*	 add new admin
	*@param admin: in, admin to add
	*@param error, out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int add(const admin_t &adm, std::string *error = 0);

	/*
	*	disable admin user
	*@param user: in, admin user
	*@param error, out, error message when failure happened
	*@return:
	*	always 0
	*/
	int disable(const std::string &user, std::string *error = 0);

	/*
	*	destroy admins
	*/
	void destroy();

private:
	std::map<std::string, admin*> _admins; //administrators, <user, admin*>
	std::mutex _mutex; //mutex for admins

	adminsdao *_dao; //dao for database
};
END_SERVICE_NAMESPACE
