#pragma once
#include <string>
#include "cube\type.h"
#include "cube\cfg\ini.h"
#include "quotes\stdqots.h"
BEGIN_QUOTES_NAMESPACE
class config {
public:
	//trade working dir
	static std::string wdir;

	//service port
	static unsigned short port;

	//service workers
	static int workers;
	
	//session idle time limit
	static int idle;

	//allow ip address
	static std::string allowips;

	//alias configure file
	static std::string alias_enable;
	static std::string alias_config;

	//response data charset
	static std::string charset;
	//response data locale
	static std::string locale;
	//response data code page
	static int codepage;
public:
	//load configure file
	static int load(const std::string &path);

private:
	//ini file
	static cube::cfg::ini _ini;
};
END_QUOTES_NAMESPACE
