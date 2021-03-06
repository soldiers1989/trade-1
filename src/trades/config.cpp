#include "trades\config.h"
#include "cube\log\logger.h"
BEGIN_TRADES_NAMESPACE
//initalize default config
std::string config::wdir = "./";
unsigned short config::port = 80;
int config::workers = 1;
int config::idle = 30;
std::string config::allowips = "";

std::string config::alias_enable = "false";
std::string config::alias_config = "./alias.ini";

std::string config::charset = "gbk";
std::string config::locale = "chs";
int config::codepage = 54936; //gb18030

int config::logtype = (int)cube::log::output::file;
int config::loglvl = (int)cube::log::level::debug;
std::string config::logdir = "./log";
std::string config::logname = "trade";
int config::logroll = (int)cube::log::roll::daily;
uint config::logfsz = (uint)-1;

//initalize static object
cube::cfg::ini config::_ini;

int config::load(const std::string &path) {
	//load ini file
	int err = _ini.load(path.c_str());
	if (err != 0) {
		return -1;
	}

	config::wdir = _ini.get_string_value("trade", "wdir", config::wdir.c_str());
	config::port = _ini.get_integer_value("trade", "port", config::port);
	config::workers = _ini.get_integer_value("trade", "workers", config::workers);
	config::idle = _ini.get_integer_value("trade", "idle", config::idle);
	config::allowips = _ini.get_string_value("trade", "allowips", config::allowips.c_str());

	config::alias_enable = _ini.get_string_value("alias", "enable", config::alias_enable.c_str());
	config::alias_config = _ini.get_string_value("alias", "config", config::alias_config.c_str());

	config::charset = _ini.get_string_value("lang", "charset", config::charset.c_str());
	config::locale = _ini.get_string_value("lang", "locale", config::locale.c_str());
	config::codepage = _ini.get_integer_value("lang", "codepage", config::codepage);

	config::logtype = _ini.get_integer_value("log", "type", config::logtype);
	config::loglvl = _ini.get_integer_value("log", "level", config::loglvl);
	config::logdir = _ini.get_string_value("log", "dir", config::logdir.c_str());
	config::logname = _ini.get_string_value("log", "name", config::logname.c_str());
	config::logroll = _ini.get_integer_value("log", "roll", config::logroll);
	config::logfsz = (uint)_ini.get_integer_value("log", "size", config::logfsz);

	return 0;
}
END_TRADES_NAMESPACE
