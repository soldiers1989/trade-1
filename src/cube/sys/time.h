#pragma once
#include <string>
#include "cube\ns.h"
BEGIN_CUBE_SYS_TIME_NS
//time zone
enum class timezone { utc = 0, local = 1 };
//time unit for date
enum class timeunit { year = 0, month = 1, day = 2, hour = 3, min = 4, sec = 5, week = 6, yday = 7, mday = 8, wday = 9 };

/*
*	get current time by specified unit
*@param u: in, time unit, year|month|day|hour|min|sec
*@return:
*	current time unit value
*/
int now(timeunit u, timezone tz = timezone::local);

/*
*	get current time
*@param timezone: in, time zone
*@return:
*	current time
*/
struct tm *now(timezone tz = timezone::local);

/*
*	get current time string by specified format
*@param format: in, time string format
*@return:
*	time string
*/
std::string now(const char* format, timezone tz = timezone::local);

/*
*	get GMT time string, 
*/
std::string gmt(::time_t t);
END_CUBE_SYS_TIME_NS
