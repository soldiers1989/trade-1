#include "tdx.h"
#include "util.h"
#include "error.h"
#include <iostream>

#define TDX_BUFFER_SIZE_RESULT 64*1024
#define TDX_BUFFER_SIZE_ERROR 4*1024
#define TDX_RESULT_ROW_SEP "\n"
#define TDX_RESULT_COL_SEP "\t"

tdx::tdx():_tdxapi(0) {
	for (int i = 0; i < TDX_BATCH_LIMIT; i++) {
		_results[i] = 0;
		_errors[i] = 0;
	}
}

tdx::~tdx() {

}

int tdx::init(std::string ip, unsigned short port, std::string version, int deptid) {
	//save trade server information
	_ip = ip;
	_port = port;
	_verion = version;
	_deptid = deptid;

	//initialize the result and error buffer holder
	for (int i = 0; i < TDX_BATCH_LIMIT; i++) {
		_results[i] = new char[TDX_BUFFER_SIZE_RESULT];
		_errors[i] = new char[TDX_BUFFER_SIZE_ERROR];
	}

	return 0;
}

int tdx::login(std::string account, std::string password, std::string &error) {
	//save the account parameter
	_account = account;
	_password = password;

	//initialize trade api first
	if (_tdxapi == 0) {
		_tdxapi = new tdxapi();
		int ret = _tdxapi->load(account.c_str(), "tdx.dll");
		if (ret != 0) {
			error = ERR_TDX_INIT_TDXDLL;
			return -1;
		}
		_tdxapi->open();
	}
	else {
		if (account != _account) {
			error = ERR_TDX_ACCOUNT_CONFLICT;
			return -1;
		}
	}

	// login to the trade server
	_client_id = _tdxapi->login(_ip.c_str(), _port, _verion.c_str(), _deptid, account.c_str(), account.c_str(), password.c_str(), password.c_str(), _errors[0]);
	if (_client_id < 0) {
		error = _errors[0];
		return -1;
	}

	return 0;
}

