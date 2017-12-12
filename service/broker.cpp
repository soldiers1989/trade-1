#include "broker.h"
#include "cube\fd.h"
#include "cube\str.h"

#include "cppconn\exception.h"
#include "cppconn\resultset.h"
#include "cppconn\statement.h"
#include "cppconn\prepared_statement.h"

BEGIN_SERVICE_NAMESPACE

//////////////////////////////////////broker class////////////////////////////////////////////
char *dept::SEPROW = "\n";
char *dept::SEPCOL = ",";
int dept::SKIPROWS = 0;
int dept::SKIPCOLS = 0;

char *server::SEPROW = "\n";
char *server::SEPCOL = ",";
int server::SKIPROWS = 0;
int server::SKIPCOLS = 0;

char *broker::FILE_NAME_DEPTS = "depts";
char *broker::FILE_NAME_QUOTES = "quotes";
char *broker::FILE_NAME_TRADES = "trades";

char *brokers::DIR = "brokers";

int broker::init(std::string *error) {
	int err = _dao.select(_id, _depts, error);
	if (err != 0) {
		return -1;
	}

	err = _dao.select(_id, server::trade, _trades, error);
	if (err != 0) {
		return -1;
	}

	err = _dao.select(_id, server::quote, _quotes, error);
	if (err != 0) {
		return -1;
	}

	return 0;
}

int broker::init(const std::string &dir, std::string *error) {
	//load departements
	int err = load_depts(dir);
	if (err != 0) {
		cube::safe_assign<std::string>(error, cube::str::format("broker %s: load departments failed.", _name.c_str()));
		return -1;
	}

	//load quote servers
	err = load_quotes(dir);
	if (err != 0) {
		cube::safe_assign<std::string>(error, cube::str::format("broker %s: load quote server failed.", _name.c_str()));
		return -1;
	}

	//load trade servers
	err = load_trades(dir);
	if (err != 0) {
		cube::safe_assign<std::string>(error, cube::str::format("broker %s: load trade server failed.", _name.c_str()));
		return -1;
	}

	return 0;
}

int broker::select(server::type type, server &server, std::string *error) {
	return 0;
}

int broker::load_depts(const std::string &dir) {
	//configure file path
	std::string path = cube::path::make(dir, FILE_NAME_DEPTS);
	if (!cube::fd::isfile(path))
		return -1;

	//parse department config file
	std::string content;
	int err = cube::file::read(path, content);
	static std::vector<std::vector<std::string>>  table = cube::str::split(content, dept::SEPROW, dept::SEPCOL);
	for (size_t row = dept::SKIPROWS; row < table.size(); row++) {
		size_t pos = dept::SKIPCOLS;
		if (table[row].size() < pos + 2)
			continue; //invalid row
		_depts.push_back(dept(table[row][pos], table[row][pos + 1]));
	}

	return 0;
}

int broker::destroy() {
	return 0;
}

int broker::load_quotes(const std::string &dir) {
	//configure file path
	std::string path = cube::path::make(dir, FILE_NAME_QUOTES);
	if (!cube::fd::isfile(path))
		return -1;

	//parse config file
	std::string content;
	int err = cube::file::read(path, content);
	static std::vector<std::vector<std::string>>  table = cube::str::split(content, server::SEPROW, server::SEPCOL);
	for (size_t row = server::SKIPROWS; row < table.size(); row++) {
		size_t pos = server::SKIPCOLS;
		if (table[row].size() < pos + 3)
			continue; //invalid row

		std::string name = table[row][pos];
		std::string host = table[row][pos + 1];
		std::string port = table[row][pos + 2];
		if(cube::str::isnum(port.c_str()))
			_quotes.push_back(server(name, host, (ushort)::atoi(port.c_str())));
	}

	return 0;
}

int broker::load_trades(const std::string &dir) {
	//configure file path
	std::string path = cube::path::make(dir, FILE_NAME_TRADES);
	if (!cube::fd::isfile(path))
		return -1;

	//parse config file
	std::string content;
	int err = cube::file::read(path, content);
	static std::vector<std::vector<std::string>>  table = cube::str::split(content, server::SEPROW, server::SEPCOL);
	for (size_t row = server::SKIPROWS; row < table.size(); row++) {
		size_t pos = server::SKIPCOLS;
		if (table[row].size() < pos + 3)
			continue; //invalid row

		std::string name = table[row][pos];
		std::string host = table[row][pos + 1];
		std::string port = table[row][pos + 2];
		if (cube::str::isnum(port.c_str()))
			_trades.push_back(server(name, host, (ushort)::atoi(port.c_str())));
	}

	return 0;
}

