#include "quotes\config.h"
BEGIN_QUOTES_NAMESPACE
//initalize default config
std::string config::wdir = "./";
unsigned short config::port = 80;
int config::workers = 1;
std::string config::allowips = "";

//initalize static object
cube::cfg::ini config::_ini;

int config::load(const std::string &path) {
	//load ini file
	int err = _ini.load(path.c_str());
	if (err != 0) {
		return -1;
	}

	config::wdir = _ini.get_string_value("quote", "wdir", "./");
	config::port = _ini.get_integer_value("quote", "port", 80);
	config::workers = _ini.get_integer_value("quote", "workers", 1);
	config::allowips = _ini.get_string_value("quote", "allowips", "");

	return 0;
}
END_QUOTES_NAMESPACE
