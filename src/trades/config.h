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
	
	//service port
	static unsigned short port;
	
	//service workers
	static int workers;

	//allow ip address
	static std::string allowips;

public:
	//load configure file
	static int load(const std::string &path);

private:
	//ini file
	static cube::cfg::ini _ini;
};
END_TRADES_NAMESPACE
