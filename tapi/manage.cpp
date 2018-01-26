#include "manage.h"
BEGIN_SEC_NAMESPACE
//initialize instance of manage
manage manage::inst;

//////////////////////////////////////////manage class/////////////////////////////////////
int manage::init(const db &db, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//connect to database
	int err = _dba.connect(db, error);
	if (err != 0) {
		return -1;
	}

	return 0;
}
//////////////////////////////////////////manager login/logout methods/////////////////////////////////
int manage::login(const std::string &user, const std::string &pwd, auth &auth, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check user & password
	model::manager mgr;
	int num = _dba.get_manager(user, mgr, error);
	if (num < 0) {
		//something wrong with dba
		return -1;
	} else if (num == 0) {
		//user not exist
		cube::throw_assign<manage::error>(error, "user is not exist");
		return -1;
	} else {
		//check password
		if (pwd != mgr.pwd) {
			//wrong password
			cube::throw_assign<manage::error>(error, "password is wrong");
			return -1;
		} else {
			//check if has login
			std::map<std::string, sec::auth>::iterator iter = _auths.find(user);
			if (iter != _auths.end()) {
				//login before, use exist auth
				auth = iter->second;
			} else {
				//first login, generate new auth
				auth.init(user);

				//save new auth for user
				_auths.insert(std::pair<std::string, sec::auth>(user, auth));
			}

			return 0;
		}
	}
}

int manage::logout(const auth &auth, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//logout, remove auth
	std::map<std::string, sec::auth>::iterator iter = _auths.find(auth.user());
	if (iter != _auths.end()) {
		_auths.erase(iter);
	}

	return 0;
}

///////////////////////////////////////////////manager manage methods///////////////////////////////////////
int manage::get_manager(const auth &auth, std::vector<model::manager> &mgrs, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//get managers
	return _dba.get_manager(mgrs, error);
}

int manage::get_manager(const auth &auth, const std::string &user, model::manager &mgr, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//get manager
	return _dba.get_manager(user, mgr, error);
}

int manage::add_manager(const auth &auth, const model::manager &mgr, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//add manager
	return _dba.add_manager(mgr, error);
}

int manage::del_manager(const auth &auth, int id, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//delete manager
	return _dba.del_manager(id, error);
}

int manage::del_manager(const auth &auth, const std::string &user, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//delete manager
	return _dba.del_manager(user, error);
}

int manage::mod_manager(const auth &auth, const std::string &user, bool disable, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//add manager
	return _dba.mod_manager(user, disable, error);
}

int manage::mod_manager(const auth &auth, const std::string &user, const model::manager &mgr, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//add manager
	return _dba.mod_manager(user, mgr, error);
}

//////////////////////////////////////////////////acount manage methods//////////////////////////////////////////////////////
int manage::get_account(const auth &auth, std::vector<model::account> &acnts, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//get acount
	return _dba.get_account(acnts, error);
}

int manage::get_account(const auth &auth, int broker, const std::string &user, model::account &acnt, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//get acount
	return _dba.get_account(broker, user, acnt, error);
}

int manage::add_account(const auth &auth, const model::account &acnt, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//add acount
	return _dba.add_account(acnt, error);
}

int manage::del_account(const auth &auth, int id, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//del acount
	return _dba.del_account(id, error);
}

//////////////////////////////////////////////////broker manage methods//////////////////////////////////////////////////////
int manage::get_broker(const auth &auth, std::vector<model::broker> &brkrs, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//get broker
	return _dba.get_broker(brkrs, error);
}

int manage::get_broker(const auth &auth, const std::string &code, model::broker &brkr, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//get broker
	return _dba.get_broker(code, brkr, error);
}
int manage::get_broker(const auth &auth, int id, std::vector<model::dept> &depts, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//get broker departments
	return _dba.get_broker(id, depts, error);
}

int manage::get_broker(const auth &auth, int id, model::server::type stype, std::vector<model::server> &svrs, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//get broker servers
	return _dba.get_broker(id, stype, svrs, error);
}

int manage::add_broker(const auth &auth, const model::broker &brkr, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//check authority
	if (!check_auth(auth, error)) {
		return -1;
	}

	//add broker
	return _dba.add_broker(brkr, error);
}

void manage::destroy() {
	std::lock_guard<std::mutex> lock(_mutex);
	//close database
	_dba.close();

	//clear auths
	_auths.clear();
}

bool manage::check_auth(const auth &auth, std::string *error) {
	std::map<std::string, sec::auth>::iterator iter = _auths.find(auth.user());
	if (iter != _auths.end()) {
		if (auth.token() != iter->second.token()) {
			cube::throw_assign<manage::error>(error, "invalid token");
			return false;
		}
	} else {
		cube::throw_assign<manage::error>(error, "user not login");
		return false;
	}

	return true;
}
END_SEC_NAMESPACE
