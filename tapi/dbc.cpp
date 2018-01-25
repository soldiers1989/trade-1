#include "dbc.h"
#include "cube\str.h"
#include "cppconn\driver.h"
#include "cppconn\statement.h"
#include "cppconn\exception.h"
BEGIN_SEC_NAMESPACE
//////////////////////////////////db class//////////////////////////////////
int dbc::connect(const std::string &host, const std::string &user, const std::string &pwd, ushort port/* = 3306*/, std::string *error/* = 0*/) {
	try {
		//mysql url
		std::string url = cube::str::format("tcp://%s:%d/", host.c_str(), port);

		//connection mysql
		sql::Driver *driver = ::get_driver_instance();
		_connection = driver->connect(url.c_str(), user.c_str(), pwd.c_str());

		//connect success
		return 0;

	} catch (sql::SQLException &e) {
		cube::throw_assign<dbc::error>(error, e.what());
		return -1;
	}
}

int dbc::use(const std::string &db, std::string *error/* = 0*/) {
	try {

		//set database used
		_connection->setSchema(db.c_str());

	} catch (sql::SQLException &e) {
		cube::throw_assign<dbc::error>(error, e.what());
		return -1;
	}

	return 0;
}

int dbc::execute(const std::string &sql, std::string *error/* = 0*/) {
	sql::Statement *stmt = 0;
	try {
		stmt = _connection->createStatement();
		stmt->execute(sql.c_str());
		delete stmt;
		return 0;
	} catch (sql::SQLException &e) {
		if (stmt != 0)
			delete stmt;
		cube::throw_assign<dbc::error>(error, e.what());
		return -1;
	}
}

int dbc::close() {
	if (_connection != 0) {
		_connection->close();
		delete _connection;
		_connection = 0;
	}
	return 0;
}
//////////////////////////////////dao class//////////////////////////////////
dbc *dao::_dbc = 0;

void dao::setdb(dbc *dbc) {
	_dbc = dbc;
}

int dao::execute(const std::string &sql, std::string *error/* = 0*/) {
	if (_dbc == 0) {
		cube::throw_assign<dbc::error>(error, "database not specified.");
		return -1;
	}

	return _dbc->execute(sql, error);
}
END_SEC_NAMESPACE