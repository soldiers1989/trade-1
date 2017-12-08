#pragma once
#include "quote2.h"
#include "tdxdll2.h"

BEGIN_QUOTE_NAMESPACE
class tdx2cfg {
public:
	static const int BATCH_LIMIT = 20;
	static const int BUFFER_SIZE_RESULT = 64 * 1024;
	static const int BUFFER_SIZE_ERROR = 4 * 1024;
	static const char* RESULT_ROW_SEP;
	static const char* RESULT_COL_SEP;
};

class tdx2 : public quote2
{
public:
	tdx2() : _quote(0) {}
	virtual ~tdx2() {}

	/*
	*	intialize quote api service
	*@param workdir: in, working directory
	*@param error: out, error message when failed
	*return:
	*	0 for success, otherwise < 0
	*/
	virtual int init(const std::string &workdir, std::string *error = 0);

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
	virtual int connect(const std::string &ip, ushort port, table &result, std::string *error = 0);

	/*
	*	query security count by specified market
	*@param market: in, security market
	*@param count: out, security count
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_security_count(market mkt, int &count, std::string *error = 0);

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
	virtual int query_security_list(market mkt, int start, int &count, table &result, std::string *error = 0);

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
	virtual int query_security_kline(kline line, market mkt, const std::string &zqdm, int start, int &count, table &result, std::string *error = 0);

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
	virtual int query_index_kline(kline line, market mkt, const std::string &zqdm, int start, int &count, table &result, std::string *error = 0);

	/*
	*	query current time-data of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_current_time_data(market mkt, const std::string &zqdm, table &result, std::string *error = 0);

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
	virtual int query_history_time_data(market mkt, const std::string &zqdm, const std::string &date, table &result, std::string *error = 0);

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
	virtual int query_current_deal_data(market mkt, const std::string &zqdm, int start, int &count, table &result, std::string *error = 0);

	/*
	*	query currrent deal detail of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param start: int, start start from 0
	*@param count: out, security count returned
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_current_deal_detail(market mkt, const std::string &zqdm, int start, int &count, table &result, std::string *error = 0);

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
	virtual int query_history_deal_data(market mkt, const std::string &zqdm, const std::string &date, int start, int &count, table &result, std::string *error = 0);

	/*
	*	query currrent order queue detail of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param start: int, start start from 0
	*@param count: out, security count returned
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_current_order_data(market mkt, const std::string &zqdm, int start, int &count, table &result, std::string *error = 0);

	/*
	*	query current buy and sell queue data of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_buysell_queue_data(market mkt, const std::string &zqdm, table &result, std::string *error = 0);

	/*
	*	query current quote data of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_current_quote_data(market mkt, const std::string &zqdm, table &result, std::string *error = 0);


	/*
	*	query current quote data of specified securities
	*@param securities: in, securities to query
	*@param results: out, query results
	*@param errors: out, errors information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_current_quote_data(const std::vector<security> &securities, table &result, std::string *error = 0);

	/*
	*	query current level 2 quote data of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_current_quote10_data(market mkt, const std::string &zqdm, table &result, std::string *error = 0);


	/*
	*	query current level 2 quote data of specified securities
	*@param securities: in, securities to query
	*@param results: out, query results
	*@param errors: out, errors information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_current_quote10_data(const std::vector<security> &securities, table &result, std::string *error = 0);

	/*
	*	query f10 category data of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_f10_category(market mkt, const std::string &zqdm, table &result, std::string *error = 0);

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
	virtual int query_f10_content(market mkt, const std::string &zqdm, const std::string &file, int start, int length, table &result, std::string *error = 0);

	/*
	*	query ex-dividend and ex-rights data of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_xdxr_data(market mkt, const std::string &zqdm, table &result, std::string *error = 0);


	/*
	*	query finance data of specified security
	*@param market: in, security market
	*@param zqdm: in, security code
	*@param result: out, query result
	*@param error: out, error information if query failed
	*@return:
	*	0 if success, otherwise < 0
	*/
	virtual int query_finance_data(market mkt, const std::string &zqdm, table &result, std::string *error = 0);


	/*
	*	disconnect from remote server
	*@return:
	*	always 0
	*/
	virtual int disconnect();

	/*
	*	destory quote api service
	*@return:
	*	always 0
	*/
	virtual int destroy();

private:
	//dll module api
	tdxdll2 *_quote;

	//result holder
	char *_results[TDX_BATCH_LIMIT];

	//error holder
	char *_errors[TDX_BATCH_LIMIT];
};
END_QUOTE_NAMESPACE
