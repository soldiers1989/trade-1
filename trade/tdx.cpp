#include "tdx.h"
#include "cube\str.h"

BEGIN_TRADE_NAMESPACE
const char* tdxerr::ERR_ACCOUNT_CONFLICT = "登录账户不一致";
const char* tdxerr::ERR_BATCH_COUNT = "批量请求数组过大";

const int tdxcfg::BUFFER_SIZE_RESULT = 64 * 1024;
const int tdxcfg::BUFFER_SIZE_ERROR = 4 * 1024;
const char* tdxcfg::RESULT_ROW_SEP = "\n";
const char* tdxcfg::RESULT_COL_SEP = "\t";

int tdx::init(const std::string &workdir, std::string *error/* = 0*/) {
	_workdir = workdir;
	return 0;
}

int tdx::login(const std::string &ip, ushort port, const std::string &version, int deptid, const std::string &login_account, const std::string &trade_account, 
			   const std::string &trade_pwd, const std::string &communicate_pwd, std::string *error){
	//prepare tdx dll
	if(prepare(login_account, error) != 0)
		return -1;

	//check account
	if (login_account != _dll_account) {
		cube::safe_assign<std::string>(error, tdxerr::ERR_ACCOUNT_CONFLICT);
		return -1;
	}

	//save the account parameter
	_ip = ip;
	_port = port;
	_verion = version;
	_deptid = deptid;

	_login_account = login_account;
	_trade_account = trade_account;
	_trade_pwd = trade_pwd;
	_communicate_pwd = communicate_pwd;

	// login to the trade server
	_client_id = _trade->Logon(ip.c_str(), port, version.c_str(), deptid, login_account.c_str(), trade_account.c_str(), trade_pwd.c_str(), communicate_pwd.c_str(), _errors[0]);
	if (_client_id < 0) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}


	return 0;
}

int tdx::query(query::type category, table &result, std::string *error) {
	//query data
	_trade->QueryData(_client_id, static_cast<int>(category), _results[0], _errors[0]);

	if (!cube::str::empty(_errors[0])) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	//transfer result
	result = cube::str::split(_results[0], tdxcfg::RESULT_ROW_SEP, tdxcfg::RESULT_COL_SEP);

	return 0;
}

int tdx::query(const std::vector<query::type> &categories, std::vector<table> &results, std::vector<std::string> *errors) {
	//check batch count
	int count = (int)categories.size();
	if (count > tdxcfg::BATCH_LIMIT) {
		cube::safe_push<std::vector<std::string>, std::string>(errors, tdxerr::ERR_BATCH_COUNT);
		return -1;
	}

	//adapt parameters
	int pcategories[tdxcfg::BATCH_LIMIT];
	for (int i = 0; i < count; i++) {
		pcategories[i] = static_cast<int>(categories[i]);
	}

	//query data
	_trade->QueryDatas(_client_id, pcategories, count, _results, _errors);

	//transfer result
	int success_count = 0;
	for (int i = 0; i < count; i++) {
		if (cube::str::empty(_errors[i])) { //success query
			table result = cube::str::split(_results[i], tdxcfg::RESULT_ROW_SEP, tdxcfg::RESULT_COL_SEP);
			results.push_back(result);
			cube::safe_push<std::vector<std::string>, std::string>(errors, "");
			success_count++;
		}
		else { //failed query
			results.push_back(table());
			cube::safe_push<std::vector<std::string>, std::string>(errors, _errors[i]);
		}
	}
	
	return success_count;
}

int tdx::query(query::type category, const std::string &start_date, const std::string &end_date, table &result, std::string *error) {
	//query data
	_trade->QueryHistoryData(_client_id, static_cast<int>(category),  start_date.c_str(), end_date.c_str(), _results[0], _errors[0]);
	if (!cube::str::empty(_errors[0])) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	//transfer result
	result = cube::str::split(_results[0], tdxcfg::RESULT_ROW_SEP, tdxcfg::RESULT_COL_SEP);

	return 0;
}

