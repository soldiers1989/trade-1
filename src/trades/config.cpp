#include "trades\config.h"
BEGIN_TRADES_NAMESPACE
//initalize default config
std::string config::wdir = "./";
unsigned short config::port = 80;
int config::workers = 1;
int config::idle = 30;
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
	config::port = _ini.get_integer_value("trade", "port", 80);
	config::workers = _ini.get_integer_value("trade", "workers", 1);
	config::idle = _ini.get_integer_value("trade", "idle", 30);
	config::allowips = _ini.get_string_value("trade", "allowips", "");

	return 0;
}
END_TRADES_NAMESPACE
