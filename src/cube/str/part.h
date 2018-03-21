#pragma once
#include <vector>
#include <string>
#include "cube\ns.h"
BEGIN_CUBE_STR_NS
/*
*	split a string by delimiter characters
*@param str: in, string to be splited
*@param sz: in, size in string to splited
*@param delimiters: in, delimiter characters
*@param result: in/out, split result
*@param maxwant: in, max split unit wanted
*@return:
*	split result
*/
std::vector<std::string> part(const char *str, const char *delimiters, int maxwant = INT_MAX);
void part(const char *str, const char *delimiters, std::vector<std::string> &result, int maxwant = INT_MAX);
std::vector<std::string> part(const char *str, int sz, const char *delimiters, int maxwant = INT_MAX);
void part(const char *str, int sz, const char *delimiters, std::vector<std::string> &result, int maxwant = INT_MAX);
END_CUBE_STR_NS
