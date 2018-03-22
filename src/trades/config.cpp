#include "trades\config.h"
BEGIN_TRADES_NAMESPACE
//initalize default config
std::string config::wdir = "./";
std::string config::token = "";
unsigned short config::port = 80;
std::string config::allowips = "";

//initalize static object
cube::cfg::ini config::_ini;

int config::load(const std::string &path) {
	//load ini file
	int err = _ini.load(path.c_str());
	if (err != 0) {
		return -1;
	}

	config::wdir = _ini.get_string_value("trade", "wdir", "./");
	config::token = _ini.get_string_value("trade", "token", "");
	config::port = _ini.get_integer_value("trade", "port", 80);
	config::allowips = _ini.get_string_value("trade", "allowips", "");

	return 0;
}
END_TRADES_NAMESPACE
