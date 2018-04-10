#pragma once
#include "quote\quote.h"
#include "cube\cfg\ini.h"
#include "quotes\stdqots.h"
BEGIN_QUOTES_NAMESPACE
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
	quote::table process(const quote::table &tbl);

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

	//need character charset converting column names(after alias)
	std::map<std::string, std::string> _convs;
};
END_QUOTES_NAMESPACE