int tdx::send(order order, table &result, std::string *error) {
	//send order
	return send(order.otype, order.ptype, order.gddm, order.zqdm, order.price, order.count, result, error);
}

int tdx::send(order::type category, price::type type, const std::string &gddm, const std::string &zqdm, float price, int count, table &result, std::string *error) {
	//send order
	_trade->SendOrder(_client_id, static_cast<int>(category), static_cast<int>(type), gddm.c_str(), zqdm.c_str(), price, count, _results[0], _errors[0]);
	if (!cube::str::empty(_errors[0])) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	//transfer result
	result = cube::str::split(_results[0], tdxcfg::RESULT_ROW_SEP, tdxcfg::RESULT_COL_SEP);

	return 0;
}

int tdx::send(const std::vector<order> &orders, std::vector<table> &results, std::vector<std::string> *errors) {
	//check batch count
	int count = (int)orders.size();
	if (count > tdxcfg::BATCH_LIMIT) {
		cube::safe_push<std::vector<std::string>, std::string>(errors, tdxerr::ERR_BATCH_COUNT);
		return -1;
	}

	//adapt parameters
	int categories[tdxcfg::BATCH_LIMIT], price_types[tdxcfg::BATCH_LIMIT], counts[tdxcfg::BATCH_LIMIT];
	const char* holders[tdxcfg::BATCH_LIMIT], * stocks[tdxcfg::BATCH_LIMIT];
	float prices[tdxcfg::BATCH_LIMIT];
	for (int i = 0; i < count; i++) {
		categories[i] = static_cast<int>(orders[i].otype);
		price_types[i] = static_cast<int>(orders[i].ptype);
		holders[i] = orders[i].gddm.c_str();
		stocks[i] = orders[i].zqdm.c_str();
		counts[i] = orders[i].count;
		prices[i] = orders[i].price;
	}

	//send orders
	_trade->SendOrders(_client_id, categories, price_types, holders, stocks, prices, counts, count, _results, _errors);

	//transfer results
	int success_count = 0;
	for (int i = 0; i < count; i++) {
		if (cube::str::empty(_errors[i])) { //success query
			table result = cube::str::split(_results[i], tdxcfg::RESULT_ROW_SEP, tdxcfg::RESULT_COL_SEP);
			results.push_back(result);
			cube::safe_push<std::vector<std::string>, std::string>(errors, "");
			success_count++;
		}
		else { //failed query
			results.push_back(table());
			cube::safe_push<std::vector<std::string>, std::string>(errors, _errors[i]);
		}
	}

	return success_count;
}

int tdx::cancel(const orderres &order, table &result, std::string *error) {
	return cancel(order.exchangeid, order.orderno, result, error);
}

int tdx::cancel(const std::string &exchangeid, const std::string &orderno, table &result, std::string *error) {
	//cancel order
	_trade->CancelOrder(_client_id, exchangeid.c_str(), orderno.c_str(), _results[0], _errors[0]);
	if (!cube::str::empty(_errors[0])) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	//transfer result
	result = cube::str::split(_results[0], tdxcfg::RESULT_ROW_SEP, tdxcfg::RESULT_COL_SEP);

	return 0;
}

int tdx::cancel(const std::vector<orderres> &orders, std::vector<table> &results, std::vector<std::string> *errors) {
	//check batch count
	int count = (int)orders.size();
	if (count > tdxcfg::BATCH_LIMIT) {
		cube::safe_push<std::vector<std::string>, std::string>(errors, tdxerr::ERR_BATCH_COUNT);
		return -1;
	}

	//adapt parameters
	const char* seids[tdxcfg::BATCH_LIMIT], * ordernos[tdxcfg::BATCH_LIMIT];
	for (int i = 0; i < count; i++) {
		seids[i] = orders[i].exchangeid.c_str();
		ordernos[i] = orders[i].orderno.c_str();
	}

	//send orders
	_trade->CancelOrders(_client_id, seids, ordernos, count, _results, _errors);

	//transfer results
	int success_count = 0;
	for (int i = 0; i < count; i++) {
		if (cube::str::empty(_errors[i])) { //success query
			table result = cube::str::split(_results[i], tdxcfg::RESULT_ROW_SEP, tdxcfg::RESULT_COL_SEP);
			results.push_back(result);
			cube::safe_push<std::vector<std::string>, std::string>(errors, "");
			success_count++;
		}
		else { //failed query
			results.push_back(table());
			cube::safe_push<std::vector<std::string>, std::string>(errors, _errors[i]);
		}
	}

	return success_count;

}

