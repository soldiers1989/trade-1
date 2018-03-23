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

	int disconnect();

	int destroy();

private:
	quoter() {}

private:
	static quoter *_instance;

	//quote connect
	quote::quote1 *_quote;
};
END_QUOTES_NAMESPACE
