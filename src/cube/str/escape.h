#pragma once
#include <string>
#include "cube\ns.h"
BEGIN_CUBE_STR_NS
/*
*	escape a charater to format "%XY" string
*@param ch: in, charater to escape
*@return:
*	escaped string of character
*/
std::string escape(char ch);

/*
*	escape(to %XY) character in string
*@param str: in, string to process
*@param len: in, length of string
*@return:
*	escaped string
*/
std::string escape(const char* str);
std::string escape(const std::string &str);
std::string escape(const char *str, int len);

/*
*	unescape escaped string
*@param str: in, string to process
*@param len: in, length of string
*@return:
*	unescaped string
*/
std::string unescape(const char* str);
std::string unescape(const std::string &str);
std::string unescape(const char *str, int len);
END_CUBE_STR_NS
