/*
*	admin - administrator module for service
*/
#pragma once
#include "stdsvr.h"
#include "db.h"
#include <mutex>
#include <vector>

BEGIN_SERVICE_NAMESPACE
class admindao;
class adminsdao;

//admin property
class admin_t {
public:
	admin_t() {}
	admin_t(const std::string &name, const std::string &user, const std::string &pwd, int role, bool disable) : id(-1), name(name), user(user), pwd(pwd), role(role), disable(disable), ctime(ctime), online(false) {}
	~admin_t() {}

	int id; //admin id
	std::string name; //admin name
	std::string user; //admin account
	std::string pwd; //admin password
	int role; //admin role
	bool disable;//disable status
	uint ctime; //create time
	bool online; //online status
};

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

//admin dao

class admindao : public dao {
public:
	/*
	*	enable or disable user in database
	*@param user: in, admin user
	*@param error, out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int enable(const std::string &user, std::string *error = 0);
	int disable(const std::string &user, std::string *error = 0);
};

//admins dao
class adminsdao : public dao {
public:
	/*
	*	select all administrators from database
	*@param admins: in/out, admins select from database
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int select(std::vector<admin_t> &admins, std::string *error = 0);

	/*
	*	select specified admin user
	*@param user: in, admin user
	*@param admin: in/out, admin data selected
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int select(const std::string &user, admin_t &admin, std::string *error = 0);


	/*
	*	insert new admin to database
	*@param admin: in, new admin to insert
	*@param error: in/out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int insert(const admin_t &admin, std::string *error = 0);
};
END_SERVICE_NAMESPACE
