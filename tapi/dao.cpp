#include "dao.h"
#include "cppconn\exception.h"
#include "cppconn\resultset.h"
#include "cppconn\statement.h"
#include "cppconn\prepared_statement.h"

BEGIN_SEC_DAO_NAMESPACE
//////////////////////////////////dao class//////////////////////////////////
int dao::execute(const std::string &sql, std::string *error/* = 0*/) {
	if (_dbc == 0) {
		cube::throw_assign<dbc::error>(error, "database not specified.");
		return -1;
	}

	return _dbc->execute(sql, error);
}

//////////////////////////////////////////managedao class/////////////////////////////////////
int manager::get(std::vector<model::manager> &managers, std::string *error) {
	//get result
	int num = 0;

	//sql to execute
	const char* sql = "select manager_id, name, user, pwd, role, disable, unix_timestamp(ctime) as ctime from tb_manager";
	
	try {
		std::shared_ptr<sql::Statement> stmt = std::shared_ptr<sql::Statement>(conn()->createStatement());
		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery(sql));
		while (res->next()) {
			model::manager adm;
			adm.id = res->getInt("manager_id");
			adm.name = res->getString("name").c_str();
			adm.user = res->getString("user").c_str();
			adm.pwd = res->getString("pwd").c_str();
			adm.role = res->getInt("role");
			adm.disable = res->getBoolean("disable");
			adm.ctime = res->getUInt("ctime");
			managers.push_back(adm);

			num++;
		}
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return num;
}

int manager::get(const std::string &user, model::manager &manager, std::string *error) {
	//get num
	int num = 0;

	//sql to execute
	const char* sql = "select manager_id, name, user, pwd, role, disable, unix_timestamp(ctime) as ctime from tb_manager where user=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setString(1, user.c_str());

		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery());
		if (res->next()) {
			manager.id = res->getInt("manager_id");
			manager.name = res->getString("name").c_str();
			manager.user = res->getString("user").c_str();
			manager.pwd = res->getString("pwd").c_str();
			manager.role = res->getInt("role");
			manager.disable = res->getBoolean("disable");
			manager.ctime = res->getUInt("ctime");

			num++;
		}
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return num;
}

int manager::add(const model::manager &manager, std::string *error) {
	//sql to execute
	const char* sql = "insert into tb_manager(name, user, pwd, role, disable) values(?, ?, ?, ?, ?)";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));

		stmt->setString(1, manager.name.c_str());
		stmt->setString(2, manager.user.c_str());
		stmt->setString(3, manager.pwd.c_str());
		stmt->setInt(4, manager.role);
		stmt->setBoolean(5, manager.disable);
		stmt->executeUpdate();
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

