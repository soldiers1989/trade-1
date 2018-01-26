#include "config.h"
BEGIN_SVR_NAMESPACE
BEGIN_MGR_NAMESPACE
//initalize static object
cube::ini cfg::_ini;

cfg::cdb cfg::db;
cfg::chttp cfg::http;

int cfg::load(const std::string &path) {
	//load ini file
	int err = _ini.load(path.c_str());
	if (err != 0) {
		return -1;
	}

	//read http configure
	http.port = _ini.get_integer_value("http", "port", 80);

	//read db configure
	db.host = _ini.get_string_value("mysql", "host", "localhost");
	db.user = _ini.get_string_value("mysql", "user", "root");
	db.pwd = _ini.get_string_value("mysql", "pwd", "");
	db.name = _ini.get_string_value("mysql", "name", "");
	db.port = (ushort)_ini.get_integer_value("mysql", "port", 3306);

	return 0;
}
END_MGR_NAMESPACE
END_SVR_NAMESPACE
