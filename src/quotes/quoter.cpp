#include "quote\tdx1.h"
#include "quotes\quoter.h"
#include "cube\log\log.h"

BEGIN_QUOTES_NAMESPACE
quoter *quoter::_instance = 0;
quoter *quoter::instance() {
	if (_instance == 0) {
		_instance = new quoter();
	}
	return _instance;
}

int quoter::init() {
	_quote = new quote::tdx1();
	std::string errmsg("");
	if (_quote->init(config::wdir, &errmsg) != 0) {
		cube::log::fatal("initialize quote module failed, %s", errmsg.c_str());
		return -1;
	}

	return 0;
}

int quoter::connect(const std::string &ip, ushort port, quote::table &result, std::string *error) {
	return _quote->connect(ip, port, result, error);
}

int quoter::query_security_count(int market, int &count, std::string *error) {
	return _quote->query_security_count((quote::market)market, count, error);
}

int quoter::query_security_list(int market, int start, int &count, quote::table &result, std::string *error) {
	return _quote->query_security_list((quote::market)market, start, count, result, error);
}

int quoter::query_security_kline(int line, int market, const std::string &zqdm, int start, int &count, quote::table &result, std::string *error) {
	return _quote->query_security_kline((quote::kline)line, (quote::market)market, zqdm, start, count, result, error);
}

int quoter::query_index_kline(int line, int market, const std::string &zqdm, int start, int &count, quote::table &result, std::string *error) {
	return _quote->query_index_kline((quote::kline)line, (quote::market)market, zqdm, start, count, result, error);
}

int quoter::query_current_time_data(int market, const std::string &zqdm, quote::table &result, std::string *error) {
	return _quote->query_current_time_data((quote::market)market, zqdm, result, error);
}

int quoter::query_current_deal_data(int market, const std::string &zqdm, int start, int &count, quote::table &result, std::string *error) {
	return _quote->query_current_deal_data((quote::market)market, zqdm, start, count, result, error);
}

int quoter::query_current_quote_data(int market, const std::string &zqdm, quote::table &result, std::string *error) {
	return _quote->query_current_quote_data((quote::market)market, zqdm, result, error);
}

int quoter::disconnect() {
	return _quote->disconnect();
}

int quoter::destroy() {
	return _quote->destroy();
}
END_QUOTES_NAMESPACE
