#pragma once
#include "quote\quote1.h"
#include "quotes\config.h"
#include "quotes\stdqots.h"
BEGIN_QUOTES_NAMESPACE
class quoter {
public:
	virtual ~quoter(){

	}
	static quoter *instance();

	int init();

	int connect(const std::string &ip, ushort port, quote::table &result, std::string *error);

	int query_security_count(int market, int &count, std::string *error);

	int query_security_list(int market, int start, int &count, quote::table &result, std::string *error);

	int query_security_kline(int line, int market, const std::string &zqdm, int start, int &count, quote::table &result, std::string *error);

	int query_index_kline(int line, int market, const std::string &zqdm, int start, int &count, quote::table &result, std::string *error);

	int query_current_time_data(int market, const std::string &zqdm, quote::table &result, std::string *error);

	int query_current_deal_data(int market, const std::string &zqdm, int start, int &count, quote::table &result, std::string *error);

	int query_current_quote_data(int market, const std::string &zqdm, quote::table &result, std::string *error);

	int disconnect();

	bool connected();

	int destroy();

private:
	quoter() : _connected(false){}

private:
	static quoter *_instance;

	//quote connect
	quote::quote1 *_quote;

	//connect flag
	bool _connected;
};
END_QUOTES_NAMESPACE