int tdx::query(ccategory_t category, table_t &result, std::string &error) {
	//query data
	_tdxapi->query_data(_client_id, static_cast<int>(category), _results[0], _errors[0]);
	if (!util::empty(_errors[0])) {
		error = _errors[0];
		return -1;
	}

	//transfer result
	result = util::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx::query(std::vector<ccategory_t> categories, std::vector<table_t> &results, std::vector<std::string> &errors) {
	//check batch count
	int count = (int)categories.size();
	if (count > TDX_BATCH_LIMIT) {
		errors.push_back(ERR_TDX_BATCH_COUNT);
		return -1;
	}

	//adapt parameters
	int pcategories[TDX_BATCH_LIMIT];
	for (int i = 0; i < count; i++) {
		pcategories[i] = static_cast<int>(categories[i]);
	}

	//query data
	_tdxapi->query_datas(_client_id, pcategories, count, _results, _errors);

	//transfer result
	int success_count = 0;
	for (int i = 0; i < count; i++) {
		if (util::empty(_errors[i])) { //success query
			table_t result = util::split(_results[i], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);
			results.push_back(result);
			errors.push_back("");
			success_count++;
		}
		else { //failed query
			results.push_back(table_t());
			errors.push_back(_errors[i]);
		}
	}
	
	return success_count;
}

int tdx::query(hcategory_t category, std::string start_date, std::string end_date, table_t &result, std::string &error) {
	//query data
	_tdxapi->query_history_data(_client_id, static_cast<int>(category),  start_date.c_str(), end_date.c_str(), _results[0], _errors[0]);
	if (!util::empty(_errors[0])) {
		error = _errors[0];
		return -1;
	}

	//transfer result
	result = util::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx::send(order_t order, table_t &result, std::string& error) {
	//send order
	return send(order.category, order.type, order.gddm, order.zqdm, order.price, order.count, result, error);
}

int tdx::send(ocategory_t category, price_t type, std::string gddm, std::string zqdm, float price, int count, table_t &result, std::string& error) {
	//send order
	_tdxapi->send_order(_client_id, static_cast<int>(category), static_cast<int>(type), gddm.c_str(), zqdm.c_str(), price, count, _results[0], _errors[0]);
	if (!util::empty(_errors[0])) {
		error = _errors[0];
		return -1;
	}

	//transfer result
	result = util::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx::send(std::vector<order_t> orders, std::vector<table_t> &results, std::vector<std::string> &errors) {
	//check batch count
	int count = (int)orders.size();
	if (count > TDX_BATCH_LIMIT) {
		errors.push_back(ERR_TDX_BATCH_COUNT);
		return -1;
	}

	//adapt parameters
	int categories[TDX_BATCH_LIMIT], price_types[TDX_BATCH_LIMIT], counts[TDX_BATCH_LIMIT];
	const char* holders[TDX_BATCH_LIMIT], * stocks[TDX_BATCH_LIMIT];
	float prices[TDX_BATCH_LIMIT];
	for (int i = 0; i < count; i++) {
		categories[i] = static_cast<int>(orders[i].category);
		price_types[i] = static_cast<int>(orders[i].type);
		holders[i] = orders[i].gddm.c_str();
		stocks[i] = orders[i].zqdm.c_str();
		counts[i] = orders[i].count;
		prices[i] = orders[i].price;
	}

	//send orders
	_tdxapi->send_orders(_client_id, categories, price_types, holders, stocks, prices, counts, count, _results, _errors);

	//transfer results
	int success_count = 0;
	for (int i = 0; i < count; i++) {
		if (util::empty(_errors[i])) { //success query
			table_t result = util::split(_results[i], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);
			results.push_back(result);
			errors.push_back("");
			success_count++;
		}
		else { //failed query
			results.push_back(table_t());
			errors.push_back(_errors[i]);
		}
	}

	return success_count;
}

int tdx::cancel(order_t order, table_t &result, std::string& error) {
	return cancel(order.seid, order.orderno, result, error);
}

int tdx::cancel(std::string seid, std::string orderno, table_t &result, std::string& error) {
	//cancel order
	_tdxapi->cancel_order(_client_id, seid.c_str(), orderno.c_str(), _results[0], _errors[0]);
	if (!util::empty(_errors[0])) {
		error = _errors[0];
		return -1;
	}

	//transfer result
	result = util::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx::cancel(std::vector<order_t> orders, std::vector<table_t> &results, std::vector<std::string>& errors) {
	//check batch count
	int count = (int)orders.size();
	if (count > TDX_BATCH_LIMIT) {
		errors.push_back(ERR_TDX_BATCH_COUNT);
		return -1;
	}

	//adapt parameters
	const char* seids[TDX_BATCH_LIMIT], * ordernos[TDX_BATCH_LIMIT];
	for (int i = 0; i < count; i++) {
		seids[i] = orders[i].seid.c_str();
		ordernos[i] = orders[i].orderno.c_str();
	}

	//send orders
	_tdxapi->cancel_orders(_client_id, seids, ordernos, count, _results, _errors);

	//transfer results
	int success_count = 0;
	for (int i = 0; i < count; i++) {
		if (util::empty(_errors[i])) { //success query
			table_t result = util::split(_results[i], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);
			results.push_back(result);
			errors.push_back("");
			success_count++;
		}
		else { //failed query
			results.push_back(table_t());
			errors.push_back(_errors[i]);
		}
	}

	return success_count;

}

int tdx::quote(std::string stock, table_t &result, std::string& error) {
	//get quote
	_tdxapi->get_quote(_client_id, stock.c_str(), _results[0], _errors[0]);
	if (!util::empty(_errors[0])) {
		error = _errors[0];
		return -1;
	}

	//transfer result
	result = util::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}

int tdx::quote(std::vector<std::string> stocks, std::vector<table_t> &results, std::vector<std::string>& errors) {
	//check batch count
	int count = (int)stocks.size();
	if (count > TDX_BATCH_LIMIT) {
		errors.push_back(ERR_TDX_BATCH_COUNT);
		return -1;
	}

	//adapt parameters
	const char* pstocks[TDX_BATCH_LIMIT];
	for (int i = 0; i < count; i++) {
		pstocks[i] = stocks[i].c_str();
	}

	//send orders
	_tdxapi->get_quotes(_client_id, pstocks, count, _results, _errors);

	//transfer results
	int success_count = 0;
	for (int i = 0; i < count; i++) {
		if (util::empty(_errors[i])) { //success query
			table_t result = util::split(_results[i], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);
			results.push_back(result);
			errors.push_back("");
			success_count++;
		}
		else { //failed query
			results.push_back(table_t());
			errors.push_back(_errors[i]);
		}
	}

	return success_count;
}

int tdx::repay(std::string amount, table_t &result, std::string& error) {
	//repay money
	_tdxapi->repay(_client_id, amount.c_str(), _results[0], _errors[0]);
	if (!util::empty(_errors[0])) {
		error = _errors[0];
		return -1;
	}

	//transfer result
	result = util::split(_results[0], TDX_RESULT_ROW_SEP, TDX_RESULT_COL_SEP);

	return 0;
}


int tdx::logout() {
	if (_client_id != -1) {
		_tdxapi->logout(_client_id);
		return 0;
	}
	else {
		return -1;
	}
}

int tdx::destroy() {

	if (_tdxapi != 0) {
		_tdxapi->close();
		delete _tdxapi;
		_tdxapi = 0;
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