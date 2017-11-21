#pragma once
#include "quote2.h"
#include "tdxdll2.h"

BEGIN_QUOTE_NAMESPACE
class tdx2 : public quote2
{
public:
	tdx2();
	virtual ~tdx2();

	virtual int init(std::string *error = 0);

	virtual int connect(std::string ip, ushort port, table_t &result, std::string &error);

	virtual int query_security_count(market_t market, int &count, std::string &error);

	virtual int query_security_list(market_t market, int start, int &count, table_t &result, std::string &error);

	virtual int query_security_kline(kline_t line, market_t market, std::string zqdm, int start, int &count, table_t &result, std::string &error);

	virtual int query_index_kline(kline_t line, market_t market, std::string zqdm, int start, int &count, table_t &result, std::string &error);

	virtual int query_current_time_data(market_t market, std::string zqdm, table_t &result, std::string &error);

	virtual int query_history_time_data(market_t market, std::string zqdm, std::string date, table_t &result, std::string &error);

	virtual int query_current_deal_data(market_t market, std::string zqdm, int start, int &count, table_t &result, std::string &error);

	virtual int query_current_deal_detail(market_t market, std::string zqdm, int start, int &count, table_t &result, std::string &error);

	virtual int query_history_deal_data(market_t market, std::string zqdm, std::string date, int start, int &count, table_t &result, std::string &error);

	virtual int query_current_order_data(market_t market, std::string zqdm, int start, int &count, table_t &result, std::string &error);

	virtual int query_buysell_queue_data(market_t market, std::string zqdm, table_t &result, std::string &error);

	virtual int query_current_quote_data(market_t market, std::string zqdm, table_t &result, std::string &error);

	virtual int query_current_quote_data(std::vector<security_t> securities, table_t &result, std::string &error);

	virtual int query_current_quote10_data(market_t market, std::string zqdm, table_t &result, std::string &error);

	virtual int query_current_quote10_data(std::vector<security_t> securities, table_t &result, std::string &error);

	virtual int query_f10_category(market_t market, std::string zqdm, table_t &result, std::string &error);

	virtual int query_f10_content(market_t market, std::string zqdm, std::string file, int start, int length, table_t &result, std::string &error);

	virtual int query_xdxr_data(market_t market, std::string zqdm, table_t &result, std::string &error);

	virtual int query_finance_data(market_t market, std::string zqdm, table_t &result, std::string &error);

	virtual int disconnect();

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