int tdx::quote(const std::string &code, table &result, std::string *error) {
	//get quote
	_trade->GetQuote(_client_id, code.c_str(), _results[0], _errors[0]);
	if (!cube::str::empty(_errors[0])) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	//transfer result
	result = cube::str::split(_results[0], tdxcfg::RESULT_ROW_SEP, tdxcfg::RESULT_COL_SEP);

	return 0;
}

int tdx::quote(const std::vector<std::string> &codes, std::vector<table> &results, std::vector<std::string> *errors) {
	//check batch count
	size_t count = codes.size();
	if (count > tdxcfg::BATCH_LIMIT) {
		cube::safe_push<std::vector<std::string>, std::string>(errors, tdxerr::ERR_BATCH_COUNT);
		return -1;
	}

	//adapt parameters
	const char* pstocks[tdxcfg::BATCH_LIMIT];
	for (size_t i = 0; i < count; i++) {
		pstocks[i] = codes[i].c_str();
	}

	//send orders
	_trade->GetQuotes(_client_id, pstocks, count, _results, _errors);

	//transfer results
	int success_count = 0;
	for (size_t i = 0; i < count; i++) {
		if (cube::str::empty(_errors[i])) { //success query
			table result = cube::str::split(_results[i], tdxcfg::RESULT_ROW_SEP, tdxcfg::RESULT_COL_SEP);
			results.push_back(result);
			cube::safe_push<std::vector<std::string>, std::string>(errors, "");
			success_count++;
		}
		else { //failed query
			results.push_back(table());
			cube::safe_push<std::vector<std::string>, std::string>(errors, _errors[i]);
		}
	}

	return success_count;
}

int tdx::repay(const std::string &amount, table &result, std::string *error) {
	//repay money
	_trade->Repay(_client_id, amount.c_str(), _results[0], _errors[0]);
	if (!cube::str::empty(_errors[0])) {
		cube::safe_assign<std::string>(error, _errors[0]);
		return -1;
	}

	//transfer result
	result = cube::str::split(_results[0], tdxcfg::RESULT_ROW_SEP, tdxcfg::RESULT_COL_SEP);

	return 0;
}


int tdx::logout() {
	if (_client_id != -1) {
		_trade->Logoff(_client_id);
		return 0;
	}
	else {
		return -1;
	}
}

int tdx::destroy() {

	if (_trade != 0) {
		_trade->CloseTdx();
		delete _trade;
		_trade = 0;
	}

	for (int i = 0; i < tdxcfg::BATCH_LIMIT; i++) {
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

int tdx::prepare(const std::string &account, std::string *error/* = 0*/) {
	//already prepared
	if (_trade != 0) {
		return 0;
	}

	//save account
	_dll_account = account;

	//first initialize the trade api module
	_trade = new tdxdll();
	int err = _trade->load(_workdir, account, error);
	if (err != 0) {
		return -1;
	}
	_trade->OpenTdx();

	//initialize the result and error buffer holder
	for (int i = 0; i < tdxcfg::BATCH_LIMIT; i++) {
		_results[i] = new char[tdxcfg::BUFFER_SIZE_RESULT];
		_errors[i] = new char[tdxcfg::BUFFER_SIZE_ERROR];
	}

	return 0;
}
END_TRADE_NAMESPACE
