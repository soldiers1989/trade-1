#pragma once
#include "cube.h"
#include <vector>

BEGIN_CUBE_NAMESPACE
static const char* SPACES = "\t\f\v\n\r\t ";
class str {
public:
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
	static std::string strip(const char *str, int len, const char* packs = SPACES);

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
	/*
	*	convert numberic(int, long, float, double) to string
	*@param val: number input value
	*@param fmt: format of input value
	*@return:
	*	string of value
	*/
	template<class T> static std::string tostr(const T val, const char* fmt);


	/*
	*	print table data to console
	*@param table: in, table want to print
	*@return
	*	void
	*/
	static void print(const std::vector<std::vector<std::string>> &table, int colwidth = 10);

	/*
	*	check if input string is empty
	*@param str: string to check
	*@return:
	*	true if input string is empty, otherwise false
	*/
	static bool empty(const char* str);

	/*
	*	split a string by character/characters
	*@param str: string to be splited
	*@param sep: character seperator
	*@param spes: characters used to seperate
	*@return:
	*	split result
	*/
	static std::vector<std::string> _split(const char *str, const char ch);
	static std::vector<std::string> split(const std::string& str, const char ch);
	static std::vector<std::string> splits(const std::string& str, const std::string& chs);

	/*
	*	split a string by string seperator
	*@param str: string to be splited
	*@param sep: character seperator
	*@return:
	*	split result
	*/
	static std::vector<std::string> _split(const char *str, const char *sep);
	static std::vector<std::string> split(const std::string &str, const std::string &sep);

	/*
	*	split a string to table structure by row and column seperator
	*@param str: string to be splited
	*@param seprow: row seperator
	*@param sepcol: column seperator
	*@return:
	*	split result
	*/
	static std::vector<std::vector<std::string>> split(const std::string &str, const std::string &seprow, const std::string &sepcol);

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