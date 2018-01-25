#include "manager.h"

BEGIN_SEC_NAMESPACE
//////////////////////////////////////////managers class/////////////////////////////////////
int managers::init(std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//create dao
	_dao = new managersdao();

	//load all accounts from database
	std::vector<manager> adms;
	int err = _dao->get(adms, error);
	if (err != 0)
		return -1;

	for (size_t i = 0; i < adms.size(); i++) {
		_managers.insert(std::pair<std::string, manager>(adms[i].user, adms[i]));
	}

	return 0;
}

int managers::login(const std::string &user, const std::string &pwd, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<std::string, manager>::iterator iter = _managers.find(user);
	if (iter != _managers.end()) {
		return iter->second.login(pwd, error);
	}
	cube::safe_assign<std::string>(error, "user is not exist.");
	return -1;
}

void managers::logout(const std::string &user) {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<std::string, manager>::iterator iter = _managers.find(user);
	if (iter != _managers.end()) {
		iter->second.logout();
	}
}

int managers::add(const manager &adm, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<std::string, manager>::iterator iter = _managers.find(adm.user);
	if (iter != _managers.end()) {
		return 0; //manager exists
	}

	//insert new manager to database
	int err = _dao->add(adm, error);
	if (err != 0) {
		return -1;
	}

	//get complete manager from database
	manager newadm;
	err = _dao->get(adm.user, newadm, error);
	if (err != 0) {
		return -1;
	}

	//add new manager to managers
	_managers.insert(std::pair<std::string, manager>(newadm.user, newadm));

	return 0;
}

int managers::disable(const std::string &user, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<std::string, manager>::iterator iter = _managers.find(user);
	if (iter != _managers.end()) {
		iter->second.disable = true;

		_dao->disable(user, error);
	}

	return 0;
}

void managers::destroy() {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<std::string, manager>::iterator iter = _managers.begin(), iterend = _managers.end();
	while (iter != iterend) {
		iter->second.logout();
		iter++;
	}
	_managers.clear();

	if (_dao != 0) {
		delete _dao;
		_dao = 0;
	}
}
END_SEC_NAMESPACE
