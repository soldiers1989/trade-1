/*
*	url - url module
*/
#pragma once
#include "cube.h"
BEGIN_CUBE_NAMESPACE
class url {
public:
	/*
	*	escape a charater to format "%XY" string
	*@param ch: in, charater to escape
	*@return:
	*	escaped string of character
	*/
	static std::string escape(char ch);

	/*
	*	escape(to %XY) character in string
	*@param str: in, string to process
	*@param len: in, length of string
	*@return:
	*	escaped string
	*/
	static std::string escape(const char* str);
	static std::string escape(const std::string &str);
	static std::string escape(const char *str, int len);

	/*
	*	unescape escaped string
	*@param str: in, string to process
	*@param len: in, length of string
	*@return:
	*	unescaped string
	*/
	static std::string unescape(const char* str);
	static std::string unescape(const std::string &str);
	static std::string unescape(const char *str, int len);
};
END_CUBE_NAMESPACE
