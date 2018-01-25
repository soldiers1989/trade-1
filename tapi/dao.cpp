#include "dao.h"
#include "cppconn\exception.h"
#include "cppconn\resultset.h"
#include "cppconn\statement.h"
#include "cppconn\prepared_statement.h"

BEGIN_SEC_NAMESPACE
//////////////////////////////////////////managersdao class/////////////////////////////////////
int managersdao::get(std::vector<manager> &managers, std::string *error) {
	//sql to execute
	const char* sql = "select manager_id, name, user, pwd, role, disable, unix_timestamp(ctime) as ctime from tb_manager";
	
	try {
		std::shared_ptr<sql::Statement> stmt = std::shared_ptr<sql::Statement>(conn()->createStatement());
		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery(sql));
		while (res->next()) {
			manager adm;
			adm.id = res->getInt("manager_id");
			adm.name = res->getString("name").c_str();
			adm.user = res->getString("user").c_str();
			adm.pwd = res->getString("pwd").c_str();
			adm.role = res->getInt("role");
			adm.disable = res->getBoolean("disable");
			adm.ctime = res->getUInt("ctime");

			managers.push_back(adm);
		}
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

int managersdao::get(const std::string &user, manager &manager, std::string *error) {
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
		}
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

int managersdao::add(const manager &manager, std::string *error) {
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

int managersdao::enable(const std::string &user, std::string *error) {
	//sql to execute
	const char* sql = "update tb_manager set disable=false where user=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setString(1, user.c_str());
		stmt->executeUpdate();
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

int managersdao::disable(const std::string &user, std::string *error) {
	//sql to execute
	const char* sql = "update tb_manager set disable=true where user=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setString(1, user.c_str());
		stmt->executeUpdate();
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

//////////////////////////////////////////accountsdao class/////////////////////////////////////
int accountsdao::get(std::vector<account> &accounts, std::string *error) {
	//sql to execute
	const char* sql = "select account_id, broker, manager, name, user, pwd, cfrate, cflimit, bfrate, sfrate, disable, unix_timestamp(ctime) as ctime from tb_account;";

	try {
		std::shared_ptr<sql::Statement> stmt = std::shared_ptr<sql::Statement>(conn()->createStatement());
		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery(sql));
		while (res->next()) {
			account acnt;
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

int accountsdao::get(int broker, const std::string &user, account &acnt, std::string *error) {
	//sql to execute
	const char* sql = "select account_id, broker, manager, name, user, pwd, cfrate, cflimit, bfrate, sfrate, disable, unix_timestamp(ctime) as ctime from tb_account where broker=? and user=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setInt(1, broker);
		stmt->setString(2, user.c_str());

		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery(sql));
		if (res->next()) {
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
		}
	} catch (sql::SQLException &e) {
		cube::throw_assign<dao::error>(error, e.what());
		return -1;
	}

	return 0;
}

int accountsdao::add(const account &account, std::string *error) {
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

int accountsdao::del(int id, std::string *error) {
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

//////////////////////////////////////brokersdao class////////////////////////////////////////////
int brokersdao::add(const broker &brkr, std::string *error) {
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

int brokersdao::get(std::vector<broker> &brokers, std::string *error) {
	//sql to execute
	const char* sql = "select broker_id, code, name, version, disable, unix_timestamp(ctime) as ctime from tb_broker;";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery());
		while (res->next()) {
			broker brkr;
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

int brokersdao::get(const std::string &code, broker &brkr, std::string *error) {
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

int brokersdao::get(int id, std::vector<dept> &depts, std::string *error) {
	//sql to execute
	const char* sql = "select dept_id, code, name, disable, unix_timestamp(ctime) as ctime from tb_dept where broker=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setInt(1, id);

		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery(sql));
		while (res->next()) {
			dept dept;
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

int brokersdao::get(int id, server::type stype, std::vector<server> &servers, std::string *error) {
	//sql to execute
	const char* sql = "select server_id, name, host, port, type, disable, unix_timestamp(ctime) as ctime from tb_server where brokerd=? and type=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setInt(1, id);
		stmt->setInt(2, (int)stype);

		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery(sql));
		while (res->next()) {
			server svr;
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
END_SEC_NAMESPACE
