#pragma once
#include "cube.h"

BEGIN_CUBE_NAMESPACE
static const char* SPACES = "\t\f\v\n\r\t ";
class str
{
public:
	str();
	~str();
	
	/*
	*	functions to classify characters
	*@param str: in, string to classify
	*@return:
	*	true if match the classifier, otherwise false
	*/
	static bool isnum(const char* str);
	static bool isdigit(const char* str);
	static bool isxdigit(const char* str);
	static bool isalpha(const char* str);
	static bool isalnum(const char* str);
	static bool islower(const char* str);
	static bool isupper(const char* str);
	static bool isfloat(const char* str);

	/*
	*	transfer the letter in string to upper case
	*@param str: in, string to transfer
	*@return:
	*	string with upper case
	*/
	static std::string upper(const std::string &str);
	static std::wstring upper(const std::wstring &str);

	/*
	*	transfer the letter in string to lower case
	*@param str: in, string to transfer
	*@return:
	*	string with lower case
	*/
	static std::string lower(const std::string &str);
	static std::wstring lower(const std::wstring &str);

	/*
	*	transfer hexadecimal value[0,15] to hexadecimal character[0123456789ABCDEF]
	*@param xdigit: in, hexadecimal value [0,15]
	*@return:
	*	hexadecimal character, otherwise -1
	*/
	static char xalpha(int xdigit);

	/*
	*	transfer hexadecimal character[0123456789ABCDEF] to hexadecimal value[0,15]
	*@param xalpha: in, hexadecimal character[0123456789ABCDEF]
	*@return:
	*	hexadecimal value, otherwise -1
	*/
	static int xdigit(char xalpha);

	/*
	*	transfer value to hexadecimal string, e.g. 0xAB->'AB'
	*@param val: in, value
	*@return:
	*	hex string of value
	*/
	static std::string hex(int val);
	static std::string hex(char val);
	static std::string hex(short val);
	static std::string hex(long val);
	static std::string hex(long long val);

	/*
	*	transfer byte data to hex string
	*@param data: in, byte data
	*@param sz: in, size of data
	*@return:
	*	hex string, or empty string when transfer failed.
	*/
	static std::string hex(const byte *data, int sz);
	static std::string hex(const std::string &data);


	/*
	*	transfer byte hexadecimal character to byte, e.g. 'AF'->0xAF
	*@param high: in, high hexadecimal alpha
	*@param low: in, low hexadecimal aplpha
	*@return:
	*	byte value
	*/
	static char bytes(char high, char low);

	/*
	*	transfer hex string to byte data
	*@param str: in, hex string
	*@param len: in, length of hex string
	*@return:
	*	byte data, or size 0 when transfer failed.
	*/
	static std::string bytes(const char* str);
	static std::string bytes(const char* str, int len);
	static std::string bytes(const std::string &str);

	/*
	*	strip packs of input string with both side / left side / right side
	*@param str: in, string to strip
	*@param len: in, length of string
	*@param packs: in, packs to strip, default space characters
	*@return:
	*	striped string
	*/
	static std::string strip(const char* str, const char* packs = SPACES);
	static std::string strip(const std::string &str, const char* packs = SPACES);
	static std::string strip(const char *str, int len, const char* packs= SPACES);
	
	static std::string lstrip(const char* str, const char* packs = SPACES);
	static std::string lstrip(const std::string &str, const char* packs = SPACES);
	static std::string lstrip(const char *str, int len, const char* packs = SPACES);

	static std::string rstrip(const char* str, const char* packs = SPACES);
	static std::string rstrip(const std::string &str, const char* packs = SPACES);
	static std::string rstrip(const char *str, int len, const char* packs = SPACES);
	

	/*
	*	format string
	*@param format: in, format string
	*@...: in, arguments meet the format
	*@return:
	*	formated string
	*/
	static std::string format(const char *format, ...);

	/*
	*	convert numeric value to string
	*@param value: numberic value
	*/
	static std::string tostr(int value);
	static std::string tostr(float value);
};
END_CUBE_NAMESPACE