//////////////////////////////////////brokers class////////////////////////////////////////////
int brokers::init(std::string *error = 0) {
	std::lock_guard<std::mutex> lock(_mutex);
	
	return _dao.select(_brokers, error);
}

int brokers::init(const std::string &workdir, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);

	std::string brokersdir = cube::path::make(workdir, DIR);
	//get sub directories from configure path, suppose file name is broker name
	std::vector<std::string> names = cube::fd::dirs(brokersdir);

	//load each broker
	for (size_t i = 0; i < names.size(); i++) {
		broker *brkr = new broker(names[i]);
		std::string errmsg("");
		int err = brkr->init(cube::path::make(brokersdir, names[i]), &errmsg);
		if (err != 0) {
			_brokers.insert(std::pair<int, broker*>(i, brkr));
		} else {
			delete brkr;
			cube::safe_append<std::string>(error, errmsg);
		}
	}
	return 0;
}

int brokers::select(int id, server::type type, server &server, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);

	std::map<int, broker*>::iterator iter = _brokers.find(id);
	if (iter != _brokers.end()) {
		return iter->second->select(type, server, error);
	} else {
		cube::throw_assign<brokers::error>(error, cube::str::format("broker %d not exist.", id));
	}

	return -1;
}

int brokers::destroy() {
	std::lock_guard<std::mutex> lock(_mutex);
	
	//free all brokers
	std::map<int, broker*>::iterator iter = _brokers.begin(), iterend = _brokers.end();
	while (iter != iterend) {
		delete iter->second;
	}
	_brokers.clear();
}
//////////////////////////////////////brokerdao class////////////////////////////////////////////
int brokerdao::select(int id, std::vector<dept> &depts, std::string *error) {
	//sql to execute
	const char* sql = "select dept_id, code, name, disable, ctime from tb_dept where broker_id=?";

	//query variables
	sql::PreparedStatement *stmt = 0;
	sql::ResultSet *res = 0;

	try {
		stmt = conn()->prepareStatement(sql);
		stmt->setInt(1, id);
		res = stmt->executeQuery();
		while (res->next()) {
			int id = res->getInt("dept_id");
			std::string code = res->getString("code").c_str();
			std::string name = res->getString("name").c_str();
			bool disable = res->getBoolean("disable");
			uint ctime = res->getUInt("ctime");

			depts.push_back(dept(id, code, name, disable, ctime));
		}

		delete stmt;
		delete res;
	} catch (sql::SQLException &e) {
		cube::safe_delete<sql::PreparedStatement>(stmt);
		cube::safe_delete<sql::PreparedStatement>(stmt);

		cube::throw_assign<db::error>(error, e.what());
	}

	return 0;
}

int brokerdao::select(int id, server::type stype, std::vector<server> &servers, std::string *error) {
	//sql to execute
	const char* sql = "select server_id, name, host, port, type, disable, ctime from tb_server where broker_id=? and type=?";

	//query variables
	sql::PreparedStatement *stmt = 0;
	sql::ResultSet *res = 0;

	try {
		stmt = conn()->prepareStatement(sql);
		stmt->setInt(1, id);
		stmt->setInt(2, (int)stype);
		res = stmt->executeQuery();
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

		delete stmt;
		delete res;
	} catch (sql::SQLException &e) {
		cube::safe_delete<sql::PreparedStatement>(stmt);
		cube::safe_delete<sql::PreparedStatement>(stmt);

		cube::throw_assign<db::error>(error, e.what());
	}

	return 0;
}


//////////////////////////////////////brokersdao class////////////////////////////////////////////
int brokersdao::select(std::map<int, broker*> &brokers, std::string *error) {
	//sql to execute
	const char* sql = "select broker_id, code, name, version, disable, ctime from tb_broker;";

	//query variables
	sql::Statement *stmt = 0;
	sql::ResultSet *res = 0;

	try {
		stmt = conn()->createStatement();
		res = stmt->executeQuery(sql);
		while (res->next()) {
			int id = res->getInt("broker_id");
			std::string code = res->getString("code").c_str();
			std::string name = res->getString("name").c_str();
			std::string version = res->getString("version").c_str();
			bool disable = res->getBoolean("disable");
			uint ctime = res->getUInt("ctime");

			broker *brkr = new broker(id, code, name, version, disable, ctime);
			int err = brkr->init();
			if (err != 0) {
				brokers.insert(std::pair<int, broker*>(id, brkr));
			} else {
				delete brkr;
			}
		}

		delete stmt;
		delete res;
	} catch (sql::SQLException &e) {
		cube::safe_delete<sql::Statement>(stmt);
		cube::safe_delete<sql::Statement>(stmt);

		cube::throw_assign<db::error>(error, e.what());
	}
		
	return 0;
}
END_SERVICE_NAMESPACE
