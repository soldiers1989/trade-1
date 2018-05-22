#pragma once
#include "trade.h"
#include "tdxdll.h"

BEGIN_TRADE_NAMESPACE
//tdx error message
class tdxerr {
public:
	static const char* ERR_ACCOUNT_CONFLICT;
	static const char* ERR_BATCH_COUNT;
};

//tdx comunication configure
class tdxcfg {
public:
	static const int BATCH_LIMIT = 8;
	static const int BUFFER_SIZE_RESULT;
	static const int BUFFER_SIZE_ERROR;
	static const char* RESULT_ROW_SEP;
	static const char* RESULT_COL_SEP;

};

//tdx trade api
class tdx : public trade
{
public:
	tdx() : _trade(0) {}
	virtual ~tdx() {}

public:
	/*
	*	initialize trade service
	*@param workdir: in, working directory
	*@param error: out, error message when failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int init(const std::string &workdir, std::string *error = 0);

	/*
	*	account login to the remote trading server
	*@param ip: in, remote trading server ip
	*@param port: in, remote trading server port
	*@param version: in, version of client
	*@param deptid: in, department of account belongs to
	*@param login_account: in, login account, may be the capital account or customer account of security broker
	*@param trade_account: in, trade account, usually same as the login account
	*@param trade_pwd: in, trade password
	*@param communicate_pwd: in, communication passowrd, usually same as the trade passowrd
	*@param error: out, error message when login failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int login(const std::string &ip, ushort port, const std::string &version, int deptid,
		const std::string &login_account, const std::string &trade_account, const std::string &trade_pwd, const std::string &communicate_pwd,
		std::string *error = 0);
	
	/*
	*	query current trading data of account by specified data category
	*@param category: in, data category
	*@param result: out, query result
	*@param error: out, error message when query failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int query(query::type category, table &result, std::string *error = 0);

	/*
	*	query current trading data of accounts by specified data categories
	*@param categories: in, data categories
	*@param results: out, query results
	*@param errors: out, error messages when query failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int query(const std::vector<query::type> &categories, std::vector<table> &results, std::vector<std::string> *errors = 0);

	/*
	*	query history trading data of accounts by specified data categories
	*@param category: in, data category
	*@param results: out, query results
	*@param errors: out, error messages when query failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int query(query::type category, const std::string &start_date, const std::string &end_date, table &result, std::string *error = 0);

	/*
	*	send delegate order to remote server
	*@param order, order data with an order_t object
	*@param result: out, send order result
	*@param error: out, error message when send order failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int send(order order, table &result, std::string *error = 0);

	/*
	*	send delegate order to remote server
	*@param category: in, order category
	*@param type: in, delegate price type
	*@param gddm: in, order's shareholder code
	*@param zqdm: in, order's stock code
	*@param price: in, delegate price
	*@param count: in, delegate count
	*@param result: out, send order result
	*@param error: out, error message when send order failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int send(order::type category, price::type type, const std::string &gddm, const std::string &zqdm, float price, int count, table &result, std::string *error = 0);


	/*
	*	send delegate orders to remote server
	*@param orders, orders data
	*@param results: out, send order results
	*@param errors: out, error messages when send order failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int send(const std::vector<order> &orders, std::vector<table> &results, std::vector<std::string> *errors = 0);

	/*
	*	cancel order by specified order object
	*@param order: in, order object
	*@param result: out, cancel result
	*@param error, out, error message when cancel order failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int cancel(const orderres &order, table &result, std::string *error = 0);

	/*
	*	cancel order by specified order number
	*@param exchange_id: in, exchange id of the order sent
	*@param order_no: in, order number want to cancel
	*@param result: out, cancel result
	*@param error, out, error message when cancel order failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int cancel(const std::string &exchangeid, const std::string &orderno, table &result, std::string *error = 0);

	/*
	*	cancel orders by specified order object
	*@param orders: in, orders object
	*@param results: out, cancel results
	*@param errors, out, error messages when cancel order failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int cancel(const std::vector<orderres> &orders, std::vector<table> &results, std::vector<std::string> *errors = 0);

	/*
	*	get current quotation of specfied stock by stock code
	*@param code: in, stock code
	*@param result: out, quotation of stock
	*@param error: out, error message when get quotation failed
	*@return:
	*	0 for success, otherwise < 0
	*/
	virtual int quote(const std::string &code, table &result, std::string *error = 0);

	/*
	*	get current quotation of specifed stocks
	*@param codes: in, stock codes
	*@param results: out, quotation of stocks
	*@param errors: out, error messages when get quotation failed
	*@return:
	*	0 for success, otherwise < 0
	*/
	virtual int quote(const std::vector<std::string> &codes, std::vector<table> &results, std::vector<std::string> *errors = 0);

	/*
	*	repay the borrowing of securites margin trading
	*@param amount: in, repay money amount
	*@param result: out, repay result
	*@param error: out, error message when get repay failed
	*@return:
	*	0 for success, otherwise < 0
	*/
	virtual int repay(const std::string &amount, table &result, std::string *error = 0);

	/*
	*	logout from remote service
	*@return:
	*	always 0
	*/
	virtual int logout();

	/*
	*	destroy the trade service
	*@return:
	*	always 0
	*/
	virtual int destroy();

private:
	/*
	*	prepare tdx dll module
	*@param account: in, user login account
	*@param error: out, error message for failure
	*@return:
	*	0 for success, otherwise <0
	*/
	int prepare(const std::string &account, std::string *error = 0);

private:
	//working directory
	std::string _workdir;

	//remote trade server ip
	std::string _ip;
	//remote trader server port
	unsigned short _port;
	//department id
	int _deptid;
	//client verion
	std::string _verion;

	//dll module account limit
	std::string _dll_account;


	//login account name
	std::string _login_account;
	//trade account name
	std::string _trade_account;
	//trade password
	std::string _trade_pwd;
	//communicate password
	std::string _communicate_pwd;

private:
	//trade api using tdx
	tdxdll *_trade;

	//client id after login
	int _client_id;

	//result holder
	char *_results[tdxcfg::BATCH_LIMIT];

	//error holder
	char *_errors[tdxcfg::BATCH_LIMIT];
};
END_TRADE_NAMESPACE
