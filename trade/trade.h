#pragma once
#include "stdtrd.h"

BEGIN_TRADE_NAMESPACE
//trader for account
class trade
{
public:
	/*
	*	initialize trade service of specified security account
	*@param account: in, security account
	*@param error: out, error message when failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int init(std::string account, std::string *error = 0) = 0;

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
	virtual int login(std::string ip, ushort port, std::string version, int deptid, std::string login_account, std::string trade_account, std::string trade_pwd, std::string communicate_pwd, std::string &error) = 0;

	/*
	*	query current trading data of account by specified data category
	*@param category: in, data category
	*@param result: out, query result
	*@param error: out, error message when query failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int query(ccategory_t category, table_t &result, std::string &error) = 0;
	
	/*
	*	query current trading data of accounts by specified data categories
	*@param categories: in, data categories
	*@param results: out, query results
	*@param errors: out, error messages when query failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int query(std::vector<ccategory_t> categories, std::vector<table_t> &results, std::vector<std::string> &errors) = 0;

	/*
	*	query current trading data of accounts by specified data categories
	*@param categories: in, data categories
	*@param results: out, query results
	*@param errors: out, error messages when query failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int query(hcategory_t category, std::string start_date, std::string end_date, table_t &result, std::string &error) = 0;

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
	virtual int send(ocategory_t category, pricetype_t type, std::string gddm, std::string zqdm, float price, int count, table_t &result, std::string& error) = 0;

	/*
	*	send delegate order to remote server
	*@param order, order data with an order_t object
	*@param result: out, send order result
	*@param error: out, error message when send order failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int send(order_t order, table_t &result, std::string& error) = 0;

	/*
	*	send delegate orders to remote server
	*@param orders, orders data
	*@param results: out, send order results
	*@param errors: out, error messages when send order failed
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int send(std::vector<order_t> orders, std::vector<table_t> &results, std::vector<std::string> &errors) = 0;

	/*
	*	cancel order by specified order number
	*@param exchange_id: in, exchange id of the order sent
	*@param order_no: in, order number want to cancel
	*@param result: out, cancel result
	*@param error, out, error message when cancel order failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int cancel(std::string exchangeid, std::string order_no, table_t &result, std::string& error) = 0;

	/*
	*	cancel order by specified order object
	*@param order: in, order object
	*@param result: out, cancel result
	*@param error, out, error message when cancel order failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int cancel(order_t order, table_t &result, std::string& error) = 0;

	/*
	*	cancel orders by specified order object
	*@param orders: in, orders object
	*@param results: out, cancel results
	*@param errors, out, error messages when cancel order failed.
	*@return:
	*	0 for success, otherwise <0
	*/
	virtual int cancel(std::vector<order_t> orders, std::vector<table_t> &results, std::vector<std::string>& errors) = 0;

	/*
	*	get current quotation of specfied stock by stock code
	*@param stock_code: in, stock code
	*@param result: out, quotation of stock
	*@param error: out, error message when get quotation failed
	*@return:
	*	0 for success, otherwise < 0
	*/
	virtual int quote(std::string stock_code, table_t &result, std::string& error) = 0;
	
	/*
	*	get current quotation of specifed stocks
	*@param stock_codes: in, stock codes
	*@param results: out, quotation of stocks
	*@param errors: out, error messages when get quotation failed
	*@return:
	*	0 for success, otherwise < 0
	*/
	virtual int quote(std::vector<std::string> stock_codes, std::vector<table_t> &results, std::vector<std::string>& errors) = 0;

	/*
	*	repay the borrowing of securites margin trading
	*@param amount: in, repay money amount
	*@param result: out, repay result
	*@param error: out, error message when get repay failed
	*@return:
	*	0 for success, otherwise < 0
	*/
	virtual int repay(std::string amount, table_t &result, std::string& error) = 0;

	/*
	*	logout from remote service
	*@return:
	*	always 0
	*/
	virtual int logout() = 0;

	/*
	*	destroy the trade service
	*@return:
	*	always 0
	*/
	virtual int destroy() = 0;
};
END_TRADE_NAMESPACE
