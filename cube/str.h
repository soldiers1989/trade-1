#pragma once
#include <vector>
#include <string>
#include "cube\ns.h"

BEGIN_CUBE_NAMESPACE
class str {
public:
	/*
	*	split a string by character seperator
	*@param str: string to be splited
	*@param sep: character seperator
	*@return:
	*	split result
	*/
	static std::vector<std::string> split(const char* str, const char sep);

	/*
	*	split a string by string seperator
	*@param str: string to be splited
	*@param sep: character seperator
	*@return:
	*	split result
	*/
	static std::vector<std::string> split(const char* str, const char* sep);

	/*
	*	split a string by character seperator
	*@param str: string to be splited
	*@param sep: character seperator
	*@return:
	*	split result
	*/
	static std::vector<std::string> split(const std::string& str, const char sep);

	/*
	*	split a string by string seperator
	*@param str: string to be splited
	*@param sep: character seperator
	*@return:
	*	split result
	*/
	static std::vector<std::string> split(const std::string& str, const std::string& sep);
};
END_CUBE_NAMESPACE
