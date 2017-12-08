#pragma once
#include "stdqot.h"
BEGIN_QUOTE_NAMESPACE
typedef std::vector<std::vector<std::string>> table;

//market class
typedef enum class market {
	sz = 0, //shanghai exchange markte
	sh = 1 //shenzhen exchange market
} market;

//kline class
typedef enum class kline {
	min5 = 0,
	min15 = 1,
	min30 = 2,
	hour = 3,
	day = 4,
	week = 5,
	month = 6,
	min = 7,
	min1 = 8,
	day1 = 9,
	quarter = 10,
	year = 11
} kline;

class security {
public:
	security(market mkt, const std::string &code) : mkt(mkt), code(code) {}
	~security() {}

public:
	market mkt; //market
	std::string code; //sercurity code
};
END_QUOTE_NAMESPACE
