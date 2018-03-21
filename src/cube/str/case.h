#pragma once
#include <string>
#include "cube\ns.h"
BEGIN_CUBE_STR_NS
/*
*	transfer the letter in string to upper case
*@param str: in, string to transfer
*@return:
*	string with upper case
*/
std::string upper(const std::string &str);
std::wstring upper(const std::wstring &str);

/*
*	transfer the letter in string to lower case
*@param str: in, string to transfer
*@return:
*	string with lower case
*/
std::string lower(const std::string &str);
std::wstring lower(const std::wstring &str);
END_CUBE_STR_NS
