#pragma once
#include "trade\trade.h"
#include "cube\cfg\ini.h"
#include "trades\stdtrds.h"
BEGIN_TRADES_NAMESPACE
class alias {
public:
	virtual ~alias() {}

	//get singleton instance
	static alias *instance();

	/*
	*	load alias configure
	*@param cfg: in, conigure file path
	*@return:
	*	0 for success, otherwise for failure
	*/
	int load(const char *cfg);

	/*
	*	process table result by alias
	*@param tbl: table data with table header as the first line
	*@return:
	*	alias result
	*/
	trade::table process(const trade::table &tbl);

	/*
	*	check if alias has enabled
	*/
	bool enabled();

	/*
	*	disable alias convert
	*/
	void disable();

private:
	alias() : _enabled(false){}

private:
	//singleton instance of alias
	static alias *_inst;

	//enable flag for alias
	bool _enabled;

	//alias->name of table column name
	std::map<std::string, std::string> _alias;
};
END_TRADES_NAMESPACE
