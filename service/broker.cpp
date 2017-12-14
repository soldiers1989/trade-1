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
	//create dao object
	_dao = new brokerdao();

	//load data from database
	int err = _dao->select(_broker.id, _depts, error);
	if (err != 0) {
		return -1;
	}

	err = _dao->select(_broker.id, server::type::trade, _trades, error);
	if (err != 0) {
		return -1;
	}

	err = _dao->select(_broker.id, server::type::quote, _quotes, error);
	if (err != 0) {
		return -1;
	}

	return 0;
}

int broker::init(const std::string &dir, std::string *error) {
	//load departements
	int err = load_depts(dir);
	if (err != 0) {
		cube::safe_assign<std::string>(error, cube::str::format("broker %s: load departments failed.", _broker.name.c_str()));
		return -1;
	}

	//load quote servers
	err = load_quotes(dir);
	if (err != 0) {
		cube::safe_assign<std::string>(error, cube::str::format("broker %s: load quote server failed.", _broker.name.c_str()));
		return -1;
	}

	//load trade servers
	err = load_trades(dir);
	if (err != 0) {
		cube::safe_assign<std::string>(error, cube::str::format("broker %s: load trade server failed.", _broker.name.c_str()));
		return -1;
	}

	return 0;
}

int broker::select(server::type type, server &server, std::string *error) {
	return 0;
}

int broker::destroy() {
	if (_dao != 0) {
		delete _dao;
		_dao = 0;
	}
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
int brokers::init(std::string *error ) {
	std::lock_guard<std::mutex> lock(_mutex);
	//create dao
	_dao = new brokersdao();

	//load data from database
	std::vector<broker_t> brkrs;
	int err = _dao->select(brkrs, error);
	if (err != 0) {
		return -1;
	}

	for (size_t i = 0; i < brkrs.size(); i++) {
		broker *brkr = new broker(brkrs[i]);
		err = brkr->init(error);
		if (err != 0) {
			delete brkr;
			return -1;//process error later
		}
		_brokers.insert(std::pair<std::string, broker*>(brkr->brkr().code, brkr));
	}

	return 0;
}

int brokers::init(const std::string &workdir, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	//get sub directories from configure path, suppose file name is broker name
	std::string brokersdir = cube::path::make(workdir, DIR);
	std::vector<std::string> names = cube::fd::dirs(brokersdir);

	//load each broker
	for (size_t i = 0; i < names.size(); i++) {
		broker *brkr = new broker(broker_t(names[i], names[i], "", false));
		std::string errmsg("");
		int err = brkr->init(cube::path::make(brokersdir, names[i]), &errmsg);
		if (err != 0) {
			_brokers.insert(std::pair<std::string, broker*>(names[i], brkr));
		} else {
			delete brkr;
			cube::safe_append<std::string>(error, errmsg);
		}
	}
	return 0;
}

int brokers::add(const broker_t &brkr, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);
	std::map<std::string, broker*>::iterator iter = _brokers.find(brkr.code);
	if (iter != _brokers.end()) {
		return 0; //broker exists
	}

	//insert new broker to database
	int err = _dao->insert(brkr, error);
	if (err != 0) {
		return -1;
	}

	//get complete broker from database
	broker_t newbrkr;
	err = _dao->select(brkr.code, newbrkr, error);
	if (err != 0) {
		return -1;
	}

	//add new broker to brokers
	_brokers.insert(std::pair<std::string, broker*>(newbrkr.code, new broker(newbrkr)));

	return 0;
}

int brokers::select(const std::string &code, server::type type, server &server, std::string *error) {
	std::lock_guard<std::mutex> lock(_mutex);

	std::map<std::string, broker*>::iterator iter = _brokers.find(code);
	if (iter != _brokers.end()) {
		return iter->second->select(type, server, error);
	} else {
		cube::throw_assign<brokers::error>(error, cube::str::format("broker %s not exist.", code.c_str()));
	}

	return -1;
}

int brokers::destroy() {
	std::lock_guard<std::mutex> lock(_mutex);
	
	//free all brokers
	std::map<std::string, broker*>::iterator iter = _brokers.begin(), iterend = _brokers.end();
	while (iter != iterend) {
		delete iter->second;
	}
	_brokers.clear();

	//free dao
	if (_dao != 0) {
		delete _dao;
		_dao = 0;
	}

	return 0;
}
//////////////////////////////////////brokerdao class////////////////////////////////////////////
int brokerdao::select(int id, std::vector<dept> &depts, std::string *error) {
	//sql to execute
	const char* sql = "select dept_id, code, name, disable, unix_timestamp(ctime) as ctime from tb_dept where broker=?";

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
		cube::safe_delete<sql::ResultSet>(res);

		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

int brokerdao::select(int id, server::type stype, std::vector<server> &servers, std::string *error) {
	//sql to execute
	const char* sql = "select server_id, name, host, port, type, disable, unix_timestamp(ctime) as ctime from tb_server where brokerd=? and type=?";

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
		cube::safe_delete<sql::ResultSet>(res);

		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}


//////////////////////////////////////brokersdao class////////////////////////////////////////////
int brokersdao::insert(const broker_t &brkr, std::string *error) {
	//sql to execute
	const char* sql = "insert into tb_broker(code, name, version, disable) values(?, ?, ?, ?)";

	//query variables
	sql::PreparedStatement *stmt = 0;
	try {
		stmt = conn()->prepareStatement(sql);

		stmt->setString(1, brkr.code.c_str());
		stmt->setString(2, brkr.name.c_str());
		stmt->setString(3, brkr.version.c_str());
		stmt->setBoolean(4, brkr.disable);
		stmt->executeUpdate();

		delete stmt;

	} catch (sql::SQLException &e) {
		cube::safe_delete<sql::PreparedStatement>(stmt);
		cube::throw_assign<db::error>(error, e.what());
		return -1;
	}

	return 0;
}

int brokersdao::select(std::vector<broker_t> &brokers, std::string *error) {
	//sql to execute
	const char* sql = "select broker_id, code, name, version, disable, unix_timestamp(ctime) as ctime from tb_broker;";

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

			brokers.push_back(broker_t(id, code, name, version, disable, ctime));
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

int brokersdao::select(const std::string &code, broker_t &brkr, std::string *error) {
	//sql to execute
	const char* sql = "select broker_id, code, name, version, disable, unix_timestamp(ctime) as ctime from tb_broker where code=?";

	//query variables
	sql::PreparedStatement *stmt = 0;
	sql::ResultSet *res = 0;

	try {
		stmt = conn()->prepareStatement(sql);
		stmt->setString(1, code.c_str());

		res = stmt->executeQuery();
		if (res->next()) {
			int id = res->getInt("broker_id");
			std::string code = res->getString("code").c_str();
			std::string name = res->getString("name").c_str();
			std::string version = res->getString("version").c_str();
			bool disable = res->getBoolean("disable");
			uint ctime = res->getUInt("ctime");			

			brkr = broker_t(id, code, name, version, disable, ctime);
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
END_SERVICE_NAMESPACE
