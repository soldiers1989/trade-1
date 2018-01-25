#include "account.h"
BEGIN_SEC_NAMESPACE
//////////////////////////////////////////accounts class/////////////////////////////////////
int accounts::init(std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//create dao
	_dao = new accountsdao();

	//load all accounts from database
	std::vector<account> acnts;
	int err = _dao->get(acnts, error);
	if (err != 0)
		return -1;

	for (size_t i = 0; i < acnts.size(); i++) {
		_accounts.insert(std::pair<std::string, account>(acnts[i].name, acnts[i]));
	}

	return 0;
}

int accounts::add(const account &acnt, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//add account if not exist
	std::map<std::string, account>::iterator iter = _accounts.find(acnt.name);
	if (iter != _accounts.end())
		return 0;
	return _dao->add(acnt, error);
}

int accounts::del(int id, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//first remove from account list
	

	//then remove from database
	return _dao->del(id, error);
}

int accounts::destroy() {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<std::string, account>::iterator iter = _accounts.begin(), iterend = _accounts.end();
	while (iter != iterend) {
		iter->second.logout();
		iter++;
	}
	_accounts.clear();

	if (_dao != 0) {
		delete _dao;
		_dao = 0;
	}
	return 0;
}
END_SEC_NAMESPACE
