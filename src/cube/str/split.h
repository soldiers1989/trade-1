#pragma once
#include <string>
#include <vector>
#include "cube\ns.h"
BEGIN_CUBE_STR_NS
/*
*	split a string by character/characters
*@param str: string to be splited
*@param sz: in, size in string to splited
*@param ch: character seperator
*@param chs: characters used to seperate
*@param keepempty: keep empty split string
*@return:
*	split result
*/
std::vector<std::string> split(const char *str, char ch);
void split(const char *str, char ch, std::vector<std::string> &result);
std::vector<std::string> split(const char *str, int sz, char ch);
void split(const char *str, int sz, char ch, std::vector<std::string> &result);

/*
*	split a string by string seperator
*@param str: in, string to be splited
*@param sz: in, size in string to splited
*@param ssz: in, size of seperator
*@param sep: in, character seperator
*@param keepempty: keep empty split string
*@return:
*	split result
*/
std::vector<std::string> split(const char *str, const char *sep);
void split(const char *str, const char *sep, std::vector<std::string> &result);

std::vector<std::string> split(const char *str, int sz, const char *sep);
void split(const char *str, int sz, const char *sep, std::vector<std::string> &result);

/*
*	split a string to table structure by row and column seperator
*@param str: string to be splited
*@param seprow: row seperator
*@param sepcol: column seperator
*@return:
*	split result
*/
std::vector<std::vector<std::string>> split(const std::string &str, const std::string &seprow, const std::string &sepcol);
void split(const std::string &str, const std::string &seprow, const std::string &sepcol, std::vector<std::vector<std::string>> &result);
END_CUBE_STR_NS
