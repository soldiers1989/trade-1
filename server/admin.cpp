#include "admin.h"
#include "cube\str.h"
#include "cppconn\exception.h"
#include "cppconn\resultset.h"
#include "cppconn\statement.h"
#include "cppconn\prepared_statement.h"

BEGIN_SERVICE_NAMESPACE
//////////////////////////////////////////admins class/////////////////////////////////////
const char *admin::ERROR_PWD = "wrong password";
const char *admin::ERROR_DISABLED = "user disabled";

int admin::init(std::string *error) {
	_dao = new admindao();

	return 0;
}

int admin::login(const std::string &pwd, std::string *error) {
	if (_admin.disable) {
		cube::safe_assign<std::string>(error, ERROR_DISABLED);
		return -1;
	}

	if (pwd != _admin.pwd) {
		cube::safe_assign<std::string>(error, ERROR_PWD);
		return -1;
	}

	_admin.online = true;

	return 0;
}

int admin::logout() {
	_admin.online = false;
	return 0;
}

int admin::disable(std::string *error) {
	_admin.disable = true;
	_admin.online = false;

	return 0;
}

void admin::destroy() {
	if (_dao != 0) {
		delete _dao;
		_dao = 0;
	}
}
//////////////////////////////////////////admins class/////////////////////////////////////
const char *admins::ERROR_NOTEXIST = "user not exist";

int admins::init(std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//create dao
	_dao = new adminsdao();

	//load all accounts from database
	std::vector<admin_t> adms;
	int err = _dao->get(adms, error);
	if (err != 0)
		return -1;

	for (size_t i = 0; i < adms.size(); i++) {
		admin *adm = new admin(adms[i]);
		err = adm->init(error);
		if (err != 0)
			return -1;

		_admins.insert(std::pair<std::string, admin*>(adms[i].user, adm));
	}

	return 0;
}

int admins::login(const std::string &user, const std::string &pwd, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<std::string, admin*>::iterator iter = _admins.find(user);
	if (iter != _admins.end()) {
		return iter->second->login(pwd, error);
	}
	cube::safe_assign<std::string>(error, ERROR_NOTEXIST);
	return -1;
}

int admins::logout(const std::string &user) {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<std::string, admin*>::iterator iter = _admins.find(user);
	if (iter != _admins.end()) {
		return iter->second->logout();
	}

	return 0;
}

int admins::add(const admin_t &adm, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<std::string, admin*>::iterator iter = _admins.find(adm.user);
	if (iter != _admins.end()) {
		return 0; //admin exists
	}

	//insert new admin to database
	int err = _dao->add(adm, error);
	if (err != 0) {
		return -1;
	}

	//get complete admin from database
	admin_t newadm;
	err = _dao->get(adm.user, newadm, error);
	if (err != 0) {
		return -1;
	}

	//add new admin to admins
	_admins.insert(std::pair<std::string, admin*>(newadm.user, new admin(newadm)));

	return 0;
}

int admins::disable(const std::string &user, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<std::string, admin*>::iterator iter = _admins.find(user);
	if (iter != _admins.end()) {
		return iter->second->disable(error);
	}

	return 0;
}

void admins::destroy() {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<std::string, admin*>::iterator iter = _admins.begin(), iterend = _admins.end();
	while (iter != iterend) {
		iter->second->destroy();
		delete iter->second;
		iter++;
	}
	_admins.clear();

	if (_dao != 0) {
		delete _dao;
		_dao = 0;
	}
}
END_SERVICE_NAMESPACE
