#pragma once
#include "dao.h"
#include <map>
#include <mutex>
BEGIN_SEC_NAMESPACE
//managers class
class managers {
public:
	managers() {}
	~managers() {}

	/*
	*	initialize managers
	*/
	int init(std::string *error = 0);

	/*
	*	manager user login
	*@param user: in, manager user
	*@param pwd: in, user password
	*@param error, out, error message when failure happened.
	*@return:
	*	0 for success, otherwise <0
	*/
	int login(const std::string &user, const std::string &pwd, std::string *error = 0);

	/*
	*	manager user logout
	*@param user: in, manager user
	*@return:
	*	void
	*/
	void logout(const std::string &user);

	/*
	*	 add new manager
	*@param manager: in, manager to add
	*@param error, out, error message when failure happened
	*@return:
	*	0 for success, otherwise <0
	*/
	int add(const manager &adm, std::string *error = 0);

	/*
	*	disable manager user
	*@param user: in, manager user
	*@param error, out, error message when failure happened
	*@return:
	*	always 0
	*/
	int disable(const std::string &user, std::string *error = 0);

	/*
	*	destroy managers
	*/
	void destroy();

private:
	std::map<std::string, manager> _managers; //manageristrators, <user, manager*>
	std::mutex _mutex; //mutex for managers

	managersdao *_dao; //dao for database
};
END_SEC_NAMESPACE
