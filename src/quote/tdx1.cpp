#include "tdx1.h"
#include "cube\str.h"

BEGIN_QUOTE_NAMESPACE
const char* tdx1cfg::RESULT_ROW_SEP = "\n";
const char* tdx1cfg::RESULT_COL_SEP = "\t";

int tdx1::init(const std::string &workdir, std::string *error) {
	if (_quote == 0) {
		_quote = new tdxdll1();
		int err = _quote->load(workdir, error);
		if (err != 0) {
			delete _quote;
			_quote = 0;
			return -1;
		}
	}

	//initialize the result and error buffer holder
	for (int i = 0; i < tdx1cfg::BATCH_LIMIT; i++) {
		_results[i] = new char[tdx1cfg::BUFFER_SIZE_RESULT];
		_errors[i] = new char[tdx1cfg::BUFFER_SIZE_ERROR];
	}

	return 0;
}

int tdx1::connect(const std::string &ip, ushort port, table &result, std::string *error) {
	//connect to server
	bool res = _quote->TdxHq_Connect(ip.c_str(), port, _results[0], _errors[0]);
	if (!res) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	//parse result
	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_security_count(market mkt, int &count, std::string *error) {
	short scount = 0;
	bool res = _quote->TdxHq_GetSecurityCount((byte)mkt, scount, _errors[0]);
	if (!res) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	count = scount;

	return 0;
}

int tdx1::query_security_list(market mkt, int start, int &count, table &result, std::string *error) {
	short scount = 0;
	bool res = _quote->TdxHq_GetSecurityList((byte)mkt, (short)start, scount, _results[0], _errors[0]);
	if (!res) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	count = scount;
	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_security_kline(kline line, market mkt, const std::string &zqdm, int start, int &count, table &result, std::string *error) {
	short scount = 0;
	bool res = _quote->TdxHq_GetSecurityBars((byte)line, (byte)mkt, zqdm.c_str(), (short)start, scount, _results[0], _errors[0]);
	if (!res) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	count = scount;
	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_index_kline(kline line, market mkt, const std::string &zqdm, int start, int &count, table &result, std::string *error) {
	short scount = 0;
	bool res = _quote->TdxHq_GetIndexBars((byte)line, (byte)mkt, zqdm.c_str(), (short)start, scount, _results[0], _errors[0]);
	if (!res) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	count = scount;
	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);
	return 0;
}

int tdx1::query_current_time_data(market mkt, const std::string &zqdm, table &result, std::string *error) {
	bool res = _quote->TdxHq_GetMinuteTimeData((byte)mkt, zqdm.c_str(), _results[0], _errors[0]);
	if (!res) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_history_time_data(market mkt, const std::string &zqdm, const std::string &date, table &result, std::string *error) {
	bool res = _quote->TdxHq_GetHistoryMinuteTimeData((byte)mkt, zqdm.c_str(), atoi(date.c_str()), _results[0], _errors[0]);
	if (!res) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_current_deal_data(market mkt, const std::string &zqdm, int start, int &count, table &result, std::string *error) {
	short scount = 0;
	bool res = _quote->TdxHq_GetTransactionData((byte)mkt, zqdm.c_str(), (short)start, scount, _results[0], _errors[0]);
	if (!res) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_history_deal_data(market mkt, const std::string &zqdm, const std::string &date, int start, int &count, table &result, std::string *error) {
	short scount = 0;
	bool res = _quote->TdxHq_GetHistoryTransactionData((byte)mkt, zqdm.c_str(), (short)start, scount, atoi(date.c_str()), _results[0], _errors[0]);
	if (!res) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_current_quote_data(market mkt, const std::string &zqdm, table &result, std::string *error) {
	//adapt for batch api
	std::vector<security> securities;

	//set security information
	securities.push_back(security(mkt, zqdm));

	return  query_current_quote_data(securities, result, error);
}

int tdx1::query_current_quote_data(const std::vector<security> &securities, table &result, std::string *error) {
	//batch query count
	short count = (short)securities.size();

	//query input data
	byte markets[tdx1cfg::BATCH_LIMIT];
	const char* codes[tdx1cfg::BATCH_LIMIT];
	for (short i = 0; i < count; i++) {
		markets[i] = (byte)securities[i].mkt;
		codes[i] = securities[i].code.c_str();
	}

	// query server
	bool res = _quote->TdxHq_GetSecurityQuotes(markets, codes, count, _results[0], _errors[0]);
	if (!res) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_f10_category(market mkt, const std::string &zqdm, table &result, std::string *error) {
	bool res = _quote->TdxHq_GetCompanyInfoCategory((byte)mkt, zqdm.c_str(), _results[0], _errors[0]);
	if (!res) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_f10_content(market mkt, const std::string &zqdm, const std::string &file, int start, int length, table &result, std::string *error) {

	short scount = 0;
	bool res = _quote->TdxHq_GetCompanyInfoContent((byte)mkt, zqdm.c_str(), file.c_str(), start, length,  _results[0], _errors[0]);
	if (!res) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_xdxr_data(market mkt, const std::string &zqdm, table &result, std::string *error) {
	bool res = _quote->TdxHq_GetXDXRInfo((byte)mkt, zqdm.c_str(), _results[0], _errors[0]);
	if (!res) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	result = cube::str::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx1::query_finance_data(market mkt, const std::string &zqdm, table &result, std::string *error) {
	bool res = _quote->TdxHq_GetFinanceInfo((byte)mkt, zqdm.c_str(), _results[0], _errors[0]);
	if (!res) {
		cube::safe_assign<std::string>(error, _errors[0]);
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

	for (int i = 0; i < tdx1cfg::BATCH_LIMIT; i++) {
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