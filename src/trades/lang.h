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
	*	convert source string to target character encoded string
	*@param dest: in, destination string converted
	*@param src: in, source string to be converted
	*@return:
	*	0 for success, otherwise faliure
	*/
	std::string conv(const std::string &src);
	int conv(std::string &dest, const std::string &src);

	/*
	*	process table result by alias
	*@param tbl: table data with table header as the first line
	*@return:
	*	0 for success, otherwise faliure
	*/
	trade::table process(const trade::table &tbl);
	void process(trade::table &result, const trade::table &tbl);

	/*
	*	test if need convert response data
	*/
	bool needconv();

	/*
	*	get current charset of response
	*/
	static const std::string& charset();
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