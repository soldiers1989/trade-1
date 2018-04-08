#pragma once
#include <string>
#include "cube\ns.h"
#include "cube\type.h"
BEGIN_CUBE_STR_NS
int iconv(std::string &dest, const std::string &src, uint fromcp, uint tocp);
int iconv(std::string &dest, const std::string &src, const char *from, const char *to);
END_CUBE_STR_NS
