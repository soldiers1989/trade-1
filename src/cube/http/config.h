#pragma once
#include <string>
#include "cube\ns.h"
BEGIN_CUBE_HTTP_NS
class config {
public:
	static std::string server;
	static std::string domain;
	static std::string default_charset;

	static int max_entity_length;
};
END_CUBE_HTTP_NS
