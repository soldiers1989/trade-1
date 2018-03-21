#pragma once
#include <string>
#include "cube\ns.h"
BEGIN_CUBE_STR_NS
/*
*	transfer hexadecimal value[0,15] to hexadecimal character[0123456789ABCDEF]
*@param xdigit: in, hexadecimal value [0,15]
*@return:
*	hexadecimal character, otherwise -1
*/
char xalpha(int xdigit);

/*
*	transfer hexadecimal character[0123456789ABCDEF] to hexadecimal value[0,15]
*@param xalpha: in, hexadecimal character[0123456789ABCDEF]
*@return:
*	hexadecimal value, otherwise -1
*/
int xdigit(char xalpha);

/*
*	convert numeric value to string
*@param value: numberic value
*/
std::string string(int value);
std::string string(float value);

/*
*	convert numberic(int, long, float, double) to string
*@param val: number input value
*@param fmt: format of input value
*@return:
*	string of value
*/
template<class T> static std::string string(const T val, const char* fmt);
END_CUBE_STR_NS
