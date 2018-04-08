#pragma once
#include "trade\trade.h"
#include "trades\stdtrds.h"
BEGIN_TRADES_NAMESPACE
class lang {
public:
	virtual ~lang() {}

	/*
	*	get sinable
	*/
	static lang* instance();

	/*
	*	set response target character code page & charset
	*/
	void set(int codepage, const std::string &charset);

	/*
	*	process table result by alias
	*@param tbl: table data with table header as the first line
	*@return:
	*	alias result
	*/
	int process(trade::table &result, const trade::table &tbl);

	/*
	*	test if need convert response data
	*/
	bool needconv();

private:
	lang() : _codepage(CODEPAGE), _charset(CHARSET){}

private:
	//singleton instance
	static lang *_inst;
	//original code page
	static int CODEPAGE;
	//original charset
	static std::string CHARSET;

	//response code page
	int _codepage;
	std::string _charset;
};
END_TRADES_NAMESPACE
