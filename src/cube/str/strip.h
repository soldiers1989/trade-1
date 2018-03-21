#pragma once
#include <string>
#include "cube\ns.h"
BEGIN_CUBE_STR_NS
static const char* SPACES = "\t\f\v\n\r\t ";
/*
*	strip packs of input string with both side / left side / right side
*@param str: in, string to strip
*@param len: in, length of string
*@param packs: in, packs to strip, default space characters
*@return:
*	striped string
*/
std::string strip(const char* str, const char* packs = SPACES);
std::string strip(const std::string &str, const char* packs = SPACES);
std::string strip(const char *str, int len, const char* packs = SPACES);

std::string lstrip(const char* str, const char* packs = SPACES);
std::string lstrip(const std::string &str, const char* packs = SPACES);
std::string lstrip(const char *str, int len, const char* packs = SPACES);

std::string rstrip(const char* str, const char* packs = SPACES);
std::string rstrip(const std::string &str, const char* packs = SPACES);
std::string rstrip(const char *str, int len, const char* packs = SPACES);
END_CUBE_STR_NS
