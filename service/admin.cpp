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
	int err = _dao->select(adms, error);
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
	int err = _dao->insert(adm, error);
	if (err != 0) {
		return -1;
	}

	//get complete admin from database
	admin_t newadm;
	err = _dao->select(adm.user, newadm, error);
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

//////////////////////////////////////////admindao class/////////////////////////////////////
int admindao::enable(const std::string &user, std::string *error) {
	//sql to execute
	const char* sql = "update tb_admin set disable=false where user=?";

	//query variables
	sql::PreparedStatement *stmt = 0;
	try {
		stmt = conn()->prepareStatement(sql);
		stmt->setString(1, user.c_str());
		stmt->executeUpdate();
		delete stmt;

	} catch (sql::SQLException &e) {
		cube::safe_delete<sql::PreparedStatement>(stmt);
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

int admindao::disable(const std::string &user, std::string *error) {
	//sql to execute
	const char* sql = "update tb_admin set disable=true where user=?";

	//query variables
	sql::PreparedStatement *stmt = 0;
	try {
		stmt = conn()->prepareStatement(sql);
		stmt->setString(1, user.c_str());
		stmt->executeUpdate();
		delete stmt;

	} catch (sql::SQLException &e) {
		cube::safe_delete<sql::PreparedStatement>(stmt);
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

//////////////////////////////////////////adminsdao class/////////////////////////////////////
int adminsdao::select(std::vector<admin_t> &admins, std::string *error) {
	//sql to execute
	const char* sql = "select admin_id, name, user, pwd, role, disable, unix_timestamp(ctime) as ctime from tb_admin";

	//query variables
	sql::Statement *stmt = 0;
	sql::ResultSet *res = 0;

	try {
		stmt = conn()->createStatement();
		res = stmt->executeQuery(sql);
		while (res->next()) {
			admin_t adm;
			adm.id = res->getInt("admin_id");
			adm.name = res->getString("name").c_str();
			adm.user = res->getString("user").c_str();
			adm.pwd = res->getString("pwd").c_str();
			adm.role = res->getInt("role");
			adm.disable = res->getBoolean("disable");
			adm.ctime = res->getUInt("ctime");

			admins.push_back(adm);
		}

		delete stmt;
		delete res;
	} catch (sql::SQLException &e) {
		cube::safe_delete<sql::Statement>(stmt);
		cube::safe_delete<sql::ResultSet>(res);

		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

int adminsdao::select(const std::string &user, admin_t &admin, std::string *error) {
	//sql to execute
	const char* sql = "select admin_id, name, user, pwd, role, disable, unix_timestamp(ctime) as ctime from tb_admin where user=?";

	//query variables
	sql::PreparedStatement *stmt = 0;
	sql::ResultSet *res = 0;

	try {
		stmt = conn()->prepareStatement(sql);
		stmt->setString(1, user.c_str());
		res = stmt->executeQuery();
		if (res->next()) {
			admin.id = res->getInt("admin_id");
			admin.name = res->getString("name").c_str();
			admin.user = res->getString("user").c_str();
			admin.pwd = res->getString("pwd").c_str();
			admin.role = res->getInt("role");
			admin.disable = res->getBoolean("disable");
			admin.ctime = res->getUInt("ctime");
		}

		delete stmt;
		delete res;
	} catch (sql::SQLException &e) {
		cube::safe_delete<sql::PreparedStatement>(stmt);
		cube::safe_delete<sql::ResultSet>(res);

		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

int adminsdao::insert(const admin_t &admin, std::string *error) {
	//sql to execute
	const char* sql = "insert into tb_admin(name, user, pwd, role, disable) values(?, ?, ?, ?, ?)";

	//query variables
	sql::PreparedStatement *stmt = 0;
	try {
		stmt = conn()->prepareStatement(sql);		
		stmt->setString(1, admin.name.c_str());
		stmt->setString(2, admin.user.c_str());
		stmt->setString(3, admin.pwd.c_str());
		stmt->setInt(4, admin.role);
		stmt->setBoolean(5, admin.disable);
		stmt->executeUpdate();

		delete stmt;

	} catch (sql::SQLException &e) {
		cube::safe_delete<sql::PreparedStatement>(stmt);
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}
END_SERVICE_NAMESPACE
