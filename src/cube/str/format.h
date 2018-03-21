#pragma once
#include <string>
#include "cube\ns.h"
BEGIN_CUBE_STR_NS
/*
*	format string
*@param format: in, format string
*@...: in, arguments meet the format
*@return:
*	formated string
*/
std::string format(const char *format, ...);
void format(std::string &result, const char *format, ...);
END_CUBE_STR_NS
