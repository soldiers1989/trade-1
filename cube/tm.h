#pragma once
#include "cube.h"
BEGIN_CUBE_NAMESPACE
class tm {
public:
	//time zone
	typedef enum class tz {utc = 0, local = 1} tz;
	//time unit for date
	typedef enum class unit { year = 0, month = 1, day = 2, hour = 3, min = 4, sec = 5, week = 6, yday = 7, mday = 8, wday = 9}unit;

public:
	/*
	*	get current time by specified unit
	*@param u: in, time unit, year|month|day|hour|min|sec
	*@return:
	*	current time unit value
	*/
	static int now(unit u, tz timezone = tz::local);

	/*
	*	get current time
	*@param timezone: in, time zone
	*@return:
	*	current time
	*/
	static struct ::tm *now(tz timezone = tz::local);

	/*
	*	get current time string by specified format
	*@param format: in, time string format
	*@return:
	*	time string
	*/
	static std::string now(const char* format, tz timezone = tz::local);
};
END_CUBE_NAMESPACE
