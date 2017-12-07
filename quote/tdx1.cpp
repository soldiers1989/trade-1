#include "tdx1.h"
#include "error.h"
#include "cube\str.h"

BEGIN_QUOTE_NAMESPACE
tdx1::tdx1() : _quote(0)
{
}


tdx1::~tdx1()
{
}

int tdx1::init(std::string *error/* = 0*/) {
	if (_quote == 0) {
		_quote = new tdxdll1();
		int err = _quote->load(TDX_QUOTE1_DLL, error);
		if (err != 0) {
			delete _quote;
			_quote = 0;
			return -1;
		}
	}

	//initialize the result and error buffer holder
	for (int i = 0; i < TDX_BATCH_LIMIT; i++) {
		_results[i] = new char[TDX_BUFFER_SIZE_RESULT];
		_errors[i] = new char[TDX_BUFFER_SIZE_ERROR];
	}

	return 0;
}

int tdx1::connect(std::string ip, ushort port, table_t &result, std::string &error) {
	//connect to server
	bool res = _quote->TdxHq_Connect(ip.c_str(), port, _results[0], _errors[0]);
	if (!res) {
		error = _errors[0];
		return -1;
	}

	//parse result
	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_security_count(market_t market, int &count, std::string &error) {
	short scount = 0;
	bool res = _quote->TdxHq_GetSecurityCount((byte)market, scount, _errors[0]);
	if (!res) {
		error = _errors[0];
		return -1;
	}

	count = scount;

	return 0;
}

int tdx1::query_security_list(market_t market, int start, int &count, table_t &result, std::string &error) {
	short scount = 0;
	bool res = _quote->TdxHq_GetSecurityList((byte)market, (short)start, scount, _results[0], _errors[0]);
	if (!res) {
		error = _errors[0];
		return -1;
	}

	count = scount;
	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_security_kline(kline_t line, market_t market, std::string zqdm, int start, int &count, table_t &result, std::string &error) {
	short scount = 0;
	bool res = _quote->TdxHq_GetSecurityBars((byte)line, (byte)market, zqdm.c_str(), (short)start, scount, _results[0], _errors[0]);
	if (!res) {
		error = _errors[0];
		return -1;
	}

	count = scount;
	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_index_kline(kline_t line, market_t market, std::string zqdm, int start, int &count, table_t &result, std::string &error) {
	short scount = 0;
	bool res = _quote->TdxHq_GetIndexBars((byte)line, (byte)market, zqdm.c_str(), (short)start, scount, _results[0], _errors[0]);
	if (!res) {
		error = _errors[0];
		return -1;
	}

	count = scount;
	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);
	return 0;
}

int tdx1::query_current_time_data(market_t market, std::string zqdm, table_t &result, std::string &error) {
	bool res = _quote->TdxHq_GetMinuteTimeData((byte)market, zqdm.c_str(), _results[0], _errors[0]);
	if (!res) {
		error = _errors[0];
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_history_time_data(market_t market, std::string zqdm, std::string date, table_t &result, std::string &error) {
	bool res = _quote->TdxHq_GetHistoryMinuteTimeData((byte)market, zqdm.c_str(), atoi(date.c_str()), _results[0], _errors[0]);
	if (!res) {
		error = _errors[0];
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_current_deal_data(market_t market, std::string zqdm, int start, int &count, table_t &result, std::string &error) {
	short scount = 0;
	bool res = _quote->TdxHq_GetTransactionData((byte)market, zqdm.c_str(), (short)start, scount, _results[0], _errors[0]);
	if (!res) {
		error = _errors[0];
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_history_deal_data(market_t market, std::string zqdm, std::string date, int start, int &count, table_t &result, std::string &error) {
	short scount = 0;
	bool res = _quote->TdxHq_GetHistoryTransactionData((byte)market, zqdm.c_str(), (short)start, scount, atoi(date.c_str()), _results[0], _errors[0]);
	if (!res) {
		error = _errors[0];
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_current_quote_data(market_t market, std::string zqdm, table_t &result, std::string &error) {
	//adapt for batch api
	std::vector<security_t> securities;

	//set security information
	securities.push_back(security_t(market, zqdm));

	return  query_current_quote_data(securities, result, error);
}

int tdx1::query_current_quote_data(std::vector<security_t> securities, table_t &result, std::string &error) {
	//batch query count
	short count = (short)securities.size();

	//query input data
	byte markets[TDX_BATCH_LIMIT];
	const char* codes[TDX_BATCH_LIMIT];
	for (short i = 0; i < count; i++) {
		markets[i] = (byte)securities[i].market;
		codes[i] = securities[i].code.c_str();
	}

	// query server
	bool res = _quote->TdxHq_GetSecurityQuotes(markets, codes, count, _results[0], _errors[0]);
	if (!res) {
		error = _errors[0];
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_f10_category(market_t market, std::string zqdm, table_t &result, std::string &error) {
	bool res = _quote->TdxHq_GetCompanyInfoCategory((byte)market, zqdm.c_str(), _results[0], _errors[0]);
	if (!res) {
		error = _errors[0];
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_f10_content(market_t market, std::string zqdm, std::string file, int start, int length, table_t &result, std::string &error) {

	short scount = 0;
	bool res = _quote->TdxHq_GetCompanyInfoContent((byte)market, zqdm.c_str(), file.c_str(), start, length,  _results[0], _errors[0]);
	if (!res) {
		error = _errors[0];
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_xdxr_data(market_t market, std::string zqdm, table_t &result, std::string &error) {
	bool res = _quote->TdxHq_GetXDXRInfo((byte)market, zqdm.c_str(), _results[0], _errors[0]);
	if (!res) {
		error = _errors[0];
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_finance_data(market_t market, std::string zqdm, table_t &result, std::string &error) {
	bool res = _quote->TdxHq_GetFinanceInfo((byte)market, zqdm.c_str(), _results[0], _errors[0]);
	if (!res) {
		error = _errors[0];
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::disconnect() {
	_quote->TdxHq_Disconnect();
	return 0;
}

int tdx1::destroy() {
	if (_quote != 0) {
		_quote->free();
		delete _quote;
		_quote = 0;
	}

	for (int i = 0; i < TDX_BATCH_LIMIT; i++) {
		if (_results[i] != 0) {
			delete[]_results[i];
			_results[i] = 0;
		}

		if (_errors[i] != 0) {
			delete[]_errors[i];
			_errors[i] = 0;
		}
	}
	return 0;
}
END_QUOTE_NAMESPACE