int manager::del(int id, std::string *error) {
	//sql to execute
	const char* sql = "delete from tb_manager where manager_id=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setInt(1, id);
		stmt->executeUpdate();

	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

int manager::del(const std::string &user, std::string *error) {
	//sql to execute
	const char* sql = "delete from tb_manager where user=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setString(1, user);
		stmt->executeUpdate();

	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

int manager::mod(const std::string &user, bool disable, std::string *error) {
	//sql to execute
	const char* sql = "update tb_manager set disable=? where user=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setBoolean(1, disable);
		stmt->setString(2, user.c_str());
		stmt->executeUpdate();
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

int manager::mod(const std::string &user, const model::manager &manager, std::string *error) {
	//sql to execute
	const char* sql = "update tb_manager set name=?, pwd=?, role=?, disable=? where user=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));

		stmt->setString(1, manager.name.c_str());
		stmt->setString(2, manager.pwd.c_str());
		stmt->setInt(3, manager.role);
		stmt->setBoolean(4, manager.disable);
		stmt->executeUpdate();
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

//////////////////////////////////////////account class/////////////////////////////////////
int account::get(std::vector<model::account> &accounts, std::string *error) {
	//sql to execute
	const char* sql = "select account_id, broker, manager, name, user, pwd, cfrate, cflimit, bfrate, sfrate, disable, unix_timestamp(ctime) as ctime from tb_account;";

	try {
		std::shared_ptr<sql::Statement> stmt = std::shared_ptr<sql::Statement>(conn()->createStatement());
		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery(sql));
		while (res->next()) {
			model::account acnt;
			acnt.id = res->getInt("account_id");
			acnt.broker = res->getInt("broker");
			acnt.manager = res->getInt("manager");
			acnt.name = res->getString("name").c_str();
			acnt.user = res->getString("user").c_str();
			acnt.pwd = res->getString("pwd").c_str();

			acnt.cfrate = (float)res->getDouble("cfrate");
			acnt.cflimit = (float)res->getDouble("cflimit");
			acnt.bfrate = (float)res->getDouble("bfrate");
			acnt.sfrate = (float)res->getDouble("sfrate");

			acnt.disable = res->getBoolean("disable");
			acnt.ctime = res->getUInt("ctime");

			accounts.push_back(acnt);
		}
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

int account::get(int broker, const std::string &user, model::account &account, std::string *error) {
	//sql to execute
	const char* sql = "select account_id, broker, manager, name, user, pwd, cfrate, cflimit, bfrate, sfrate, disable, unix_timestamp(ctime) as ctime from tb_account where broker=? and user=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setInt(1, broker);
		stmt->setString(2, user.c_str());

		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery(sql));
		if (res->next()) {
			account.id = res->getInt("account_id");
			account.broker = res->getInt("broker");
			account.manager = res->getInt("manager");
			account.name = res->getString("name").c_str();
			account.user = res->getString("user").c_str();
			account.pwd = res->getString("pwd").c_str();

			account.cfrate = (float)res->getDouble("cfrate");
			account.cflimit = (float)res->getDouble("cflimit");
			account.bfrate = (float)res->getDouble("bfrate");
			account.sfrate = (float)res->getDouble("sfrate");

			account.disable = res->getBoolean("disable");
			account.ctime = res->getUInt("ctime");
		}
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

int account::add(const model::account &account, std::string *error) {
	//sql to execute
	const char* sql = "insert into tb_account(broker, manager, name, user, pwd, cfrate, cflimit, bfrate, sfrate, disable) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));

		stmt->setInt(1, account.broker);
		stmt->setInt(2, account.manager);
		stmt->setString(3, account.name.c_str());
		stmt->setString(4, account.user.c_str());
		stmt->setString(5, account.pwd.c_str());
		stmt->setDouble(6, account.cfrate);
		stmt->setDouble(7, account.cflimit);
		stmt->setDouble(8, account.bfrate);
		stmt->setDouble(9, account.sfrate);
		stmt->setBoolean(10, account.disable);

		stmt->executeUpdate();
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

int account::del(int id, std::string *error) {
	//sql to execute
	const char* sql = "delete from tb_account where account_id=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setInt(1, id);
		stmt->executeUpdate();

	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

//////////////////////////////////////broker class////////////////////////////////////////////
int broker::add(const model::broker &brkr, std::string *error) {
	//sql to execute
	const char* sql = "insert into tb_broker(code, name, version, disable) values(?, ?, ?, ?)";

	//query variables
	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setString(1, brkr.code.c_str());
		stmt->setString(2, brkr.name.c_str());
		stmt->setString(3, brkr.version.c_str());
		stmt->setBoolean(4, brkr.disable);

		stmt->executeUpdate();
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

int broker::get(std::vector<model::broker> &brokers, std::string *error) {
	//sql to execute
	const char* sql = "select broker_id, code, name, version, disable, unix_timestamp(ctime) as ctime from tb_broker;";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery());
		while (res->next()) {
			model::broker brkr;
			int id = res->getInt("broker_id");
			brkr.code = res->getString("code").c_str();
			brkr.name = res->getString("name").c_str();
			brkr.version = res->getString("version").c_str();
			brkr.disable = res->getBoolean("disable");
			brkr.ctime = res->getUInt("ctime");

			brokers.push_back(brkr);
		}
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

int broker::get(const std::string &code, model::broker &brkr, std::string *error) {
	//sql to execute
	const char* sql = "select broker_id, code, name, version, disable, unix_timestamp(ctime) as ctime from tb_broker where code=?";

	//query variables
	sql::PreparedStatement *stmt = 0;
	sql::ResultSet *res = 0;

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setString(1, code.c_str());

		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery());
		if (res->next()) {
			int id = res->getInt("broker_id");
			brkr.code = res->getString("code").c_str();
			brkr.name = res->getString("name").c_str();
			brkr.version = res->getString("version").c_str();
			brkr.disable = res->getBoolean("disable");
			brkr.ctime = res->getUInt("ctime");
		}
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

int broker::get(int id, std::vector<model::dept> &depts, std::string *error) {
	//sql to execute
	const char* sql = "select dept_id, code, name, disable, unix_timestamp(ctime) as ctime from tb_dept where broker=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setInt(1, id);

		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery(sql));
		while (res->next()) {
			model::dept dept;
			dept.id = res->getInt("dept_id");
			dept.code = res->getString("code").c_str();
			dept.name = res->getString("name").c_str();
			dept.disable = res->getBoolean("disable");
			dept.ctime = res->getUInt("ctime");

			depts.push_back(dept);
		}
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

int broker::get(int id, model::server::type stype, std::vector<model::server> &servers, std::string *error) {
	//sql to execute
	const char* sql = "select server_id, name, host, port, type, disable, unix_timestamp(ctime) as ctime from tb_server where brokerd=? and type=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setInt(1, id);
		stmt->setInt(2, (int)stype);

		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery(sql));
		while (res->next()) {
			model::server svr;
			svr.id = res->getInt("server_id");
			svr.name = res->getString("name").c_str();
			svr.host = res->getString("host").c_str();
			svr.port = (ushort)(res->getUInt("port"));
			svr.stype = res->getInt("type");
			svr.disable = res->getBoolean("disable");
			svr.ctime = res->getUInt("ctime");

			servers.push_back(svr);
		}
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}
END_SEC_DAO_NAMESPACE
