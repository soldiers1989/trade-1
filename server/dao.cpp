#include "dao.h"
#include "cube\cube.h"
#include "cppconn\exception.h"
#include "cppconn\resultset.h"
#include "cppconn\statement.h"
#include "cppconn\prepared_statement.h"

BEGIN_SERVICE_NAMESPACE
//////////////////////////////////////////admindao class/////////////////////////////////////
int admindao::enable(const std::string &user, std::string *error) {
	//sql to execute
	const char* sql = "update tb_admin set disable=false where user=?";
	
	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setString(1, user.c_str());
		stmt->executeUpdate();
	} catch (sql::SQLException &e) {
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

int admindao::disable(const std::string &user, std::string *error) {
	//sql to execute
	const char* sql = "update tb_admin set disable=true where user=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setString(1, user.c_str());
		stmt->executeUpdate();
	} catch (sql::SQLException &e) {
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

//////////////////////////////////////////adminsdao class/////////////////////////////////////
int adminsdao::get(std::vector<admin_t> &admins, std::string *error) {
	//sql to execute
	const char* sql = "select admin_id, name, user, pwd, role, disable, unix_timestamp(ctime) as ctime from tb_admin";
	
	try {
		std::shared_ptr<sql::Statement> stmt = std::shared_ptr<sql::Statement>(conn()->createStatement());
		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery(sql));
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
	} catch (sql::SQLException &e) {
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

int adminsdao::get(const std::string &user, admin_t &admin, std::string *error) {
	//sql to execute
	const char* sql = "select admin_id, name, user, pwd, role, disable, unix_timestamp(ctime) as ctime from tb_admin where user=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setString(1, user.c_str());

		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery());
		if (res->next()) {
			admin.id = res->getInt("admin_id");
			admin.name = res->getString("name").c_str();
			admin.user = res->getString("user").c_str();
			admin.pwd = res->getString("pwd").c_str();
			admin.role = res->getInt("role");
			admin.disable = res->getBoolean("disable");
			admin.ctime = res->getUInt("ctime");
		}
	} catch (sql::SQLException &e) {
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

int adminsdao::add(const admin_t &admin, std::string *error) {
	//sql to execute
	const char* sql = "insert into tb_admin(name, user, pwd, role, disable) values(?, ?, ?, ?, ?)";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));

		stmt->setString(1, admin.name.c_str());
		stmt->setString(2, admin.user.c_str());
		stmt->setString(3, admin.pwd.c_str());
		stmt->setInt(4, admin.role);
		stmt->setBoolean(5, admin.disable);
		stmt->executeUpdate();
	} catch (sql::SQLException &e) {
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

//////////////////////////////////////////accountsdao class/////////////////////////////////////
int accountsdao::get(std::vector<account_t> &accounts, std::string *error) {
	//sql to execute
	const char* sql = "select account_id, broker, admin, name, user, pwd, cfrate, cflimit, bfrate, sfrate, disable, unix_timestamp(ctime) as ctime from tb_account;";

	try {
		std::shared_ptr<sql::Statement> stmt = std::shared_ptr<sql::Statement>(conn()->createStatement());
		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery(sql));
		while (res->next()) {
			account_t acnt;
			acnt.id = res->getInt("account_id");
			acnt.broker = res->getInt("broker");
			acnt.admin = res->getInt("admin");
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
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

int accountsdao::get(int broker, const std::string &user, account_t &acnt, std::string *error) {
	//sql to execute
	const char* sql = "select account_id, broker, admin, name, user, pwd, cfrate, cflimit, bfrate, sfrate, disable, unix_timestamp(ctime) as ctime from tb_account where broker=? and user=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setInt(1, broker);
		stmt->setString(2, user.c_str());

		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery(sql));
		if (res->next()) {
			acnt.id = res->getInt("account_id");
			acnt.broker = res->getInt("broker");
			acnt.admin = res->getInt("admin");
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
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

int accountsdao::add(const account_t &account, std::string *error) {
	//sql to execute
	const char* sql = "insert into tb_account(broker, admin, name, user, pwd, cfrate, cflimit, bfrate, sfrate, disable) values(?, ?, ?, ?, ?, ?, ?, ?, ?, ?)";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));

		stmt->setInt(1, account.broker);
		stmt->setInt(2, account.admin);
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
		cube::throw_assign<db::error>(error, e.what());
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
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

//////////////////////////////////////brokerdao class////////////////////////////////////////////
int brokerdao::get(int id, std::vector<dept> &depts, std::string *error) {
	//sql to execute
	const char* sql = "select dept_id, code, name, disable, unix_timestamp(ctime) as ctime from tb_dept where broker=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setInt(1, id);

		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery(sql));
		while (res->next()) {
			int id = res->getInt("dept_id");
			std::string code = res->getString("code").c_str();
			std::string name = res->getString("name").c_str();
			bool disable = res->getBoolean("disable");
			uint ctime = res->getUInt("ctime");

			depts.push_back(dept(id, code, name, disable, ctime));
		}
	} catch (sql::SQLException &e) {
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

int brokerdao::get(int id, server::type stype, std::vector<server> &servers, std::string *error) {
	//sql to execute
	const char* sql = "select server_id, name, host, port, type, disable, unix_timestamp(ctime) as ctime from tb_server where brokerd=? and type=?";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		stmt->setInt(1, id);
		stmt->setInt(2, (int)stype);

		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery(sql));
		while (res->next()) {
			int id = res->getInt("server_id");
			std::string name = res->getString("name").c_str();
			std::string host = res->getString("host").c_str();
			ushort port = (ushort)(res->getUInt("port"));
			int type = res->getInt("type");
			bool disable = res->getBoolean("disable");
			uint ctime = res->getUInt("ctime");

			servers.push_back(server(id, name, host, port, type, disable, ctime));
		}
	} catch (sql::SQLException &e) {
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}


//////////////////////////////////////brokersdao class////////////////////////////////////////////
int brokersdao::add(const broker_t &brkr, std::string *error) {
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
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

int brokersdao::get(std::vector<broker_t> &brokers, std::string *error) {
	//sql to execute
	const char* sql = "select broker_id, code, name, version, disable, unix_timestamp(ctime) as ctime from tb_broker;";

	try {
		std::shared_ptr<sql::PreparedStatement> stmt = std::shared_ptr<sql::PreparedStatement>(conn()->prepareStatement(sql));
		std::shared_ptr<sql::ResultSet> res = std::shared_ptr<sql::ResultSet>(stmt->executeQuery());
		while (res->next()) {
			int id = res->getInt("broker_id");
			std::string code = res->getString("code").c_str();
			std::string name = res->getString("name").c_str();
			std::string version = res->getString("version").c_str();
			bool disable = res->getBoolean("disable");
			uint ctime = res->getUInt("ctime");

			brokers.push_back(broker_t(id, code, name, version, disable, ctime));
		}
	} catch (sql::SQLException &e) {
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

int brokersdao::get(const std::string &code, broker_t &brkr, std::string *error) {
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
			std::string code = res->getString("code").c_str();
			std::string name = res->getString("name").c_str();
			std::string version = res->getString("version").c_str();
			bool disable = res->getBoolean("disable");
			uint ctime = res->getUInt("ctime");

			brkr = broker_t(id, code, name, version, disable, ctime);
		}
	} catch (sql::SQLException &e) {
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}
END_SERVICE_NAMESPACE
