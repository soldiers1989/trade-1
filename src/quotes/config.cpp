#include "quotes\config.h"
BEGIN_QUOTES_NAMESPACE
//initalize default config
std::string config::wdir = "./";
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
	config::port = _ini.get_integer_value("trade", "port", 80);
	config::allowips = _ini.get_string_value("trade", "allowips", "");

	return 0;
}
END_QUOTES_NAMESPACE
