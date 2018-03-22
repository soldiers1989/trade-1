#pragma once
#include <string>
#include "cube\type.h"
#include "cube\cfg\ini.h"
#include "trades\stdtrds.h"
BEGIN_TRADES_NAMESPACE
class config {
public:
	//trade working dir
	static std::string wdir;
	
	//private token
	static std::string token;

	//service port
	static unsigned short port;
	
public:
	//load configure file
	static int load(const std::string &path);

private:
	//ini file
	static cube::cfg::ini _ini;
};
END_TRADES_NAMESPACE
