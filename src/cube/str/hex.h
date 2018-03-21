#pragma once
#include <string>
#include "cube\ns.h"
#include "cube\type.h"
BEGIN_CUBE_STR_NS
/*
*	transfer value to hexadecimal string, e.g. 0xAB->'AB'
*@param val: in, value
*@return:
*	hex string of value
*/
std::string hex(int val);
std::string hex(char val);
std::string hex(short val);
std::string hex(long val);
std::string hex(long long val);

/*
*	transfer byte data to hex string
*@param data: in, byte data
*@param sz: in, size of data
*@return:
*	hex string, or empty string when transfer failed.
*/
std::string hex(const byte *data, int sz);
std::string hex(const std::string &data);


/*
*	transfer byte hexadecimal character to byte, e.g. 'A','F'->AF
*@param high: in, high hexadecimal alpha
*@param low: in, low hexadecimal aplpha
*@return:
*	byte value
*/
char octet(char high, char low);

/*
*	transfer hex string to byte data, 'AF01C8...'->AF 01 C8
*@param str: in, hex string
*@param len: in, length of hex string
*@return:
*	byte data, or size 0 when transfer failed.
*/
std::string octet(const std::string &str);
std::string octet(const char* str);
std::string octet(const char* str, int len);
END_CUBE_STR_NS

