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
	
	//allow ip address
	static std::string allowips;

public:
	//load configure file
	static int load(const std::string &path);

private:
	//ini file
	static cube::cfg::ini _ini;
};
END_QUOTES_NAMESPACE
