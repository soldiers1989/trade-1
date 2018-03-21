#pragma once
#include <string>
#include "quote.h"

BEGIN_QUOTE_NAMESPACE
//level-1 quote class
class quote1 {
public:
	/*
	*	intialize quote api service
	*@param workdir: in, working directory
	*@param error: out, error message when failed
	*return:
	*	0 for success, otherwise < 0
	*/
	virtual int init(const std::string &workdir, std::string *error = 0) = 0;

	/*
	*	connect to the quotation service, must be invoke this method before using the other quotation
	*methods.
	*@param ip: in, remote server ip address, format: a.b.c.d
	*@param port: in, remote server port
	*@param result: out, connect result
	*@param error: out, error information if connect failed
	*@return:
	*	true if success, otherwise false
	*/
	virtual int connect(const std::string &ip, ushort port, table &result, std::string *error = 0) = 0;

	/*
	*	query security count by specified market
	*@param market: in, security market
	*@param count: out, security count
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_security_count(market mkt, int &count, std::string *error = 0) = 0;

	/*
	*	query security list of specified market
	*@param market: in, security market
	*@param start: in, start start from 0
	*@param count: out, security count returned
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_security_list(market mkt, int start, int &count, table &result, std::string *error = 0) = 0;

	/*
	*	query k-line data of specified security
	*@param line: in, k line type
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param start: int, start start from 0
	*@param count: out, security count returned
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_security_kline(kline line, market mkt, const std::string &zqdm, int start, int &count, table &result, std::string *error = 0) = 0;

	/*
	*	query k-line data of specified index
	*@param line: in, k line type
	*@param market: in, security market
	*@param zqdm: in, index code
	*@param start: int, start start from 0
	*@param count: out, security count returned
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_index_kline(kline line, market mkt, const std::string &zqdm, int start, int &count, table &result, std::string *error = 0) = 0;

	/*
	*	query current time-data of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_current_time_data(market mkt, const std::string &zqdm, table &result, std::string *error = 0) = 0;

	/*
	*	query history time-data of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param date: in, history date
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_history_time_data(market mkt, const std::string &zqdm, const std::string &date, table &result, std::string *error = 0) = 0;

	/*
	*	query currrent deal data of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param start: int, start start from 0
	*@param count: out, security count returned
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_current_deal_data(market mkt, const std::string &zqdm, int start, int &count, table &result, std::string *error = 0) = 0;

	/*
	*	query history deal data of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param date: in, history date
	*@param start: int, start start from 0
	*@param count: out, security count returned
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_history_deal_data(market mkt, const std::string &zqdm, const std::string &date, int start, int &count, table &result, std::string *error = 0) = 0;

	/*
	*	query current quote data of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_current_quote_data(market mkt, const std::string &zqdm, table &result, std::string *error = 0) = 0;


	/*
	*	query current quote data of specified securities
	*@param securities: in, securities to query
	*@param results: out, query results
	*@param errors: out, errors information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_current_quote_data(const std::vector<security> &securities, table &result, std::string *error = 0) = 0;

	/*
	*	query f10 category data of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_f10_category(market mkt, const std::string &zqdm, table &result, std::string *error = 0) = 0;

	/*
	*	query f10 content data of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param file: in, f10 file name, from f10 category
	*@param start: in, start start, from f10 category
	*@param length: in, length of category, from 10 category
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_f10_content(market mkt, const std::string &zqdm, const std::string &file, int start, int length, table &result, std::string *error = 0) = 0;

	/*
	*	query ex-dividend and ex-rights data of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_xdxr_data(market mkt, const std::string &zqdm, table &result, std::string *error = 0) = 0;


	/*
	*	query finance data of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_finance_data(market mkt, const std::string &zqdm, table &result, std::string *error = 0) = 0;

	/*
	*	disconnect from remote server
	*@return:
	*	always 0
	*/
	virtual int disconnect() = 0;

	/*
	*	destory quote api service
	*@return:
	*	always 0
	*/
	virtual int destroy() = 0;
};
END_QUOTE_NAMESPACE
